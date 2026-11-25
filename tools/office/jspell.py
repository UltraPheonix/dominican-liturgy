"""Pre-1955 spelling in the Office: consonantal i written j, as in the Breviarium and Completorium O.P. before 1955
(Divinum Officium's 1962 text writes Iesus, eius, adiutorium). The j-words are taken from the Vulgate in bible/la.
Run from the repo root: python3 tools/office/jspell.py"""
import json, re, glob, unicodedata
def plain(c): return unicodedata.normalize('NFD', c)[0].lower()
def key(w): return ''.join('i' if plain(c) == 'j' else plain(c) for c in w)
J, I = {}, set()
for f in glob.glob('bible/la/*.txt'):
    for w in re.findall(r"[^\W\d_]+", open(f, encoding='utf-8').read()):
        k = key(w)
        if 'j' in w.lower(): J[k] = ''.join(plain(c) for c in w)
        else: I.add(k)
EXCL = {'alleluia'}
J = {k: v for k, v in J.items() if k not in EXCL and k not in I}
def fix(w):
    k = key(w); v = J.get(k)
    if not v: return w
    return ''.join(('J' if c.isupper() else 'j') if v[i] == 'j' and plain(c) == 'i' else c for i, c in enumerate(w))
def fixtext(s): return re.sub(r"[^\W\d_]+", lambda m: fix(m.group()), s)
n = 0
def walk(x):
    global n
    if isinstance(x, str):
        y = fixtext(x); n += y != x; return y
    if isinstance(x, list): return [walk(v) for v in x]
    if isinstance(x, dict): return {k: walk(v) for k, v in x.items()}
    return x
files = ['data/office/common.json'] + glob.glob('data/office/psalter/*.json') + glob.glob('data/office/20*/*.json')
for f in files:
    d = json.load(open(f, encoding='utf-8'))
    if f.endswith('common.json') or '/psalter/' in f: d2 = walk(d)
    else:
        d2 = dict(d)
        if 'b' in d: d2['b'] = walk(d['b'])
        if 't' in d: d2['t'] = walk(d['t'])
        if 'tv' in d: d2['tv'] = walk(d['tv'])
    if d2 != d:
        raw = open(f, encoding='utf-8').read()
        sep = (',', ':') if '":"' in raw[:200] or '":[' in raw[:200] or '":{' in raw[:200] else None
        json.dump(d2, open(f, 'w', encoding='utf-8'), ensure_ascii=False, separators=sep)
print(n, 'strings changed in', len(files), 'files;', len(J), 'j-words')
