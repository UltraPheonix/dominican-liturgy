"""For every 2026 day, read the Mass on its Missal page (from the Ordo) and compare its readings with the site's."""
import re, json, sys, io
sys.path.insert(0, '/tmp')
_o = sys.stdout; sys.stdout = io.StringIO()
import resolve_m39 as R
import m39_confirm as C
import m39_fixreadings as X
sys.stdout = _o
from adj import flat
PG = {}
def pflat(n):
    if n not in PG:
        try: T = open('/home/claude/dl/m39cols/%d.txt' % n).read()
        except FileNotFoundError: T = ''
        T = re.sub(r'(?m) [A-Z]$', '', T)
        PG[n] = re.sub(r'[0-9]', '', flat(re.sub(r'[­-]\s*\n', '', T)))
    return PG[n]
ordo = json.load(open('ordo2026.json')); wins = json.load(open('wins2026.json'))
def w(s):
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c)).replace('j', 'i').replace('æ', 'ae')
    return set(x[:6] for x in re.findall(r'[a-z]{4,}', s)) - {'sancti', 'sancta', 'beati', 'missa', 'domini', 'confes', 'virgin', 'episco', 'martyr', 'ordini', 'praedi'}
out = {}; seen = set()
for o in ordo:
    if o['region'] or not o.get('m39'): continue
    k = wins.get(o['date'])
    if not k or k in seen: continue
    M = C.D['masses'].get(k)
    if not M or not M.get('readings'): continue
    t = (M.get('title') or '') + ' ' + (M.get('en') or '') + ' ' + (M.get('name_en') or '')
    if not (w(o['name']) & w(t)) and k[0] in 'SG': continue
    p = R.pdf_page(o['m39'])
    if not p: continue
    win = pflat(p - 1) + pflat(p) + pflat(p + 1) + pflat(p + 2)
    off = len(pflat(p - 1))
    intro = C.gtext((M['parts'].get('in') or [{}])[0].get('id'))
    A = sorted({m.start() - oo for oo in (2, 14, 26) if len(intro) > oo + 12 for m in re.finditer(re.escape(intro[oo:oo + 12]), win)})
    A = [a for a in A if a >= off - 3000]
    if not A: continue
    a = A[0]
    seg = win[a: a + 14000]
    seen.add(k)
    res = []
    for r in M['readings']:
        bk, rng = C.parse(r['ref']); vs = C.verses(bk, rng) if bk else []
        probes = [flat(tt)[oo:oo + 13] for cv, tt in vs[::max(1, len(vs) // 8)][:10] for oo in (4, 20, 36) if len(flat(tt)) >= oo + 13]
        n = sum(1 for pr in probes if pr in seg)
        res.append((r['ref'], n, len(probes)))
    # the Missal's own readings after the Introit
    X.F = seg
    found = []
    for typ, pos, body in X.readings_after(0):
        l = X.locate(body)
        if l: found.append((typ, X.fmt(*l[:5]), l[5]))
    out[k] = {'date': o['date'], 'name': o['name'], 'page': o['m39'], 'ours': res, 'missal': found}
json.dump(out, open('m39_pagefix.json', 'w'), ensure_ascii=False, indent=1)
bad = {k: v for k, v in out.items() if any(n < max(1, min(2, tot)) for _, n, tot in v['ours'])}
print('checked', len(out), 'with unconfirmed readings', len(bad))
for k, v in bad.items():
    print(k, v['date'], v['name'][:36], 'p.' + v['page']); print('    ours  :', v['ours']); print('    missal:', v['missal'])
