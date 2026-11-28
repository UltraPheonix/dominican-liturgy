#!/usr/bin/env python3
"""variants.py [N...] : for each Commune reading N, the distinct Latin variants among its copies, each diffed with the text layer."""
import sys, json
from collections import defaultdict
from lib import *
from tl import diff
C = json.load(open('/tmp/A7/comm_readings.json')); CL = json.load(open('/tmp/A7/clusters.json')); r = R()
ns = [int(x) for x in sys.argv[1:]] or sorted({x['c'] for x in CL})
for n in ns:
    print('########', n, 'tl page', C[n]['page'], C[n]['head'][:60])
    var = defaultdict(list)
    for x in CL:
        if x['c'] == n: var[r[x['key']][x['i']]['la']].append(f"{x['key']}/{x['i']}")
    for la, ks in sorted(var.items(), key=lambda t: -len(t[1])):
        print(' -- variant used by', len(ks), ':', ' '.join(ks))
        for l in diff(la, C[n]['la']): print('     ', l)
