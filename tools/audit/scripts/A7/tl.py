#!/usr/bin/env python3
"""tl.py N KEY/I : token diff (deaccented, case kept) of readings33 KEY[I].la against Commune text-layer reading N."""
import sys, json, difflib
from lib import *
C = json.load(open('/tmp/A7/comm_readings.json'))
def diff(a, b, ctx=3):
    A, B = toks(a), toks(b); out = []
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal': continue
        out.append(f"{op}: data[{' '.join(A[i1:i2])}] tl[{' '.join(B[j1:j2])}]  @ ...{' '.join(A[max(0,i1-ctx):i1])} | {' '.join(A[i2:i2+ctx])}")
    return out
if __name__ == '__main__':
    n = int(sys.argv[1]); r = R()
    for ki in sys.argv[2:]:
        k, i = ki.split('/'); e = r[k][int(i)]
        print('==', ki, e.get('ref'), '| vs', n, C[n]['page'], C[n]['head'][:50])
        for l in diff(e['la'], C[n]['la']): print('  ', l)
