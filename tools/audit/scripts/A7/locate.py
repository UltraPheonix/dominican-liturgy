#!/usr/bin/env python3
"""locate.py [N...]: for each copy of Commune reading N, is the text printed at the Mass's own M39 page (text layer), and
which 'pag. N*' references stand on that page. -> /tmp/A7/locate.json"""
import sys, json, re
from lib import *
T = open('/home/claude/dominican-liturgy/tools/orat39/m39lin.txt', encoding='utf8').read()
P = {}
for m in re.finditer(r'@@PAGE (\d+)\n(.*?)(?=@@PAGE|\Z)', T, re.S): P[int(m.group(1))] = re.sub(r'­\s*', '', m.group(2))
C = json.load(open('/tmp/A7/comm_readings.json')); CL = json.load(open('/tmp/A7/clusters.json')); r = R()
O = json.load(open(ST + 'orations.json'))
PN = json.load(open('/home/claude/dominican-liturgy/tools/audit/scripts/A5/pnums.json'))
P2 = {}
for kk, v in PN.items():
    for x in v: P2.setdefault(x, int(kk))
def p2pdf(p):
    p = str(p); n = int(p.rstrip('*')); st = '*' if p.endswith('*') else ''
    if p in P2: return P2[p]
    for d in range(1, 6):
        for q in (n - d, n + d):
            if str(q) + st in P2: return P2[str(q) + st] + (n // 2 - q // 2)
def pg(k):
    s = O.get(k, {}).get('src', '') if isinstance(O.get(k), dict) else ''
    m = re.search(r'p\. (\d+)', s)
    if not m or 'Missale O.P. (1939)' not in s: return None
    return p2pdf(m.group(1)) - 1     # @@PAGE number
ns = [int(x) for x in sys.argv[1:]] or sorted({x['c'] for x in CL})
out = {}
for n in ns:
    print('##', n, C[n]['page'], C[n]['head'][:50])
    for x in CL:
        if x['c'] != n or x['key'].startswith('C') or x['key'] in ('Dedicatio',): continue
        k = x['key']; p = pg(k); la = r[k][x['i']]['la']
        w = norm(la)[6:14]
        found = []
        for q in ([p - 1, p, p + 1, p + 2] if p else []):
            if q in P and q not in range(367, 389) and q != C[n]['page']:
                t = ' '.join(norm(P[q]))
                if ' '.join(w[:5]) in t or ' '.join(w[3:8]) in t: found.append(q)
        refs = re.findall(r'pag\.?\s*(\d+\*?)', ' '.join(P.get(p, '').split())) if p else []
        out[f"{k}/{x['i']}"] = {'page': p, 'printed': found, 'refs': refs}
        print(f"  {k}/{x['i']} @@{p} printed@{found} refs={refs[:8]}")
json.dump(out, open('/tmp/A7/locate.json', 'w'), indent=0)
