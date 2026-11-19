"""blobs.py : note heads in /tmp/rt/zs.png with pitch letters from the measured staff lines (c-clef letters: d=bottom line)."""
import numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi
a = np.array(Image.open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/rt/zs.png').convert('L')).astype(float)
B = a < 120
W = a.shape[1]
row = B[:, int(W*0.25):int(W*0.95)].mean(1)
ys = [y for y in range(len(row)) if row[y] > 0.6]
g = []
for y in ys:
    if g and y - g[-1][-1] <= 2: g[-1].append(y)
    else: g.append([y])
L = [sum(x)/len(x) for x in g]
import itertools
best=None
for i in range(len(L)-3):
    d=np.diff(L[i:i+4])
    if d.max()-d.min()<8 and d.min()>15:
        best=L[i:i+4]; break
L = best
s = (L[3]-L[0])/3
# keep pixels inside vertical runs taller than a line (removes staff lines, keeps heads)
run = np.zeros_like(B, dtype=int)
for x in range(B.shape[1]):
    col = B[:, x]; y = 0
    while y < len(col):
        if col[y]:
            y2 = y
            while y2 < len(col) and col[y2]: y2 += 1
            run[y:y2, x] = y2 - y; y = y2
        else: y += 1
C = B & (run >= s*0.45)
C = ndi.binary_opening(C, structure=np.ones((int(s*0.35), int(s*0.35))))
lab, n = ndi.label(C)
out = []
for sl in ndi.find_objects(lab):
    ys_, xs_ = sl; h = ys_.stop-ys_.start; w = xs_.stop-xs_.start
    if w < s*0.35 or w > s*1.5 or h < s*0.35 or ys_.start > L[3]+3*s: continue
    k = max(1, round(h/(s*0.55)))
    for j in range(k):
        cy = ys_.start + (j+0.5)*h/k
        p = round((L[3]-cy)/(s/2))
        out.append((xs_.start + w//2, chr(ord('d')+p)))
out.sort()
print('lines', [round(v) for v in L])
print(' '.join('%s@%d' % (p, x) for x, p in out))
