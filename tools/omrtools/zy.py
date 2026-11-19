"""zy.py PAGE : find staves by horizontal projection; zy.py PAGE i j [x0 x1 sc] : stack staves i..j -> zz.png"""
import sys, numpy as np
from PIL import Image, ImageDraw
pi = int(sys.argv[1])
im = Image.open('/tmp/rt/page%d.png' % pi).convert('L'); a = np.array(im).astype(float)
dark = (a < 140)
W = a.shape[1]
row = dark[:, int(W*0.2):int(W*0.85)].mean(1)
lines = [y for y in range(1, len(row)-1) if row[y] > 0.25 and row[y] >= row[y-1] and row[y] >= row[y+1]]
# merge adjacent
L = []
for y in lines:
    if L and y - L[-1][-1] <= 3: L[-1].append(y)
    else: L.append([y])
L = [sum(g)/len(g) for g in L]
st = []
i = 0
while i + 3 < len(L):
    g = L[i:i+4]; d = np.diff(g)
    if d.max() < 46 and d.min() > 22 and d.max() - d.min() < 12: st.append(g); i += 4
    else: i += 1
if len(sys.argv) == 2:
    for k, g in enumerate(st): print(k, [round(v) for v in g])
    sys.exit()
s0, s1 = int(sys.argv[2]), int(sys.argv[3])
x0, x1, sc = (int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (230, 1570, 0.95)
ims = []
for g in st[s0:s1+1]:
    sp = (g[3]-g[0])/3
    c = Image.open('/tmp/rt/page%d.png' % pi).convert('RGB').crop((x0, int(g[0]-2.3*sp), x1, int(g[3]+3.3*sp)))
    c = c.resize((int(c.width*sc), int(c.height*sc)))
    d = ImageDraw.Draw(c)
    for xx in range(0, x1-x0, 50): d.text((xx*sc+2, 0), str(xx+x0), fill=(0,150,0))
    ims.append(c)
o = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims)), 'white'); y = 0
for i in ims: o.paste(i, (0, y)); y += i.height
o.save('/tmp/rt/zz.png')
