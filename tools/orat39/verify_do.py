"""Check the orations taken from Divinum Officium (src not 'Missale O.P.') against the Missale O.P. 1939 text layer (m39lin.txt).
For each prayer: find the Missal passage starting like it (OCR-tolerant) and compare the body (conclusion cut).
Output: /tmp/vdo.json {key: {kind: [ratio, m39_line, missal_snippet, site_snippet]}} and a summary."""
import json, re, unicodedata, difflib, bisect, sys
def F(s):
    s = s.replace('æ', 'ae').replace('œ', 'oe').replace('Æ', 'ae').replace('Œ', 'oe').replace('ǽ', 'ae')
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.lower().replace('j', 'i').replace('v', 'u'))
L = open('m39lin.txt').read().split('\n')
S = ''; OFF = []; LN = []
for i, l in enumerate(L):
    if l.startswith('@@PAGE'): continue
    t = l.rstrip()
    t = t[:-1] if t.endswith('­') else t
    f = F(t); OFF.append(len(S)); LN.append(i + 1); S += f
def line_of(off): return LN[max(0, bisect.bisect_right(OFF, off) - 1)]
CONC = re.compile(r'(Per (eúndem |eúmdem )?Dóminum|Per Dominum|Qui vivis|Qui tecum|qui tecum|Qui vivit|Per eúndem|Per eumdem|Per Christum|Qui cum Patre)')
def body(t):
    m = CONC.search(t)
    return t[:m.start()] if m else t
def find(f):
    cands = set()
    for n, sk in ((24, 0), (18, 6), (16, 14), (16, 30)):
        q = f[sk:sk + n]
        if len(q) < n: continue
        i = S.find(q)
        while i >= 0 and len(cands) < 300:
            cands.add(i - sk); i = S.find(q, i + 1)
    best = (0, None)
    for a in cands:
        if a < 0: continue
        r = difflib.SequenceMatcher(None, S[a:a + len(f)], f, autojunk=False).ratio()
        if r > best[0]: best = (r, a)
    return best
o = open('../../data/orations.js').read(); O = json.loads(o[o.index('{'):].rstrip().rstrip(';'))
out = {}
for k, v in O.items():
    if v.get('src', '').startswith('Missale'): continue
    out[k] = {}
    for kind in ('or', 'se', 'pc'):
        if kind not in v: continue
        f = F(body(v[kind][0]))
        r, a = find(f)
        if a is None: out[k][kind] = [0, None, '', f[:60]]; continue
        # extend/trim the Missal window to the best length
        out[k][kind] = [round(r, 3), line_of(a), S[a:a + len(f)][:90], f[:90]]
json.dump(out, open('/tmp/vdo.json', 'w'), indent=0)
rs = [x[0] for v in out.values() for x in v.values()]
for th in (0.97, 0.93, 0.85, 0.7):
    print(th, sum(1 for r in rs if r >= th), '/', len(rs))
