"""Complete every Mass with the St. Dominic Missal (1959): chants it assigns and its Epistle/Gospel references.

Called by build_masses.py before data/masses.js is written.
"""
import json, re, difflib, unicodedata, os

PARTS = ['in', 'gr', 'al', 'tr', 'se', 'of', 'co']
# The Commons of the Missal (its Part III), by the incipit of their Introit -> page of that Mass in the Graduale
COMMON_INTROIT = {1: '7*', 2: '11*', 3: '15*', 4: '7*', 5: '18*', 6: '15*', 7: '21*', 8: '25*', 9: '28*', 10: '30*',
                  11: '32*', 12: '35*', 13: '39*', 14: '42*', 15: '42*', 16: '45*', 17: '48*', 18: '51*', 19: '55*',
                  20: '48*', 21: '48*', 22: '51*'}
BOOKS = {
    'matt': 'Matthæus', 'mt': 'Matthæus', 'mark': 'Marcus', 'mk': 'Marcus', 'luke': 'Lucas', 'lk': 'Lucas', 'luk': 'Lucas', 'lu': 'Lucas',
    'john': 'Joannes', 'joh': 'Joannes', 'jn': 'Joannes', 'acts': 'Actus Apostolorum', 'rom': 'Ad Romanos', 'kom': 'Ad Romanos',
    '1cor': 'Ad Corinthios 1', '1car': 'Ad Corinthios 1', '2cor': 'Ad Corinthios 2', '2car': 'Ad Corinthios 2',
    'gal': 'Ad Galatas', 'eph': 'Ad Ephesios', 'phil': 'Ad Philippenses', 'col': 'Ad Colossenses',
    '1thess': 'Ad Thessalonicenses 1', '2thess': 'Ad Thessalonicenses 2', '1tim': 'Ad Timotheum 1', '2tim': 'Ad Timotheum 2',
    'titus': 'Ad Titum', 'tit': 'Ad Titum', 'philem': 'Ad Philemonem', 'heb': 'Ad Hebræos', 'james': 'Jacobi', 'jas': 'Jacobi',
    '1pet': 'Petri 1', '2pet': 'Petri 2', '1john': 'Joannis 1', '2john': 'Joannis 2', '3john': 'Joannis 3', 'jude': 'Judæ',
    'apoc': 'Apocalypsis', 'rev': 'Apocalypsis', 'gen': 'Genesis', 'ex': 'Exodus', 'exod': 'Exodus', 'lev': 'Leviticus',
    'num': 'Numeri', 'nu': 'Numeri', 'deut': 'Deuteronomium', 'jos': 'Josue', 'josh': 'Josue', 'judg': 'Judicum', 'ruth': 'Ruth',
    '1kgs': 'Regum 1', '2kgs': 'Regum 2', '3kgs': 'Regum 3', '4kgs': 'Regum 4', '1kings': 'Regum 1', '2kings': 'Regum 2',
    '3kings': 'Regum 3', '4kings': 'Regum 4', '1par': 'Paralipomenon 1', '2par': 'Paralipomenon 2', '1esd': 'Esdræ',
    '2esd': 'Nehemiæ', 'tob': 'Tobiæ', 'judith': 'Judith', 'esther': 'Esther', 'esth': 'Esther', 'job': 'Job', 'ps': 'Psalmi',
    'prov': 'Proverbia', 'eccl': 'Ecclesiastes', 'eccles': 'Ecclesiastes', 'cant': 'Canticum Canticorum',
    'wisd': 'Sapientia', 'wis': 'Sapientia', 'ecclus': 'Ecclesiasticus', 'sir': 'Ecclesiasticus', 'isa': 'Isaias',
    'isaias': 'Isaias', 'is': 'Isaias', 'jer': 'Jeremias', 'lam': 'Lamentationes', 'bar': 'Baruch', 'ezech': 'Ezechiel',
    'ez': 'Ezechiel', 'dan': 'Daniel', 'osee': 'Osee', 'joel': 'Joel', 'amos': 'Amos', 'abd': 'Abdias', 'jon': 'Jonas',
    'mich': 'Michæa', 'nah': 'Nahum', 'hab': 'Habacuc', 'soph': 'Sophonias', 'agg': 'Aggæus', 'zach': 'Zacharias',
    'mal': 'Malachias', '1mach': 'Machabæorum 1', '2mach': 'Machabæorum 2',
}


def book(b):
    k = re.sub(r'[^a-z0-9]', '', b.lower())
    if k in BOOKS:
        return BOOKS[k]
    best = difflib.get_close_matches(k, list(BOOKS), n=1, cutoff=0.75)
    return BOOKS[best[0]] if best else None


def clean_ref(r):
    """'13,11-14' -> '13: 11-14'; '14,22;15,3-4' -> '14: 22; 15: 3-4' (the form jgabc's lectiones use)."""
    r = r.replace('–', '-').strip(' .,;')
    parts = []
    for seg in r.split(';'):
        seg = seg.strip()
        m = re.match(r'^(\d+)[,.](.+)$', seg)
        if m:
            parts.append('%s: %s' % (m.group(1), m.group(2).strip()))
        elif parts and re.match(r'^[\d\-, ]+$', seg):
            parts.append(seg)
    return '; '.join(parts)


def flat(s):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('J', 'i')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z]', '', s)


def merge(masses, sections, groups, allchants, core, roman_lectiones, jgabc_dir, out_gabc_dir):
    D = json.load(open('dm_masses.json'))
    dm = D['masses']
    bypage = {}
    for i, m in enumerate(dm):
        for p in m['pages']:
            bypage.setdefault(p, i)
    common_dm = {int(m['key'][2:]): m for m in dm if m['kind'] == 'common'}
    gpage = {g['page']: g for g in groups}

    # ---- readings ------------------------------------------------------------------------------
    def readings_of(m, depth=0):
        out = []
        for r in m['readings']:
            if 'page' in r:
                if depth > 2:
                    continue
                # "Gospel, p. 75": the reading of that type printed on that page
                for pg in (r['page'], r['page'] - 1, r['page'] + 1):
                    j = bypage.get(pg)
                    if j is None:
                        continue
                    src = [x for x in readings_of(dm[j], depth + 1) if x['type'] == r['type'] or (r['type'] == 'Epistle' and x['type'] == 'Lesson')]
                    if src:
                        out.append(dict(src[-1] if r['type'] == 'Gospel' else src[0], type=r['type']))
                        break
            else:
                b = book(r['book'])
                ref = clean_ref(r['ref'])
                if b and ref:
                    out.append({'type': r['type'], 'ref': '%s %s' % (b, ref)})
        return out

    def complete_readings(m):
        rs = readings_of(m)
        types = {r['type'] for r in rs}
        if m.get('ref') and common_dm.get(m['ref']):
            for r in readings_of(common_dm[m['ref']]):
                t = 'Epistle' if r['type'] == 'Lesson' else r['type']
                if t == 'Gospel' and 'Gospel' not in types or t == 'Epistle' and not types & {'Epistle', 'Lesson'}:
                    rs.append(r); types.add(t)
        if m.get('refpage') and bypage.get(m['refpage']) is not None:
            for r in readings_of(dm[bypage[m['refpage']]]):
                t = 'Epistle' if r['type'] == 'Lesson' else r['type']
                if t == 'Gospel' and 'Gospel' not in types or t == 'Epistle' and not types & {'Epistle', 'Lesson'}:
                    rs.append(r); types.add(t)
        # Epistle/Lessons first, then the Gospel
        order = {'Lesson': 0, 'Epistle': 1, 'Gospel': 2}
        seen, res = set(), []
        for r in sorted(rs, key=lambda r: order[r['type']]):
            if r['ref'] not in seen:
                res.append(r); seen.add(r['ref'])
        return res

    def common_parts(n):
        """Chants of Common No. n: the Missal's assignment over the Graduale's printed Common."""
        g = gpage.get(COMMON_INTROIT.get(n))
        parts = {}
        if g:
            taken, _ = core(g)
            parts = {p: [c['id'] for c in v] for p, v in taken.items()}
        m = common_dm.get(n)
        if m:
            for p, ids in m['parts'].items():
                parts[p] = ids[:1] if p != 'gr' else ids[:1]
        return parts

    def as_parts(d):
        return {p: [{'id': i} for i in v] for p, v in d.items() if v}

    stats = {'tempore_matched': 0, 'saints_matched': 0}
    # ---- Temporale: align by Introit -----------------------------------------------------------------
    temp = next(s for s in sections if s['id'] == 'tempore')['items']
    dmt = [m for m in dm if m['kind'] == 'tempore' and m['parts'].get('in')]
    ptr = 0
    for key in temp:
        M = masses[key]
        intro = (M['parts'].get('in') or [{}])[0].get('id')
        if intro is None:
            continue
        inc = flat(allchants[intro]['incipit'])[:12]
        hit = None
        for j in range(ptr, min(ptr + 8, len(dmt))):
            ids = dmt[j]['parts']['in']
            if intro in ids or any(flat(allchants[i]['incipit'])[:12] == inc for i in ids if i in allchants):
                hit = j; break
        if hit is None:
            continue
        ptr = hit + 1
        d = dmt[hit]
        stats['tempore_matched'] += 1
        for p, ids in d['parts'].items():
            if p == 'in':
                continue
            cur = M['parts'].get(p, [])
            if not cur or all(c.get('inferred') for c in cur):
                M['parts'][p] = [{'id': i, 'dm': True} for i in ids[: (5 if p == 'gr' else 2 if p == 'al' else 1)]]
        rs = complete_readings(d)
        if rs:
            M['readings'] = rs
    for key in temp:  # the Roman lectionary of jgabc where the Missal was not read
        M = masses[key]
        if not M.get('readings') and roman_lectiones.get(key):
            M['readings'] = [{'type': 'Gospel' if i == len(roman_lectiones[key]) - 1 else ('Epistle' if i == len(roman_lectiones[key]) - 2 else 'Lesson'),
                              'ref': r, 'roman': True} for i, r in enumerate(roman_lectiones[key])]

    # ---- Saints ----------------------------------------------------------------------------------
    def words(s):
        s = flat(s.replace(' ', '_')) if False else s
        return set(w[:5] for w in re.findall(r'[a-z]{4,}', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))))
    for sec in ('sanctorum', 'beati'):
        for key in next(s for s in sections if s['id'] == sec)['items']:
            M = masses[key]
            if 'month' not in M or M['month'] > 11:
                continue
            k = '%02d%02d' % (M['month'] + 1, M['day'])
            cands = [m for m in dm if m['kind'] == 'saint' and m['key'] == k]
            if not cands:
                continue
            name = words(M['en'].split('—')[-1])
            cands.sort(key=lambda m: (-len(words(m['title']) & name), -len(m['parts']) - (1 if m['ref'] else 0)))
            d = cands[0]
            if not (words(d['title']) & name) and len(cands) > 1:
                continue
            stats['saints_matched'] += 1
            parts = {}
            if d.get('ref'):
                parts.update(common_parts(d['ref']))
            elif d.get('refpage') and bypage.get(d['refpage']) is not None:
                src = dm[bypage[d['refpage']]]
                parts.update({p: v[:1] for p, v in src['parts'].items()})
            for p, ids in d['parts'].items():
                parts[p] = ids[:1]
            if parts.get('in'):
                old = {p: v for p, v in M['parts'].items()}
                newp = as_parts(parts)
                for p in PARTS:  # keep what the Graduale/1939 Missal gave for any part the 1959 Missal is silent on
                    if p not in newp and old.get(p) and p != 'tr':
                        newp[p] = old[p]
                M['parts'] = newp
                M['conf'] = 'dm'
                M['note'] = 'Chants as assigned by the St. Dominic Missal (1959)' + (', Common No. %d' % d['ref'] if d.get('ref') else '') + '.'
            elif d.get('ref'):
                M['parts'] = as_parts(common_parts(d['ref']))
                M['conf'] = 'dm'
                M['note'] = 'Common No. %d of the St. Dominic Missal (1959).' % d['ref']
            # seasons
            season = M.get('season') or {}
            if d['season'].get('pasch'):
                season.setdefault('pasch', {})['al'] = [{'id': i} for i in d['season']['pasch']['al'][:2]]
            if d.get('refPasch'):
                cp = common_parts(d['refPasch'])
                if cp.get('al'):
                    season.setdefault('pasch', {})['al'] = [{'id': i} for i in (common_dm.get(d['refPasch'], {}).get('parts', {}).get('al') or cp['al'])[:2]]
            if 'tr' in M['parts'] and M['parts'].get('al'):
                season.setdefault('lent', {})['tr'] = M['parts'].pop('tr')
            M['season'] = season
            rs = complete_readings(d)
            if rs:
                M['readings'] = rs

    # ---- Commons of the site: readings from the Missal's Commons --------------------------------------
    for key in next(s for s in sections if s['id'] == 'commune')['items']:
        M = masses[key]
        for n, pg in COMMON_INTROIT.items():
            if pg == M['page'] and common_dm.get(n):
                rs = complete_readings(common_dm[n])
                if rs:
                    M['readings'] = rs
                    break
    return stats
