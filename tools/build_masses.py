import os
"""Assemble the site's data file (data/masses.js) from the aligned Temporale and Sanctorale.

Every Mass lists its chants by part; each chant is a GregoBase ID of the Graduale O.P. (1950).
'inferred': the chant is not printed in this Mass's place in the Graduale (it is used again from
elsewhere in the book); it was found by the incipit the same day has in the Roman Graduale.
"""
import json, re, sys, io, csv, os, unicodedata
_o = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import norm, same
sys.stdout = _o

G = json.load(open('groups.json'))
groups, front, kyriale = G['groups'], G['front'], G['kyriale']
temporale = json.load(open('temporale_align.json'))
sdates = {int(k): v for k, v in json.load(open('sanct_dates.json')).items()}
cal = json.load(open('calendar.json'))
lines = open('/home/claude/dl/txt/M39r.txt', encoding='utf8').read().split('\n')
_o = sys.stdout; sys.stdout = io.StringIO()
from build_sanctorale import bydate, find_common, GUESS
sys.stdout = _o

import resolve_m39 as R
ORDO = [o for o in json.load(open('ordo2026.json')) if not o['region']]
PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
allchants = {}
for g in groups + [front]:
    for c in g['chants']:
        allchants[c['id']] = c
for c in kyriale:
    allchants[c['id']] = c


def ptype(c):
    return 'gr' if c['code'] in ('re', 'gr') else c['code']


def core(g, roman=None):
    taken, extras, seen_co, last, co_page = {}, [], False, None, None
    for c in g['chants']:
        t = ptype(c)
        if t not in PARTS:
            extras.append(c['id']); last = t; continue
        ok = False
        if t not in taken:
            ok = not seen_co or (roman is not None and t in roman) or (roman is None and c['page'] == co_page)
        elif t in ('gr', 'al', 'tr') and not seen_co and last == t:
            ok = True  # Ember days: several Graduals; Paschaltide: two Alleluias
        if ok:
            taken.setdefault(t, []).append({'id': c['id']})
        else:
            extras.append(c['id'])
        if t == 'co' and not seen_co:
            seen_co, co_page = True, c['page']
        last = t
    return taken, extras


def lookup(part, incipit):
    for c in allchants.values():
        if ptype(c) == part and same(c['incipit'], incipit, 2):
            return c['id']
    return None


masses, sections = {}, []


def add(key, m):
    masses[key] = m
    return key


# ---- Temporale ----------------------------------------------------------------
items = []
for t in temporale:
    g = groups[t['gid']]
    roman = t.get('roman') or {}
    taken, extras = core(g, roman if roman else None)
    if t['conf'] == 'shared':
        parts = {'in': taken.get('in', [])}
        for p in PARTS[1:]:
            ids = [lookup(p, inc) for inc in roman.get(p, [])]
            ids = [i for i in ids if i]
            parts[p] = [{'id': i, 'inferred': True} for i in ids]
        extras = []
    else:
        parts = dict(taken)
        for p in PARTS[1:]:
            if p not in parts and roman.get(p):
                ids = [i for i in (lookup(p, inc) for inc in roman[p]) if i]
                if ids:
                    parts[p] = [{'id': i, 'inferred': True} for i in ids]
    note = {'introit': None, 'manual': 'Mass identified from the Missale O.P.; it differs from the Roman Mass of this day.',
            'shared': 'This day repeats an Introit printed elsewhere in the Graduale (p. %s); the other chants were found by the incipits of the same day in the Roman Graduale.' % g['page']}[t['conf']]
    items.append(add(t['key'], {'title': t['title'], 'en': t['en'], 'page': g['page'], 'conf': t['conf'], 'note': note,
                                'parts': {p: v for p, v in parts.items() if v}, 'extras': extras}))
# Good Friday is printed inside the Holy Thursday Mass (pp. 171-180)
ht = masses.get('Quad6h')
if ht:
    gf_ids = [c['id'] for c in groups[[t for t in temporale if t['key'] == 'Quad6h'][0]['gid']]['chants'] if c['page'] in ('171', '173', '176', '178', '179', '180')]
    gf = {'tr': [{'id': i} for i in gf_ids if ptype(allchants[i]) == 'tr']}
    pos = items.index('Quad6h') + 1
    masses['Quad6f'] = {'title': 'Feria VI in Parasceve', 'en': 'Good Friday', 'page': '171', 'conf': 'manual',
                        'note': 'Tracts of the Mass of the Presanctified; the Improperia and antiphons of the Adoration of the Cross are under "Other chants".',
                        'parts': gf, 'extras': [i for i in gf_ids if ptype(allchants[i]) != 'tr']}
    items.insert(pos, 'Quad6f')
    ht['extras'] = [i for i in ht['extras'] if i not in gf_ids]
sections.append({'id': 'tempore', 'title': 'Proprium de Tempore', 'en': 'Proper of the Time', 'items': items})

# ---- Commune & votive Masses -------------------------------------------------------
COMMON_TITLES = {
    '1*': ('Commune Apostolorum', 'Common of Apostles'),
    '7*': ('Commune unius Martyris', 'Common of One Martyr'),
    '11*': ('Commune unius Martyris Pontificis', 'Common of a Martyr Bishop'),
    '15*': ('Commune unius Martyris Tempore Paschali', 'Common of One Martyr in Paschaltide'),
    '18*': ('Commune unius Martyris (alia Missa)', 'Common of One Martyr (another Mass)'),
    '21*': ('Commune plurimorum Martyrum', 'Common of Several Martyrs'),
    '25*': ('Commune plurimorum Martyrum (alia Missa)', 'Common of Several Martyrs (another Mass)'),
    '28*': ('Commune plurimorum Martyrum Tempore Paschali', 'Common of Several Martyrs in Paschaltide'),
    '30*': ('Commune Confessoris Pontificis (alia Missa)', 'Common of a Confessor Bishop (another Mass)'),
    '32*': ('Commune Confessoris Pontificis', 'Common of a Confessor Bishop'),
    '35*': ('Commune Doctorum', 'Common of Doctors'),
    '39*': ('Commune Confessoris non Pontificis', 'Common of a Confessor not a Bishop'),
    '42*': ('Commune Confessoris non Pontificis (alia Missa)', 'Common of a Confessor not a Bishop (another Mass)'),
    '45*': ('Commune Virginis et Martyris', 'Common of a Virgin Martyr'),
    '48*': ('Commune Virginis et Martyris (alia Missa)', 'Common of a Virgin Martyr (another Mass)'),
    '51*': ('Commune Sanctarum Mulierum', 'Common of Holy Women'),
    '55*': ('Commune Virginum', 'Common of Virgins'),
    '62*': ('Missa votiva de SS. Sacramento', 'Votive Mass of the Blessed Sacrament'),
    '64*': ('Missa votiva de D.N.J.C. Summo et Aeterno Sacerdote', 'Votive Mass of Christ the High Priest'),
    '68*': ('Missa votiva de Passione Domini', 'Votive Mass of the Passion'),
    '75*': ('Missa votiva de Spiritu Sancto', 'Votive Mass of the Holy Spirit'),
    '79*': ('Missa votiva de B. Maria Virgine (Salve sancta parens)', 'Votive Mass of Our Lady (Salve sancta parens)'),
    '82*': ('Missa votiva de B. Maria Virgine (Salve radix sancta)', 'Votive Mass of Our Lady (Salve radix sancta)'),
    '89*': ('Missa in electione Summi Pontificis', 'Mass for the Election of a Pope'),
    '93*': ('Missa pro Fidei propagatione', 'Mass for the Propagation of the Faith'),
    '104*': ('Missa tempore mortalitatis', 'Mass in Time of Pestilence'),
    '110*': ('Missa pro Sponso et Sponsa', 'Nuptial Mass'),
    '114*': ('Missa pro Defunctis', 'Mass for the Dead'),
}
citems, vitems = [], []
for g in groups:
    if g['section'] not in ('commune', 'votivae', 'defunctorum'):
        continue
    la, en = COMMON_TITLES.get(g['page'], ('Missa «%s»' % g['introit'], 'Mass "%s"' % g['introit']))
    taken, extras = core(g)
    key = 'C' + g['page'].replace('*', 's')
    add(key, {'title': la, 'en': en, 'page': g['page'], 'conf': 'graduale', 'note': None,
              'parts': taken, 'extras': extras, 'introit': g['introit']})
    (citems if g['section'] == 'commune' else vitems).append(key)
    g['key'] = key
sections.append({'id': 'commune', 'title': 'Commune Sanctorum', 'en': 'Commons of Saints', 'items': citems})
sections.append({'id': 'votivae', 'title': 'Missae Votivae et pro Defunctis', 'en': 'Votive Masses and Requiem', 'items': vitems})

# ---- Sanctorale -------------------------------------------------------------------
MON = ['Ian.', 'Feb.', 'Mart.', 'Apr.', 'Maii', 'Iun.', 'Iul.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']
MEN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
proper_by_date = {}
for gid, d in sdates.items():
    if d['score'] >= 2:
        proper_by_date.setdefault((d['month'], d['day']), []).append(gid)
attached = set()
TEMPORAL = re.compile(r'NATIVITATIS DOMINI|NATIVITAS DOMINI|EPIPHANI|Infra Octavam|in Octava|VIGILIA$|Baptismatis|CHRISTI REGIS|Missa', re.I)


def common_ref(month, day):
    for t in bydate.get((month, day), []):
        m = re.search(r'Officium\s+([A-Z][^,\n]{2,40}?),?\s+(?:ut\s+in\s+Comm|in\s+Comm|de\s+Comm|ut\s+supra)', t)
        if m:
            return m.group(1).strip()
    return None


def feast_mass(f):
    mo, d = f['month'], f['day']
    for gid in proper_by_date.get((mo, d), []):
        return gid, 'proper', None
    ref = common_ref(mo, d)
    if ref:
        g = find_common(ref)
        if g:
            return g['gid'], 'common', ref
    for pat, inc in GUESS:
        if re.search(pat, f['name']):
            g = find_common(inc)
            if g:
                return g['gid'], 'guess', inc
            break
    return None, None, None


import unicodedata as _ud


def _w(s):
    s = ''.join(c for c in _ud.normalize('NFD', s) if not _ud.combining(c)).lower().replace('j', 'i').replace('æ', 'ae')
    return set(w for w in re.findall(r'[a-z]{4,}', s) if w not in ('sancti', 'sanctae', 'beati', 'beatae', 'virg', 'conf', 'mart', 'feria', 'missa', 'ordinis'))


def ordo_page(f):
    """The Missal page the 2026 Ordo gives for this feast (if it is celebrated in 2026)."""
    for o in ORDO:
        y, mo, d = map(int, o['date'].split('-'))
        if mo - 1 == f['month'] and d == f['day'] and (_w(o['name']) & _w(f['name'])):
            return o['m39']
    return None


TEMPORE_PAGES = lambda c: c['section'] == 'tempore'


def missal_mass(f, prefer):
    """Parts of the feast read from its page in the Missale O.P. 1939."""
    ref = ordo_page(f)
    if not ref:
        return None
    p = R.pdf_page(ref)
    parts, commref, seg = R.resolve(p, f['day'], f['month'], prefer)
    # a saint's Introit never comes from the Proper of the Time; a stray match there is OCR noise
    parts['in'] = [h for h in parts.get('in', []) if h[0]['section'] != 'tempore']
    if not parts['in']:
        return None
    return {'parts': parts, 'commref': commref, 'm39': ref}


sitems, bitems = [], []
for f in cal:
    if not f['beatus'] and TEMPORAL.search(f['name']):
        continue
    prefer = tuple(proper_by_date.get((f['month'], f['day']), []))
    mm = missal_mass(f, prefer)
    season = {}
    if mm:
        intro, isc = mm['parts']['in'][0][0], mm['parts']['in'][0][2]
        if prefer and groups[prefer[0]]['section'] == 'sanctorum' and not mm['commref']:
            gid, conf = prefer[0], 'missal'
        else:
            gid, conf = intro['gid'], 'missal'
        g = groups[gid]
        taken, extras = core(g)
        if g['section'] == 'commune' and gid != intro['gid']:
            pass
        # the Introit as the Missal gives it (e.g. without the Paschal alleluias)
        if intro['gid'] != gid or not taken.get('in'):
            if taken.get('in') and groups[gid]['section'] == 'sanctorum' and 'all' in allchants[taken['in'][0]['id']]['incipit']:
                season.setdefault('pasch', {})['in'] = taken['in']
            taken['in'] = [{'id': intro['id']}]
        # parts the Missal labels clearly override the Graduale's default
        for p, hits in mm['parts'].items():
            if p == 'in':
                continue
            for c, se, sc in hits:
                if sc < 2:
                    continue
                if p == 'al' and c['section'] == 'tempore':
                    se = 'pasch'
                if se == 'pasch':
                    if p == 'al':
                        season.setdefault('pasch', {}).setdefault('al', []).append({'id': c['id']})
                    continue
                elif se == 'lent' or p == 'tr':
                    season.setdefault('lent', {}).setdefault('tr', []).append({'id': c['id']})
                else:
                    if p not in [k for k in taken if taken.get(k) and k + '_set' in taken]:
                        taken[p] = []
                        taken[p + '_set'] = True
                    taken[p].append({'id': c['id']})
        for k in [k for k in taken if k.endswith('_set')]:
            del taken[k]
        if season.get('pasch', {}).get('al') and len(season['pasch']['al']) > 2:
            season['pasch']['al'] = season['pasch']['al'][:2]
        if 'tr' in taken and taken.get('al'):
            season.setdefault('lent', {})['tr'] = taken.pop('tr')
        # one Gradual, Alleluia, Offertory and Communion: alternatives from the Common go to the extras
        for p in ('gr', 'al', 'of', 'co'):
            if len(taken.get(p, [])) > 1:
                extras = [c['id'] for c in taken[p][1:]] + extras
                taken[p] = taken[p][:1]
        ref = mm['commref']
        note = ('Chants as given on p. %s of the Missale O.P. 1939 (the page cited by the 2026 Ordo)' % mm['m39']) + \
               ((', from the Common (Missal p. %s).' % ref) if ref else '.')
        if gid in prefer:
            attached.add(gid)
    else:
        gid, conf, ref = feast_mass(f)
        if gid is None:
            continue
        g = groups[gid]
        taken, extras = core(g)
        note = {'proper': 'Proper Mass, Graduale p. %s (matched to this date in the Missale O.P. 1939).' % g['page'],
                'common': 'The Missale O.P. 1939 gives Officium «%s» for this day: %s.' % (ref, masses.get(g.get('key'), {}).get('en', 'Graduale p. %s' % g['page'])),
                'guess': 'Common chosen from the saint\'s title (%s): check the Ordo.' % (masses.get(g.get('key'), {}).get('en', ref))}[conf]
        if conf == 'proper':
            attached.add(gid)
        for p in ('gr', 'al', 'of', 'co'):
            if len(taken.get(p, [])) > 1:
                extras = [c['id'] for c in taken[p][1:]] + extras
                taken[p] = taken[p][:1]
        if 'tr' in taken and taken.get('al'):
            season.setdefault('lent', {})['tr'] = taken.pop('tr')
    date_la = '%d %s' % (f['day'], MON[f['month']])
    key = 'S%02d%02d' % (f['month'] + 1, f['day']) + ('b' if f['beatus'] else '')
    while key in masses:
        key += 'x'
    add(key, {'title': '%s — %s' % (date_la, f['name']), 'en': '%s %d — %s' % (MEN[f['month']], f['day'], f['name']),
              'rank': f['rank'], 'op': f['op'], 'page': g['page'], 'conf': conf, 'note': note,
              'parts': {k: v for k, v in taken.items() if v}, 'season': season,
              'extras': extras, 'month': f['month'], 'day': f['day']})
    (bitems if f['beatus'] else sitems).append(key)
# proper Masses of the Graduale not attached to a calendar date
for g in groups:
    if g['section'] != 'sanctorum' or g['gid'] in attached:
        continue
    d = sdates.get(g['gid'])
    taken, extras = core(g)
    key = 'G' + g['page'].replace('.', '_')
    when = (' (c. %d %s)' % (d['day'], MON[d['month']])) if d else ''
    add(key, {'title': 'Missa «%s»%s' % (g['introit'], when), 'en': 'Mass "%s", Graduale p. %s' % (g['introit'], g['page']),
              'page': g['page'], 'conf': 'graduale', 'note': 'A proper Mass of the Sanctorale that could not be tied to a date in the calendar automatically.',
              'parts': taken, 'extras': extras, 'month': d['month'] if d else 12, 'day': d['day'] if d else 0})
    sitems.append(key)


def liturgical(k):  # year begins with Advent (St Andrew)
    m = masses[k]
    mo = m['month'] if m['month'] < 12 else 13
    return ((mo - 10) % 12 if mo < 12 else 99, m['day'])


sitems.sort(key=liturgical)
bitems.sort(key=liturgical)
sections.insert(1, {'id': 'sanctorum', 'title': 'Proprium Sanctorum', 'en': 'Proper of the Saints', 'items': sitems})
sections.insert(2, {'id': 'beati', 'title': 'Beati Ordinis (Missae pro opportunitate)', 'en': 'Dominican Blesseds', 'items': bitems})

# ---- complete every Mass from the St. Dominic Missal (1959) ---------------------------
import dm_merge
st = dm_merge.merge(masses, sections, groups, allchants, core, json.load(open('sources_roman_lectiones.json')), None, None)
print('St. Dominic Missal:', st)
import complete
ROMAN_FILES, st2 = complete.run(masses, sections, groups, allchants, temporale, os.environ.get('JGABC', '/home/claude/src/jgabc'), os.environ.get('SITE', 'site'))
print('Completion from jgabc:', st2)

# ---- error check against the St. Dominic Missal: where its entry is clearly one Mass, it decides --------
_dm = json.load(open('dm_masses.json'))['masses']
def _fl(x): return re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', (x or '').lower()).encode('ascii', 'ignore').decode().replace('j', 'i'))
_fixed = 0
for s_ in sections:
    if s_['id'] not in ('sanctorum', 'beati'):
        continue
    for k in s_['items']:
        M = masses[k]
        if 'month' not in M or M['month'] > 11:
            continue
        key = '%02d%02d' % (M['month'] + 1, M['day'])
        _nm = set(w[:5] for w in re.findall(r'[a-z]{4,}', _fl((M.get('name_en') or '') + ' ' + M['title']).replace('', '') if False else (unicodedata.normalize('NFD', ((M.get('name_en') or '') + ' ' + M['title']).lower()).encode('ascii', 'ignore').decode()))) - {'sanct', 'beati', 'beata', 'missa'}
        def _ov(m):
            return len(_nm & set(w[:5] for w in re.findall(r'[a-z]{4,}', unicodedata.normalize('NFD', m['title'].lower()).encode('ascii', 'ignore').decode())))
        cands = sorted([m for m in _dm if m['kind'] == 'saint' and m['key'] == key and _ov(m) > 0 and m['parts']], key=lambda m: -_ov(m))
        if not cands or (len(cands) > 1 and _ov(cands[0]) == _ov(cands[1])):
            continue
        d = cands[0]
        if any(len(v) > (2 if p == 'al' else 1) for p, v in d['parts'].items()):
            continue   # the parser merged two Masses here: leave it
        for p, ids in d['parts'].items():
            cur = [c['id'] for c in M['parts'].get(p, [])]
            if [_fl(allchants[i]['incipit'])[:10] for i in ids if i in allchants] != [_fl(allchants[i]['incipit'])[:10] for i in cur if i in allchants]:
                M['parts'][p] = [{'id': i} for i in ids if i in allchants][: (2 if p == 'al' else 1)]
                _fixed += 1
print('corrected from the St. Dominic Missal:', _fixed, 'chants')

# ---- English names of the feasts, from the 2026 Ordo O.P. ---------------------------
for k, M in masses.items():
    if 'month' not in M or M['month'] > 11 or M.get('name_en'):
        continue
    for o in ORDO:
        y, mo, d = map(int, o['date'].split('-'))
        if mo - 1 == M['month'] and d == M['day'] and o.get('en') and (_w(o['name']) & _w(M['title'])):
            M['name_en'] = re.split(r'\s{2,}', o['en'].strip())[0].rstrip('.')
            break

# ---- corrections identified by hand -----------------------------------------------
FIX_TITLES = {'G494': ('Vigilia S. Ioannis Baptistae', 'Vigil of St John the Baptist', 5, 23),
              'G502_3': ('Vigilia Ss. Petri et Pauli', 'Vigil of Sts Peter and Paul', 5, 28)}
for k, (la, en, mo, dy) in FIX_TITLES.items():
    if k in masses:
        masses[k].update(title='%d %s — %s' % (dy, MON[mo], la), en='%s %d — %s' % (MEN[mo], dy, en), name_en=en, month=mo, day=dy, req=['in', 'gr', 'of', 'co'])
        masses[k].pop('note', None)
for s_ in sections:
    if s_['id'] == 'votivae' and 'C76s' in s_['items']:
        s_['items'].remove('C76s')
    if s_['id'] == 'sanctorum':
        s_['items'].sort(key=lambda k: liturgical(k))
if 'Pasc6s' in masses:
    al = [c for c in allchants.values() if c['code'] == 'al' and c['incipit'].lower().startswith('confitemini')]
    if al and not masses['Pasc6s']['parts'].get('al'):
        masses['Pasc6s']['parts']['al'] = [{'id': al[0]['id']}]
if 'S0709' in masses and len(masses['S0709'].get('readings') or []) < 2:
    masses['S0709']['readings'] = [{'type': 'Epistle', 'ref': 'Ad Hebræos 10: 32-38', 'roman': True}, {'type': 'Gospel', 'ref': 'Lucas 21: 9-19', 'roman': True}]

# ---- corrections from the Missale O.P. (1939), checked page by page (m39_fixes.json) ----
def _normref(r):
    """'Matthæus 5: 43-6,4' -> 'Matthæus 5: 43-48; 6: 1-4' style cross-chapter ranges; '1 Petri 5' -> 'Petri 1 5'."""
    r = re.sub(r'^([1-4]) (Ad \w+|Petri|Joannis|Regum|Machabæorum|Paralipomenon)\b(.*)$', lambda m: m.group(2) + ' ' + m.group(1) + m.group(3), r.strip())
    r = re.sub(r'^([1-4]) (Ad \w+) ', lambda m: m.group(2) + ' ' + m.group(1) + ' ', r)
    m = re.match(r'^(.*?) (\d+): (\d+)-(\d+),(\d+)$', r)
    if m and int(m.group(4)) < int(m.group(3)):
        r = '%s %s: %s-99; %s: 1-%s' % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
    r = re.sub(r'(\d+): (\d+)(\d\d)$', lambda m: '%s: %s-%s' % (m.group(1), m.group(2), m.group(3)) if int(m.group(2)) < int(m.group(3)) else m.group(0), r)
    r = re.sub(r':(\d)', r': \1', r)
    if '-99;' in r:
        bk = re.match(r'^(.*?) \d+:', r).group(1); ch = int(re.search(r' (\d+): \d+-99;', r).group(1))
        try:
            last = max(int(l.split('\t')[1]) for l in open('site/bible/la/%s.txt' % bk, encoding='utf8') if l.split('\t')[0] == str(ch))
            r = r.replace('-99;', '-%d;' % last)
        except (OSError, ValueError):
            pass
    return r
for M in masses.values():
    for rd in M.get('readings') or []:
        rd['ref'] = _normref(rd['ref'])
if os.path.exists('m39_fixes.json'):
    FX = json.load(open('m39_fixes.json'))
    for k, parts in FX.get('parts', {}).items():
        for p, cid in parts.items():
            if k in masses:
                ids = cid if isinstance(cid, list) else [cid]
                if ids: masses[k]['parts'][p] = [dict({'id': c, 'm39': True}, **({'roman': True} if str(c).startswith('r') else {})) for c in ids]
                else: masses[k]['parts'].pop(p, None)
                if not ids and 'req' in masses[k]: masses[k]['req'] = [x for x in masses[k]['req'] if x != p]
    for k, rs in FX.get('readings', {}).items():
        if k in masses:
            masses[k]['readings'] = [{'type': t, 'ref': r, 'm39': True} for t, r in rs]
    for (old_r, new_r) in FX.get('generic', []):
        for M in masses.values():
            rs = M.get('readings') or []
            refs = [r['ref'] for r in rs]
            if all(o in refs for o in old_r):
                for r in rs:
                    if r['ref'] in old_r: r['ref'] = new_r[old_r.index(r['ref'])]; r['m39'] = True
    import copy as _copy
    for k, v in FX.get('new_masses', {}).items():
        if 'copy' in v and v['copy'] in masses:
            src = masses[v['copy']]
            v = dict(v)
            parts = {p: [x['id'] for x in ids] for p, ids in src['parts'].items()}
            parts.update(v.get('parts', {}))
            parts = {p: ids for p, ids in parts.items() if ids}
            v['parts'] = parts
            v.setdefault('req', list(src.get('req') or parts.keys()))
            v.setdefault('extras', list(src.get('extras') or []))
        masses[k] = {'title': v['title'], 'en': v['en'], 'page': v['page'], 'conf': v['conf'], 'note': v['note'],
                     'parts': {p: [{'id': i} for i in ids] for p, ids in v['parts'].items()}, 'extras': v.get('extras', []),
                     'req': v['req'], 'jgabc': None, 'order': v.get('order'), 'prophecies': v.get('prophecies'), 'ptr': v.get('ptr'), 'noAgnus': v.get('noAgnus'), 'readings': [{'type': t, 'ref': r, 'm39': True} for t, r in v['readings']]}
        for f_ in ('rank', 'month', 'day', 'name_en', 'color'):
            if f_ in v: masses[k][f_] = v[f_]
        masses[k]['season'] = {}
        placed = False
        for s_ in sections:
            if v['after'] in s_['items'] and k not in s_['items']:
                s_['items'].insert(s_['items'].index(v['after']) + 1, k); placed = True
        if not placed:
            for s_ in sections:
                if s_['id'] == v.get('section', 'tempore') and k not in s_['items']:
                    s_['items'].append(k)
                    if s_['id'] == 'sanctorum': s_['items'].sort(key=lambda kk: liturgical(kk))
    for k, flds in FX.get('fields', {}).items():
        if k in masses:
            for f_, val in flds.items():
                if val is None: masses[k].pop(f_, None)
                else: masses[k][f_] = val
            if flds.get('prophecies') or 'in' not in masses[k]['parts']:
                masses[k]['req'] = [x for x in (masses[k].get('req') or []) if x in masses[k]['parts']]
    for k, r in FX.get('ranks', {}).items():
        if k in masses: masses[k]['rank'] = r
    for k, n in FX.get('notes', {}).items():
        if k in masses: masses[k]['note'] = n
    for k, (la, en, mo, dy) in FX.get('titles', {}).items():
        if k in masses:
            masses[k].update(title='%d %s — %s' % (dy, MON[mo], la), en='%s %d — %s' % (MEN[mo], dy, en), name_en=en, month=mo, day=dy)
            masses[k].pop('note', None)

# ---- vestment colours from the 2026 Ordo (for the Mass the site chooses that day) ----
if os.path.exists('wins2026.json'):
    _wins = json.load(open('wins2026.json')); _col = {}
    for o in ORDO:
        if o.get('region') or not o.get('color'): continue
        k = _wins.get(o['date'])
        if not k or k not in masses: continue
        M = masses[k]
        temporal = not re.match(r'^(S\d|G\d|C\d)', k)
        ok = bool(_w(o['name']) & _w(M['title'] + ' ' + (M.get('name_en') or ''))) or (temporal and re.match(r'^(Feria|Dominica|"|DIES|Sabbat|Vigilia|In |Octava)', o['name'].strip(), re.I))
        if ok: _col.setdefault(k, set()).add(o['color'])
    # feasts whose class is unknown: take it from the Ordo of the day they are celebrated
    for o in ORDO:
        if o.get('region') or o.get('cls') not in ('I', 'II', 'III'): continue
        y_, m_, d_ = map(int, o['date'].split('-'))
        for k, M in masses.items():
            if M.get('month') == m_ - 1 and M.get('day') == d_ and not M.get('rank') and re.match(r'^(S\d|G\d)', k) and not k.endswith('b') \
               and (_w(o['name']) & _w(M['title'] + ' ' + (M.get('name_en') or ''))):
                M['rank'] = o['cls']
    for k, cs in _col.items():
        if len(cs) == 1: masses[k]['color'] = cs.pop()
    # the proper Preface of a Mass, where the Ordo's Preface for it is not simply that of the season
    import datetime as _dt
    def _easter(y):
        a=y%19;b_=y//100;c=y%100;d=b_//4;e=b_%4;f=(b_+8)//25;g=(b_-f+1)//3;h=(19*a+b_-d-g+15)%30;i=c//4;k_=c%4;l=(32+2*e+2*i-h-k_)%7;m_=(a+11*h+22*l)//451
        mo=(h+l-7*m_+114)//31; da=((h+l-7*m_+114)%31)+1; return _dt.date(y,mo,da)
    def _season(ds):
        d = _dt.date(*map(int, ds.split('-'))); f = (d - _easter(d.year)).days; md = d.month * 100 + d.day
        if md >= 1225 or md <= 105: return 'Nativitate'
        if 106 <= md <= 113: return 'Epiphania'
        if -46 <= f <= -15: return 'Quadragesima'
        if -14 <= f <= -3: return 'Sancta Cruce'
        if -1 <= f <= 38: return 'Paschalis'
        if 39 <= f <= 47: return 'Ascensione'
        if 48 <= f <= 55: return 'Spiritu Sancto'
        return None
    _pref = {}
    for o in ORDO:
        if o.get('region') or not o.get('pref'): continue
        k = _wins.get(o['date'])
        if not k or k not in masses: continue
        M = masses[k]
        if not ((_w(o['name']) & _w(M['title'] + ' ' + (M.get('name_en') or ''))) or not re.match(r'^(S\d|G\d|C\d)', k)): continue
        if o['pref'] in ('Communis', 'SS. Trinitate') or o['pref'] == _season(o['date']): continue
        _pref.setdefault(k, set()).add(o['pref'])
    for k, ps in _pref.items():
        if len(ps) == 1: masses[k]['pref'] = ps.pop()
    print('proper Prefaces from the Ordo:', sum(1 for M in masses.values() if M.get('pref')))
    print('colours from the Ordo:', sum(1 for M in masses.values() if M.get('color')))

# ---- chants used -----------------------------------------------------------------
chants = {}
for c in allchants.values():
    chants[c['id']] = {'p': ptype(c) if ptype(c) in PARTS else c['code'], 'i': c['incipit'], 'pg': c['page']}
chants.update(ROMAN_FILES)
for cid, v in (FX.get('local_chants', {}) if os.path.exists('m39_fixes.json') else {}).items():
    chants[cid] = {'p': v['p'], 'i': v['i'], 'pg': v['pg']}
# English translations of the chants (St. Dominic Missal, 1959): text and scripture reference
TRANS = {}
for cid, t in json.load(open('dm_trans.json')).items():
    t = re.sub(r"(?:\s|^)(?:Y[fIl'1]?|J[I1l]|V/|Yf|y|Y|Ji|Yl|f|1/)\.\s*(?=[A-Z0-9])", ' ℣. ', ' ' + t).strip()
    t = re.sub(r'\.\.+', '.', t).replace('.,', '.').strip(' ,')
    t = re.sub(r'(?<=[a-z])\.(?=[a-z])', ' ', t)
    t = re.sub(r'\s*(Gospel|Epistle|Lesson|Collect|Secret|Postcommunion|Prayer)[,.]\s*p\.\s*\d+\.?.*$', '', t)
    t = re.sub(r"\s+['\"`]+\s*$", '', t).strip()
    m = re.match(r'^((?:Alleluia, alleluia!\s*)?)(?:℣\.\s*)?((?:[1-4]\s?)?[A-Z][a-z]{1,7}\.?\s*\d+[,;.]\s*[\d\-,. ]*\d\.?)\s*(.*)$', t)
    ref = ''
    if m:
        ref = m.group(2).strip().rstrip('.')
        t = (m.group(1) + ('℣. ' if m.group(1) else '') + m.group(3)).strip()
    TRANS[cid] = {'t': t, 'r': ref}
# where the St. Dominic Missal has no English: the Douay-Rheims of the same verses, then our own translation
if os.path.exists('douay_trans.json'):
    for cid, v in json.load(open('douay_trans.json')).items():
        if cid not in TRANS:
            TRANS[cid] = {'t': re.sub(r'^℣\.\s*', '', v['t']), 'r': v['r'], 's': 'douay'}
if os.path.exists('manual_trans.json'):
    for cid, v in json.load(open('manual_trans.json')).items():
        if cid not in TRANS:
            TRANS[cid] = {'t': v['t'], 'r': v['r'] if not v['r'] in ('Alleluia', 'Sequence', 'Tract', 'Antiphon') else '', 's': 'own'}
for cid, v in (FX.get('local_chants', {}) if os.path.exists('m39_fixes.json') else {}).items():
    TRANS[cid] = {'t': v['t'], 'r': v['r'], 's': 'own'}
for cid, v in (FX.get('trans', {}) if os.path.exists('m39_fixes.json') else {}).items():
    TRANS[cid] = {'t': v['t'], 'r': v['r'], 's': 'douay'}
data_trans = TRANS
data = {'sections': sections, 'trans': data_trans, 'masses': masses, 'chants': chants,
        'kyriale': [c['id'] for c in kyriale], 'front': [c['id'] for c in front['chants']]}
import os
os.makedirs('site/data', exist_ok=True)
with open('site/data/masses.js', 'w', encoding='utf8') as f:
    f.write('// Generated by build_masses.py from the Graduale O.P. (1950, GregoBase source 14), the Missale O.P. (1939)\n')
    f.write('// and the Calendarium O.P. reformatum. Do not edit by hand; edit the build scripts.\n')
    f.write('var DOMINICAN = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
from collections import Counter
print({s['id']: len(s['items']) for s in sections})
print('sanctorale conf', Counter(masses[k]['conf'] for k in sitems + bitems))
print('with seasonal variants', sum(1 for k in sitems+bitems if masses[k].get('season')))
print('temporale inferred parts', sum(1 for k in items for p in masses[k]['parts'].values() for c in p if c.get('inferred')))
