import sys, os, pickle
os.environ.setdefault('TRI_CACHE','/home/claude/build/tri_staves.pkl')
import build
S = build.S
for k in sorted(S):
    if not (int(sys.argv[1]) <= k[0] <= int(sys.argv[2])): continue
    for i, x in enumerate(S[k]):
        sy, items, s = build.ocr_sylls(x)
        print('%d%s.%d n%d | %s' % (k[0], k[1], i, len([it for it in items if it[1]=='note']), ' '.join(t for t, x0 in sy)))
