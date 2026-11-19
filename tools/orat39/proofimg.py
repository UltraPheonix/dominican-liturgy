"""Proof images: crop each Mass's Collect, Secret and Postcommunion from the Missale O.P. 1939 PDF.
Usage: python3 proofimg.py /path/to/M39.pdf [KEY ...]  -> proof/<KEY>.png (+ proof/where.json)"""
import sys, os, re, json, unicodedata
import pymupdf as fitz
PDF = sys.argv[1]
d = fitz.open(PDF)
def L(s):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('Œ', 'oe')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower().replace('j', 'i'))
# reading-order stream of text blocks (same column logic as lin.py)
BL = []; S = ''; OFF = []
for i in range(len(d)):
    pg = d[i]; W = pg.rect.width
    cols = {}
    for b in pg.get_text('blocks'):
        if b[6] != 0: continue
        k = min(range(4), key=lambda c: abs(b[0] - [42, 212, 455, 623][c] * W / 800))
        cols.setdefault(k, []).append(b)
    for k in sorted(cols):
        for b in sorted(cols[k], key=lambda b: (round(b[1]), b[0])):
            OFF.append(len(S)); BL.append((i, k, fitz.Rect(b[:4]))); S += L(b[4])
import bisect
def blk(o): return bisect.bisect_right(OFF, o) - 1
import difflib
def find(raw, near=None, lo=0, hi=None):
    """all places where the prayer's opening occurs; keep the one most like the whole prayer (names included),
    preferring one just after the Collect (near)."""
    body = re.split(r'\b(Per Dominum|Per eumdem|Qui vivis|Qui tecum)', raw)[0]
    f = L(body)
    cands = set()
    for n, sk in ((30, 0), (20, 5), (15, 12)):
        q = f[sk:sk + n]; i = S.find(q)
        while i >= 0 and len(cands) < 400:
            cands.add(i - sk); i = S.find(q, i + 1)
    if hi is not None: cands = {a for a in cands if lo <= a < hi}
    best = None
    for a in cands:
        r = difflib.SequenceMatcher(None, S[a:a + len(f) + 20], f, autojunk=False).ratio()
        if near is not None and 0 <= a - near < 25000: r += 0.02
        if not best or r > best[0]: best = (r, a)
    if not best or best[0] < 0.6: return None
    a = best[1]
    for m in (25, 15, 10):
        e = S.find(f[-m:], a, a + len(f) + 400)
        if e >= 0: return a, e + m
    return a, a + len(f)
M = json.load(open(os.path.join(os.path.dirname(__file__) or '.', 'matched.json')))
M.update(json.load(open(os.path.join(os.path.dirname(__file__) or '.', 'manual_match.json'))))
# the pdf page where each Mass begins (from its line in m39lin.txt)
LIN = open('m39lin.txt').read().split('\n'); PG = []; cur = 0
for l in LIN:
    if l.startswith('@@PAGE '): cur = int(l.split()[1])
    PG.append(cur)
POFF = {}
for j, (p, c, rc) in enumerate(BL): POFF.setdefault(p, OFF[j])
def poff(p): return POFF.get(p, len(S))
keys = sys.argv[2:] or list(M)
os.makedirs('proof', exist_ok=True)
where = {}
OUTSIDE = []
for k in keys:
    m = M[k]
    if not (len(m['pr']) == 3 and all(m['pr'].values())): continue
    if k in ('S0508b', 'S1119b', 'G481'): continue
    crops = []; w = {}; near = None
    p0 = PG[m['start']] if m.get('start') is not None else None
    for kind in ('or', 'se', 'pc'):
        r = find(m['pr'][kind], near, poff(p0), poff(p0 + 3)) if p0 is not None else None
        if not r:
            r = find(m['pr'][kind], near); OUTSIDE.append((k, kind, p0, r and blk(r[0]) and BL[blk(r[0])][0]))
        if r and kind == 'or': near = r[0]
        if not r: w[kind] = None; continue
        b0, b1 = blk(r[0]), blk(r[1] - 1)
        w[kind] = [BL[b0][0], BL[b1][0]]
        reg = {}
        for j in range(b0, b1 + 1):
            p, c, rc = BL[j]
            reg.setdefault((p, c), fitz.Rect(rc)).include_rect(rc)
        for (p, c), rc in reg.items():
            rc = fitz.Rect(rc.x0 - 4, rc.y0 - 3, rc.x1 + 4, rc.y1 + 3) & d[p].rect
            crops.append(d[p].get_pixmap(clip=rc, dpi=200))
    where[k] = w
    if not crops: continue
    Wd = max(c.width for c in crops); H = sum(c.height + 12 for c in crops)
    out = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, Wd, H), False); out.set_rect(out.irect, (255, 255, 255))
    y = 0
    for c in crops:
        if c.n != 3: c = fitz.Pixmap(fitz.csRGB, c)
        c.set_origin(0, y); out.copy(c, c.irect); y += c.height + 12
    out.save('proof/%s.png' % k)
W0 = json.load(open('proof/where.json')) if os.path.exists('proof/where.json') else {}
W0.update(where); json.dump(W0, open('proof/where.json', 'w'), indent=0)
json.dump(OUTSIDE, open('proof/outside.json', 'w'))
print('found only outside the Mass pages:', OUTSIDE)
print(len(where), 'Masses;', sum(1 for w in where.values() for v in w.values() if v is None), 'prayers not located')
