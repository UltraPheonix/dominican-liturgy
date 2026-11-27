# list the note heads of a staff: x, letter (gabc position), kind -- from a page image and the staff's 4 line ys
import sys, numpy as np
from PIL import Image
from scipy import ndimage
pnm, x0, x1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
L = [float(v) for v in sys.argv[4].split(',')]
gap = (L[3] - L[0]) / 3; half = gap / 2
y0 = int(L[0] - 3 * gap); y1 = int(L[3] + 2.5 * gap)
g = np.array(Image.open(pnm).convert('L').crop((x0, y0, x1, y1))).astype(float)
b = g < 100
# remove thin horizontal lines: keep pixels with vertical run > line thickness
lt = max(3, int(gap * 0.12))
v = np.zeros_like(b)
for c in range(b.shape[1]):
    col = b[:, c]; r = 0
    for i in range(len(col)):
        r = r + 1 if col[i] else 0
        if r > lt: v[i - r + 1:i + 1, c] = True
# heads are thick both ways: erode by a small square
k = max(3, int(gap * 0.28))
h = ndimage.binary_opening(v, structure=np.ones((k, k)))
lab, n = ndimage.label(h)
out = []
for sl in ndimage.find_objects(lab):
    ys, xs = sl; hh = ys.stop - ys.start; ww = xs.stop - xs.start
    if ww < gap * 0.35 or hh < gap * 0.3: continue
    # a tall blob may be two heads stacked (pes): split by height
    nheads = max(1, int(round(hh / (gap * 0.62))))
    # the staff lines near this note (the page is not quite level)
    cx = (xs.start + xs.stop) // 2; wa, wb = max(0, cx - 200), min(b.shape[1], cx + 200)
    prof = b[:, wa:wb].sum(1) / (wb - wa)
    LL = []
    for Ly in L:
        r0, r1 = int(Ly - y0 - 14), int(Ly - y0 + 14)
        seg = prof[r0:r1]; LL.append(y0 + r0 + int(np.argmax(seg)) if len(seg) else Ly)
    Lb = LL[3]; halfl = (LL[3] - LL[0]) / 6
    for j in range(nheads):
        cy = ys.start + (j + 0.5) * hh / nheads + y0
        pos = round((Lb - cy) / halfl)        # 0 = bottom line (d)
        out.append((xs.start + x0, xs.stop + x0, 'abcdefghijklmn'[3 + pos] if -3 <= pos <= 10 else '?', round((Lb - cy) / halfl, 2)))
out.sort(key=lambda t: (t[0], -t[3]))
print(' '.join('%d:%s(%.1f)' % (a, l, p) for a, _, l, p in out))
