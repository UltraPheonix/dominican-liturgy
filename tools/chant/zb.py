"""zb.py PAGE x0 x1 sc y1 y2 ... : stack bands [y-100, y+135] with pitch guides from the staff found near y -> zz.png"""
import sys, numpy as np
from PIL import Image, ImageDraw
pi, x0, x1, sc = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
A = np.array(Image.open('/tmp/rt/page%d.png' % pi).convert('L')).astype(float); W = A.shape[1]
def lines(yc):
    win = A[yc-80:yc+80, int(W*0.2):int(W*0.85)] < 140; row = win.mean(1)
    idx = [i for i in range(len(row)) if row[i] > 0.33]
    g = []
    for i in idx:
        if g and i - g[-1][-1] <= 6: g[-1].append(i)
        else: g.append([i])
    c = [sum(x)/len(x) + yc - 80 for x in g]
    best = None
    for i in range(len(c) - 3):
        d = np.diff(c[i:i+4])
        if d.min() > 24 and d.max() < 42 and d.max() - d.min() < 10:
            if best is None or abs(np.mean(c[i:i+4]) - yc) < abs(np.mean(best) - yc): best = c[i:i+4]
    return best
ims = []
for y in map(int, sys.argv[5:]):
    c = Image.open('/tmp/rt/page%d.png' % pi).convert('RGB').crop((x0, y-100, x1, y+135))
    d = ImageDraw.Draw(c)
    L = lines(y)
    if L:
        s = (L[3]-L[0])/3
        for p in range(-3, 11):
            yy = L[3] - p*s/2 - (y-100)
            col = (0, 110, 255) if p % 2 == 0 else (255, 120, 0)
            for xx in range(0, c.width, 9): d.point((xx, yy), fill=col)
            d.text((0, yy-6), chr(ord('d')+p), fill=col); d.text((c.width-10, yy-6), chr(ord('d')+p), fill=col)
    c = c.resize((int(c.width*sc), int(c.height*sc)))
    d = ImageDraw.Draw(c)
    for xx in range(0, x1-x0, 50): d.text((xx*sc+12, 0), str(xx+x0), fill=(0,150,0))
    ims.append(c)
o = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims)), 'white'); yy = 0
for i in ims: o.paste(i, (0, yy)); yy += i.height
o.save('/tmp/rt/zz.png')
