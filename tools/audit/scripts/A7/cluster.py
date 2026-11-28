#!/usr/bin/env python3
"""For every readings33 entry, the best-matching Commune reading (text layer pp. 1*-40*). -> /tmp/A7/clusters.json"""
import json, difflib
from lib import *
C = json.load(open('/tmp/A7/comm_readings.json'))
r = R(); O = json.load(open(ST + 'orations.json'))
CN = [norm(c['la']) for c in C]
res = []
for k, v in r.items():
    for i, e in enumerate(v):
        a = norm(e['la'])
        best = None
        for n, b in enumerate(CN):
            if not set(a[:12]) & set(b[:12]): continue
            s = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
            if best is None or s > best[0]: best = (s, n)
        if best and best[0] > 0.6:
            src = O.get(k, {}).get('src', '') if isinstance(O.get(k), dict) else ''
            res.append({'key': k, 'i': i, 'ref': e.get('ref'), 'c': best[1], 'sim': round(best[0], 3), 'src': src})
json.dump(res, open('/tmp/A7/clusters.json', 'w'), ensure_ascii=False, indent=0)
from collections import defaultdict
g = defaultdict(list)
for x in res: g[x['c']].append(x)
for n in sorted(g):
    print('##', n, C[n]['page'], C[n]['head'][:60])
    print('   ', ' '.join(f"{x['key']}/{x['i']}:{x['sim']}" for x in sorted(g[n], key=lambda x: -x['sim'])))
