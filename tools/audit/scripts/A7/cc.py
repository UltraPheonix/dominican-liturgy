#!/usr/bin/env python3
"""cc.py CANON_KEY/I KEY/I ... : raw token diff (accents, case, marks) of copies against the canonical entry; also en and title."""
import sys, re, difflib
from lib import *
def rt(s): return re.findall(r"[^\W\d_]+|[.,:;?!]", s)
def rdiff(a, b, ctx=2):
    A, B = rt(a), rt(b); out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op != 'equal': out.append(f"{op}: [{' '.join(A[i1:i2])}]→[{' '.join(B[j1:j2])}] @ {' '.join(A[max(0,i1-ctx):i1])} | {' '.join(A[i2:i2+ctx])}")
    return out
if __name__ == '__main__':
    r = R(); ck, ci = sys.argv[1].split('/'); c = r[ck][int(ci)]
    for ki in sys.argv[2:]:
        k, i = ki.split('/'); e = r[k][int(i)]
        d = rdiff(e['la'], c['la']); de = rdiff(e.get('en', ''), c.get('en', ''))
        print(f"== {ki} (copy→canon) la:{len(d)} en:{len(de)} title:{e.get('title')==c.get('title')} ref:{e.get('ref')==c.get('ref')} en_src:{e.get('en_src')}/{c.get('en_src')}")
        for l in d: print('   LA', l)
        for l in de[:6]: print('   EN', l)
