import sys
from PIL import Image
import numpy as np
from scipy import ndimage
def run(f, box):
    im = np.array(Image.open(f).convert('L').crop(box)) < 120
    H, W = im.shape
    rows = im.sum(1)
    ls = [i for i in range(H) if rows[i] > W * 0.45]
    g = []
    for r in ls:
        if g and r - g[-1][-1] <= 3: g[-1].append(r)
        else: g.append([r])
    lines = [sum(x)/len(x) for x in g]
    # erase thin staff lines: a pixel on a line row is kept only if pixels 4 above or below are dark
    m = im.copy()
    for grp in g:
        for r in grp:
            for x in range(W):
                if m[r, x] and not (r-5 >= 0 and im[r-5, x]) and not (r+5 < H and im[r+5, x]):
                    m[r, x] = False
    m = ndimage.binary_opening(m, np.ones((5, 5)))
    lab, n = ndimage.label(m)
    out = []
    for sl in ndimage.find_objects(lab):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if 14 <= w <= 45 and 14 <= h <= 90:
            out.append(((sl[1].start + sl[1].stop)//2, (sl[0].start + sl[0].stop)/2, h))
    out.sort()
    # group staves by 4 lines
    staves = [lines[i:i+4] for i in range(0, len(lines) - 3, 4)]
    names = 'abcdefghijklm'
    for st in staves:
        top, bot = st[0], st[3]; sp = (bot - top) / 6  # half-space
        res = []
        for x, y, h in out:
            if top - 3*sp <= y <= bot + 3*sp:
                ys = [y] if h < 2.3*sp*2*0.8 else [y - h/4, y + h/4]
                ps = []
                for yy in ys:
                    k = round((bot - yy) / sp)  # 0 = line1 = d
                    ps.append(names[3 + k] if 0 <= 3 + k < len(names) else '?')
                res.append('%d:%s' % (x, ''.join(ps)))
        print('staff', [round(v) for v in st], ' '.join(res))
if __name__ == '__main__':
    f = sys.argv[1]; box = tuple(int(v) for v in sys.argv[2].split(','))
    run(f, box)
