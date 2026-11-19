# big zoom around syllables i0..i1 of a piece: zz.py code i0 i1 out
import sys, pickle, os
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/build/ten')
import gcache
S = pickle.load(open(os.environ.get('TRI_CACHE','/home/claude/build/tri_staves.pkl'), 'rb'))
R = pickle.load(open('/home/claude/build/ten/res.pkl', 'rb'))
code, i0, i1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
sp = [z for z in R[code]['spans'] if z[1] <= i0 <= z[2]][0]; key = sp[0]
x = S[key[:2]][key[2]]; s = x['s']; L = x['L']; g = gcache.G(*key[:2])
xs = [n[0] for i in range(i0, i1 + 1) for n in R[code]['nx'][i]]
x0 = int(max(0, min(xs) - float(sys.argv[5] if len(sys.argv) > 5 else 1.5) * s)); x1 = int(max(xs) + 2 * s); y0 = int(L[0] - 1.7 * s); y1 = int(L[3] + 2.6 * s)
im = Image.fromarray(g[y0:y1, x0:x1].astype('uint8')).convert('RGB'); sc = 3
im = im.resize((im.width * sc, im.height * sc)); d = ImageDraw.Draw(im)
for p in range(-2, 10):
    yy = (L[3] - p * s / 2 - y0) * sc
    d.line([(0, yy), (25, yy)], fill=(0, 0, 255) if p % 2 == 0 else (0, 170, 0), width=2)
    d.text((28, yy - 12), 'bcdefghijklm'[p + 2], fill=(0, 0, 255) if p % 2 == 0 else (0, 170, 0), font=F)
im.save(out); print([(i, R[code]['out'][i][0], R[code]['out'][i][1]) for i in range(i0, i1 + 1)])
