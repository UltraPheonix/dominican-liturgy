#!/usr/bin/env python3
"""Coordinator audit C0: compare data/addiv.js (2nd/3rd prayers) with the M39 text layer. Prints, per prayer, the
pdf page where it was found and the word/punctuation differences (to be checked on the scan before any fix)."""
import json, re, sys, unicodedata, difflib, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
lines = open(f'{R}/tools/orat39/m39lin.txt', encoding='utf8').read().split('\n')
PAGES = set(range(1, 700)) or set(range(196, 200)) | set(range(355, 360)) | set(range(414, 433)) | set(range(45, 52))
def fold(w):
    w = w.replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('ǽ','ae').replace('Œ','oe')
    w = ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn').lower()
    return w.replace('j','i')
def toks(s):
    s = re.sub(r'[­-]\s*\n\s*', '', s); s = s.replace('\n', ' ')
    return re.findall(r"[A-Za-zÀ-ÿæœǽÆŒ]+|[,;:.!?]", s)
stream = []; pg = 0; buf = []
for L in lines:
    m = re.match(r'@@PAGE (\d+)', L)
    if m:
        if pg in PAGES: stream += [(t, pg + 1) for t in toks('\n'.join(buf))]
        pg = int(m.group(1)); buf = []; continue
    buf.append(L)
F = [fold(t) for t, _ in stream]
s = open(f'{R}/data/addiv.js', encoding='utf8').read(); i = re.search(r'window\.\w+\s*=\s*', s).end(); j = s.rfind('}') + 1
D = json.loads(s[i:j])['sets']
out = []
for k, v in D.items():
    for part in ('or', 'se', 'pc'):
        if part not in v: continue
        txt = v[part]['la']; T = toks(txt); TF = [fold(t) for t in T]
        rg = range(418, 426) if k.startswith('d') and k[1:].isdigit() else range(356, 360) if k in ('bvmAdv','cruce') else range(1, 700) if k in ('bvm','bvmNat') else range(424, 432)
        words = [w for w in TF if w.isalpha()][:8]
        best = None
        for a in range(len(F)):
            if stream[a][1] not in rg or not F[a].isalpha(): continue
            seq = [w for w in F[a:a+16] if w.isalpha()][:8]
            sc = sum(x == y for x, y in zip(seq, words))
            if sc >= 5 and (best is None or sc > best[0]): best = (sc, a)
        if not best: out.append(f'{k}.{part}: NOT FOUND ({" ".join(T[:6])})'); continue
        a = best[1]; seg = F[a:a + len(TF) + 15]
        sm = difflib.SequenceMatcher(None, TF, seg, autojunk=False)
        # trim to the matched end
        blocks = [b for b in sm.get_matching_blocks() if b.size]
        end = blocks[-1].b + blocks[-1].size; seg = seg[:end]
        sm = difflib.SequenceMatcher(None, TF, seg, autojunk=False)
        diffs = [(op, ' '.join(T[i1:i2]), ' '.join(t for t, _ in stream[a + j1:a + j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal']
        out.append(f'{k}.{part}: pdf {stream[a][1]} | {len(diffs)} diffs' + ''.join(f'\n    {op}: site[{x}] m39[{y}]' for op, x, y in diffs))
print('\n'.join(out))
