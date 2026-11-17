"""Last pass: make sure every Mass has every chant and both readings.

Each Mass gets a list of required parts (`req`): for a day of the Proper of the Time, the parts its
Mass has in the Roman Graduale (the structure of the Dominican Mass is the same); otherwise Introit,
Gradual, Alleluia (Tract from Septuagesima to Easter), Offertory and Communion.
Anything still missing after the Dominican books is taken from the matching Mass of jgabc (the Roman
Graduale and Missal), found by its day or by the same Introit, and marked 'roman'.
"""
import json, re, os, shutil, sys, io
_o = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import norm, same
sys.stdout = _o

PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
RP = json.load(open('sources_roman_proprium.json'))
RL = json.load(open('sources_roman_lectiones.json'))
COMMON_KEYS = {'7*': 'mass_ii_martyr_not_bishop', '11*': 'mass_ii_martyr_bishop', '15*': 'mass_one_martyr',
               '18*': 'mass_i_martyr_not_bishop', '21*': 'mass_iii_two_or_more_martyr', '25*': 'mass_i_two_or_more_martyr',
               '28*': 'mass_two_or_more_martyr', '30*': 'mass_ii_confessor_bishop', '32*': 'mass_i_confessor_bishop',
               '35*': 'mass_doctors', '39*': 'mass_ii_confessor_not_bishop', '42*': 'mass_i_confessor_not_bishop',
               '45*': 'mass_i_virgin_martyr', '48*': 'mass_ii_virgin_martyr', '51*': 'mass_holy_woman_not_martyr',
               '55*': 'mass_i_virgin_not_martyr', '1*': 'mass_vigil_apostle', '114*': 'defunctorum',
               '62*': 'votiveSES', '64*': 'votiveJCSES', '68*': 'votivePJC', '75*': 'votiveSS', '79*': 'SMpentecost',
               '82*': 'SMpentecost', '93*': 'votiveFP', '110*': 'nuptialis'}
# Readings of the Commons in the Roman Missal (1962), used only where the Dominican Missal could not be read
COMMON_READINGS = {
    '11*': ['Ad Corinthios 2 1: 3-7', 'Matthæus 16: 24-27'], '7*': ['Ad Timotheum 2 2: 8-10; 3: 10-12', 'Joannes 12: 24-26'],
    '18*': ['Sapientia 10: 10-14', 'Matthæus 10: 34-42'], '15*': ['Sapientia 5: 1-5', 'Joannes 15: 1-7'],
    '25*': ['Ad Hebræos 10: 32-38', 'Lucas 21: 9-19'], '21*': ['Ad Hebræos 11: 33-39', 'Lucas 6: 17-23'],
    '28*': ['Sapientia 5: 1-5', 'Joannes 15: 5-11'], '32*': ['Ecclesiasticus 44: 16-27; 45: 3-20', 'Matthæus 25: 14-23'],
    '30*': ['Ad Hebræos 7: 23-27', 'Matthæus 24: 42-47'], '35*': ['Ad Timotheum 2 4: 1-8', 'Matthæus 5: 13-19'],
    '42*': ['Ecclesiasticus 31: 8-11', 'Lucas 12: 35-40'], '39*': ['Ad Corinthios 1 4: 9-14', 'Lucas 12: 32-34'],
    '45*': ['Ecclesiasticus 51: 1-8, 12', 'Matthæus 25: 1-13'], '48*': ['Ad Corinthios 1 7: 25-34', 'Matthæus 13: 44-52'],
    '55*': ['Ad Corinthios 2 10: 17-18; 11: 1-2', 'Matthæus 25: 1-13'], '51*': ['Proverbia 31: 10-31', 'Matthæus 13: 44-52'],
    '1*': ['Ad Ephesios 2: 19-22', 'Lucas 6: 12-19'],
}
MON3 = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def ptype(c):
    return 'gr' if c['code'] in ('re', 'gr') else c['code']


def run(masses, sections, groups, allchants, temporale, jgabc_dir, site_dir):
    roman_files = {}
    temp_keys = set(next(s for s in sections if s['id'] == 'tempore')['items'])
    roman_struct = {t['key']: t.get('roman') or {} for t in temporale}
    by_intro = {}
    for k, p in RP.items():
        if p.get('in'):
            by_intro.setdefault(norm(p['in'][0]['name'] or '')[:18], []).append(k)
    gpage = {g['page']: g for g in groups}

    def dominican_by_incipit(part, inc):
        for c in allchants.values():
            if ptype(c) == part and same(c['incipit'], inc, 2):
                return c['id']
        return None

    def roman_chant(rid, name, part):
        key = 'r%d' % rid
        if key not in roman_files:
            src = os.path.join(jgabc_dir, 'gabc', '%d.gabc' % rid)
            os.makedirs(os.path.join(site_dir, 'gabc', 'r'), exist_ok=True)
            shutil.copy(src, os.path.join(site_dir, 'gabc', 'r', '%d.gabc' % rid))
            roman_files[key] = {'p': part, 'i': name or '', 'pg': 'GR', 'roman': True}
        return key

    def jgabc_key(k, M):
        """The jgabc Mass that corresponds to this one: same key, same date, or same Introit."""
        if k in RP:
            return k
        intro = (M['parts'].get('in') or [{}])[0].get('id')
        if 'month' in M and M['month'] < 12 and intro is not None and not str(intro).startswith('r'):
            dk = '%s%d' % (MON3[M['month']], M['day'])
            for cand in [x for x in RP if x == dk or re.match(dk + r'(or\d+)?$', x)]:
                if RP[cand].get('in') and same(RP[cand]['in'][0]['name'] or '', allchants[intro]['incipit'], 2):
                    return cand
        if intro is not None and not str(intro).startswith('r'):
            g = gpage.get(allchants[intro]['page']) if False else None
            pg = allchants[intro]['page']
            for gp, ck in COMMON_KEYS.items():
                if any(c['id'] == intro for c in (gpage.get(gp) or {'chants': []})['chants']):
                    return ck
            cands = by_intro.get(norm(allchants[intro]['incipit'])[:18]) or []
            if not cands:
                n = norm(allchants[intro]['incipit']).split()
                cands = [x for kk, v in by_intro.items() if kk.split()[:2] == n[:2] for x in v]
            if 'month' in M and M['month'] < 12:
                dk = '%s%d' % (MON3[M['month']], M['day'])
                for c in cands:
                    if c.startswith(dk):
                        return c
            return cands[0] if cands else None
        return None

    stats = {'roman_chants': 0, 'roman_readings': 0, 'dominican_found': 0}
    for s in sections:
        for k in s['items']:
            M = masses[k]
            if k in temp_keys:
                req = ['in'] + [p for p in PARTS[1:] if roman_struct.get(k, {}).get(p)]
                if k == 'Quad6f':
                    req = ['tr']
                if len(req) == 1 and k != 'Quad6f':
                    req = ['in', 'gr', 'al', 'of', 'co']
            else:
                req = ['in', 'gr', 'al', 'of', 'co']
            if 'gr' in req and (len(M['parts'].get('al') or []) >= 2 or (k not in temp_keys and (M.get('season') or {}).get('pasch', {}).get('al') and not M['parts'].get('gr'))):
                req = [p for p in req if p != 'gr']
            if M.get('page') in ('15*', '28*'):
                req = [p for p in req if p != 'gr']
            M['req'] = req
            jk = jgabc_key(k, M)
            M['jgabc'] = jk
            # chants
            for p in req:
                if M['parts'].get(p):
                    continue
                src = (RP.get(jk) or {}).get(p) or []
                if not src and k in temp_keys:
                    continue
                ids = []
                for c in src:
                    d = dominican_by_incipit(p, c['name'] or '')
                    if d:
                        ids.append({'id': d, 'inferred': True}); stats['dominican_found'] += 1
                    else:
                        ids.append({'id': roman_chant(c['id'], c['name'], p), 'roman': True}); stats['roman_chants'] += 1
                if ids:
                    M['parts'][p] = ids if p == 'gr' and k in temp_keys else ids[:1]
            # seasonal Tract for saints (Septuagesima to Easter), from the same jgabc Mass
            if k not in temp_keys and M['parts'].get('al') and not (M.get('season') or {}).get('lent', {}).get('tr'):
                src = (RP.get(jk) or {}).get('tr') or []
                if src:
                    c = src[0]
                    d = dominican_by_incipit('tr', c['name'] or '')
                    M.setdefault('season', {}).setdefault('lent', {})['tr'] = [{'id': d, 'inferred': True} if d else {'id': roman_chant(c['id'], c['name'], 'tr'), 'roman': True}]
            # readings
            rd = M.get('readings') or []
            has_g = any(r['type'] == 'Gospel' for r in rd)
            has_e = any(r['type'] != 'Gospel' for r in rd)
            if not (has_g and has_e):
                lk = k if k in RL else (jk if jk in RL else None)
                if not lk and 'month' in M and M['month'] < 12:
                    dk = '%s%d' % (MON3[M['month']], M['day'])
                    lk = dk if dk in RL else None
                refs = RL[lk] if lk else None
                if not refs:
                    intro = (M['parts'].get('in') or [{}])[0].get('id')
                    for gp, rr in COMMON_READINGS.items():
                        g = gpage.get(gp)
                        if M.get('page') == gp or (g and intro is not None and any(c['id'] == intro for c in g['chants'])):
                            refs = rr
                            break
                if refs:
                    new = []
                    for i, r in enumerate(refs):
                        t = 'Gospel' if i == len(refs) - 1 else ('Epistle' if i == len(refs) - 2 else 'Lesson')
                        if (t == 'Gospel' and not has_g) or (t != 'Gospel' and not has_e):
                            new.append({'type': t, 'ref': r, 'roman': True})
                    if new:
                        stats['roman_readings'] += 1
                        M['readings'] = sorted(rd + new, key=lambda r: {'Lesson': 0, 'Epistle': 1, 'Gospel': 2}[r['type']])
    return roman_files, stats
