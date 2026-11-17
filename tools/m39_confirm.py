"""Confirm each reading by finding a middle verse of it in the Missale O.P. 1939 shortly after the Mass's Introit."""
import re, json, sys, unicodedata
sys.path.insert(0, '/tmp')
from adj import F, flat
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
BIB = {}
def book(b):
    if b not in BIB:
        v = {}
        try:
            for l in open('site/bible/la/%s.txt' % b, encoding='utf8'):
                c, n, t = l.rstrip('\n').split('\t', 2); v[(int(c), int(n))] = t
        except FileNotFoundError: pass
        BIB[b] = v
    return BIB[b]
def parse(ref):
    m = re.match(r'^(\d)?\s*([^\d:]+?)(?:\s+(\d))?\s+(\d+):\s*(.+)$', ref.strip())
    if not m: return None, []
    bk = m.group(2).strip() + (' ' + m.group(1) if m.group(1) else (' ' + m.group(3) if m.group(3) else ''))
    ch = int(m.group(4)); out = []
    for seg in m.group(5).split(';'):
        seg = seg.strip(); c = re.match(r'^(\d+):\s*(.*)$', seg)
        if c: ch = int(c.group(1)); seg = c.group(2)
        for r in seg.split(','):
            x = re.match(r'^(\d+)[a-c]?(?:\s*-\s*(?:(\d+):)?(\d+)[a-c]?)?$', r.strip())
            if not x: continue
            a = int(x.group(1)); ch2 = int(x.group(2)) if x.group(2) else ch; b = int(x.group(3)) if x.group(3) else a
            out.append((ch, a, ch2, b)); ch = ch2
    return bk, out
def verses(bk, rng):
    V = book(bk); out = []
    for c1, a, c2, b in rng:
        for c in range(c1, c2 + 1):
            for n in range(a if c == c1 else 1, (b if c == c2 else 200) + 1):
                if (c, n) in V: out.append(((c, n), V[(c, n)]))
    return out
def gtext(i):
    try: t = open('site/gabc/%s.gabc' % i, encoding='utf8').read().split('%%', 1)[1]
    except Exception: return ''
    return flat(re.sub(r'<[^>]*>', '', re.sub(r'\([^)]*\)', '', t)))
def anchors(M):
    out = set()
    for x in M['parts'].get('in', [])[:1]:
        t = gtext(x['id'])
        for o in (2, 14, 26):
            k = t[o:o + 12]
            if len(k) == 12:
                out |= {m.start() - o for m in re.finditer(re.escape(k), F)}
    return sorted(out)
res = {'ok': [], 'bad': [], 'noanchor': [], 'nobook': []}
for k, M in D['masses'].items():
    A = anchors(M)
    for r in M.get('readings', []):
        bk, rng = parse(r['ref'])
        vs = verses(bk, rng) if bk else []
        if not vs: res['nobook'].append((k, r['ref'])); continue
        if not A: res['noanchor'].append((k, r['ref'])); continue
        step = max(1, len(vs) // 8)
        probes = []
        for (cv, t) in vs[::step][:10]:
            f = flat(t)
            for o in (4, 20, 36):
                if len(f) >= o + 13: probes.append(f[o:o + 13])
        need = 2 if len(probes) >= 3 else 1
        hit = any(sum(1 for p in probes if F.find(p, a, a + 16000) > 0) >= need for a in A)
        (res['ok'] if hit else res['bad']).append((k, r['ref'], r.get('roman', False)))
json.dump(res, open('m39_confirm.json', 'w'), ensure_ascii=False, indent=0)
for x in res: print(x, len(res[x]))
print('roman ok', sum(1 for x in res['ok'] if x[2]), 'roman bad', sum(1 for x in res['bad'] if x[2]))
for x in res['nobook']: print('NOBOOK', x)
