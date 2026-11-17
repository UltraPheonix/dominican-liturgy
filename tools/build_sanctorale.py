"""Link each feast of the Dominican calendar to a Mass in the Graduale O.P.

1. calendar.json (from the Calendarium O.P. reformatum) gives date, name and rank.
2. The Missale O.P. 1939 text for that date says whether the Introit is proper or taken from a
   Common ("Officium Os justi, ut in Communi ...").  A proper Introit is found by searching the
   date's text for the Introit incipit of each Sanctorale Mass in the Graduale.
3. Otherwise the Common is taken from the "Officium ..." reference, or, failing that, guessed from
   the saint's title (C., E. C., V. M., ...), and marked as a guess.
Output: sanctorale.json
"""
import gzip
import json, re, difflib, sys, io
_stdout = sys.stdout; sys.stdout = io.StringIO()
from build_temporale import norm, same, groups
sys.stdout = _stdout

lines = gzip.open('sources/missale_op_1939_ocr.txt.gz', 'rt', encoding='utf8').read().split('\n')
cal = json.load(open('calendar.json'))
MONTHS = ['Januarii', 'Februarii', 'Martii', 'Aprilis', 'Maii', 'Junii', 'Julii', 'Augusti', 'Septembris',
          'Octobris', 'Novembris', 'Decembris']
HEAD = re.compile(r'^D ?i ?e\s+((?:\d\s?){1,2})\s+([A-Za-z ]{4,16}?)\s*(?:[.—\-]|$)')


def letters(s):
    return re.sub(r'[^a-z]', '', norm(s))


def month_of(s):
    s = s.replace(' ', '').lower()
    r = [difflib.SequenceMatcher(None, s, m.lower()).ratio() for m in MONTHS]
    b = max(range(12), key=lambda i: r[i])
    return b if r[b] > 0.7 else None


# ---- Missal text by date ---------------------------------------------------------
heads = []
for i, l in enumerate(lines):
    if 40000 <= i <= 73000:
        m = HEAD.match(l.strip())
        if m:
            mon = month_of(m.group(2))
            day = int(m.group(1).replace(' ', ''))
            if mon is not None and 1 <= day <= 31:
                heads.append((i, day, mon))
bydate = {}
for k, (i, day, mon) in enumerate(heads):
    end = heads[k + 1][0] if k + 1 < len(heads) else i + 300
    bydate.setdefault((mon, day), []).append('\n'.join(lines[i:end]))

sanct = [g for g in groups if g['section'] == 'sanctorum']
commons = [g for g in groups if g['section'] in ('commune', 'votivae')]
probe = {g['gid']: letters(g['introit'])[1:13] for g in sanct}


def find_common(ref):
    for pool in (commons, groups):
        c = [g for g in pool if same(g['introit'], ref, 2)]
        if c:
            return c[0]
    c = [g for g in commons if same(g['introit'], ref, 1)]
    return c[0] if c else None


# Common by the saint's title, following the arrangement of the Missale O.P.
GUESS = [
    (r'\bApost', 'Mihi autem nimis'), (r'\bEvang', 'Mihi autem nimis'),
    (r'\bMm\.|Martyrum', 'Intret in conspectu'),
    (r'\bV\.\s*M\.|Virg\. et Mart', 'Loquebar'),
    (r'\bE\.\s*M\.|Ep\. et Mart|P\.\s*M\.', 'Sacerdotes Dei'),
    (r'\bM\.', 'Laetabitur justus'),
    (r'\bD\.$|\bD\.,|Doct', 'In medio Ecclesiae'),
    (r'\bE\.\s*C\.|P\.\s*C\.|Ep\. et Conf', 'Statuit'),
    (r'\bAbb', 'Os justi'),
    (r'\bVid\.|\bMat\.|Matron', 'Gaudeamus... beatae N.'),
    (r'\bV\.', 'Dilexisti'),
    (r'\bC\.|Conf', 'Os justi'),
]

used = set()
out = []
for f in cal:
    texts = bydate.get((f['month'], f['day']), [])
    txt = '\n'.join(texts)
    flat = letters(txt)
    rec = dict(f)
    # proper Mass?
    hits = [g for g in sanct if len(probe[g['gid']]) >= 8 and probe[g['gid']] in flat]
    hits = [g for g in hits if g['gid'] not in used] or hits
    ref = None
    for t in texts:
        m = re.search(r'Officium\s+([A-Z][^,\n]{2,40}?),?\s+(?:ut\s+in\s+Comm|in\s+Comm|de\s+Comm|ut\s+supra)', t)
        if m:
            ref = m.group(1).strip()
            break
    if hits and not (ref and f['rank'] == 'III' and not hits):
        g = hits[0]
        rec.update(gid=g['gid'], conf='proper')
        used.add(g['gid'])
    elif ref and find_common(ref):
        rec.update(gid=find_common(ref)['gid'], conf='common', ref=ref)
    else:
        for pat, inc in GUESS:
            if re.search(pat, f['name']):
                g = find_common(inc)
                if g:
                    rec.update(gid=g['gid'], conf='guess', ref=inc)
                break
    out.append(rec)

unlinked = [g for g in sanct if g['gid'] not in used]
json.dump({'feasts': out, 'unlinked': [g['gid'] for g in unlinked]}, open('sanctorale.json', 'w'), ensure_ascii=False, indent=0)
from collections import Counter
print(Counter(r.get('conf', 'none') for r in out))
for r in out:
    if not r['beatus'] and r.get('conf') in ('proper', None):
        g = groups[r['gid']] if r.get('gid') is not None else None
        print('%2d/%2d %-7s %-45s %s' % (r['month'] + 1, r['day'], r.get('conf'), r['name'][:45], ('p.%s %s' % (g['page'], g['introit'])) if g else ''))
print('UNLINKED graduale masses:', ['p.%s %s' % (g['page'], g['introit']) for g in unlinked])
