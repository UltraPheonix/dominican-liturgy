# half-staff zooms of a piece: half.py code staffno part(0/1) out
import sys, pickle
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/build/abl')
import gcache
S = pickle.load(open('/home/claude/build/tri_staves.pkl', 'rb'))
R = pickle.load(open('/home/claude/build/abl/res.pkl', 'rb'))
code, n, part, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
key, lo, hi = R[code]['spans'][n]
x = S[key[:2]][key[2]]; s = x['s']; L = x['L']; g = gcache.G(*key[:2])
X0 = int(x['x'][0] - 0.3 * s); X1 = int(x['x'][1] + 0.3 * s); mid = (X0 + X1) // 2
xa, xb = X0, X1
y0 = int(L[0] - 1.8 * s); y1 = int(L[3] + 2.7 * s)
im = Image.fromarray(g[y0:y1, xa:xb].astype('uint8')).convert('RGB'); sc = 1.1
im = im.resize((int(im.width * sc), int(im.height * sc))); d = ImageDraw.Draw(im)
for p in range(-2, 10):
    yy = (L[3] - p * s / 2 - y0) * sc
    c = (0, 0, 255) if p % 2 == 0 else (0, 170, 0)
    d.line([(0, yy), (18, yy)], fill=c, width=2); d.text((20, yy - 12), 'bcdefghijklm'[p + 2], fill=c, font=F)
    d.line([(im.width - 18, yy), (im.width, yy)], fill=c, width=2); d.text((im.width - 40, yy - 12), 'bcdefghijklm'[p + 2], fill=c, font=F)
im.save(out); print(lo, hi, im.size)
