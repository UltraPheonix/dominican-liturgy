#!/usr/bin/env python3
"""own.py KEY/I @@P[,@@Q..] : diff readings33 KEY[I].la against the text layer of the given @@PAGEs (best window)."""
import sys, re, json, difflib
from lib import *
T = open('/home/claude/dominican-liturgy/tools/orat39/m39lin.txt', encoding='utf8').read()
P = {}
for m in re.finditer(r'@@PAGE (\d+)\n(.*?)(?=@@PAGE|\Z)', T, re.S): P[int(m.group(1))] = m.group(2)
def clean(t):
    t = re.sub(r'­\s*\n\s*', '', t); t = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', t); t = t.replace('Arnen', 'Amen')
    return re.sub(r'\s+', ' ', t)
def window(la, pages):
    B = toks(clean(' '.join(P[p] for p in pages))); A = toks(la)
    al = [x.lower() for x in A]; bl = [x.lower() for x in B]
    sm = difflib.SequenceMatcher(None, al, bl, autojunk=False)
    bl_ = [b for b in sm.get_matching_blocks() if b.size >= 3]
    if not bl_: return A, []
    j0 = max(0, bl_[0].b - bl_[0].a); j1 = bl_[-1].b + bl_[-1].size + (len(A) - bl_[-1].a - bl_[-1].size)
    return A, B[j0:j1]
def odiff(la, pages, ctx=3):
    A, B = window(la, pages); out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op != 'equal':
            out.append(f"{op}: data[{' '.join(A[i1:i2])}] tl[{' '.join(B[j1:j2])}] @ ...{' '.join(A[max(0,i1-ctx):i1])} | {' '.join(A[i2:i2+ctx])}")
    return out
if __name__ == '__main__':
    r = R(); k, i = sys.argv[1].split('/'); pages = [int(x) for x in sys.argv[2].split(',')]
    for l in odiff(r[k][int(i)]['la'], pages): print('  ', l)
