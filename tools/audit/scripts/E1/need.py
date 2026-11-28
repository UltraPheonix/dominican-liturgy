# which pair halves need Tesseract: English of every DM prayer near a site prayer; Latin where the text layer is not clean
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import pickle, collections, difflib, glob, re
import dm_verbatim as V, cmp as C
pairs, _, _ = pickle.load(open(W_('pairs.pkl'), 'rb'))
F = V.F
fl = [F(V.dm_body(x['la'])) for x in pairs]
idx = collections.defaultdict(set)
for n, f in enumerate(fl):
    for k in range(0, max(1, len(f) - 8), 3): idx[f[k:k + 8]].add(n)
needE = set(); needL = set()
for file, k, f, la, en, cur in V.site_prayers():
    fs = F(la); c = collections.Counter()
    for q in range(0, max(1, len(fs) - 8), 2):
        for n in idx.get(fs[q:q + 8], ()): c[n] += 1
    for n, _ in c.most_common(6):
        r = difflib.SequenceMatcher(None, fs, fl[n], autojunk=False).ratio()
        if r < 0.6: continue
        needE.add(n)
        real, _ = C.compare(la, V.dm_body(pairs[n]['la']))
        if real: needL.add(n)
done = lambda i, s: bool(glob.glob(W_('crops/%04d_%s_*.tsv' % (i, s))))
jobs = [(i, 'e') for i in sorted(needE) if not done(i, 'e')] + [(i, 'l') for i in sorted(needL) if not done(i, 'l')]
open(W_('jobs.txt'), 'w').write(''.join('%d %s\n' % j for j in jobs))
print('need E', len(needE), 'L', len(needL), 'jobs left', len(jobs))
