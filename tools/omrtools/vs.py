"""vs.py PAGE STAFF [x0 x1] : crop a staff of /tmp/rt/page<PAGE>.png with letter guides (gabc positions) -> /tmp/rt/vs.png"""
import sys, numpy as np
sys.path.insert(0,'/home/claude/build/omr'); import staves
from PIL import Image, ImageDraw, ImageFont
pi, si = int(sys.argv[1]), int(sys.argv[2])
a = np.array(Image.open('/tmp/rt/page%d.png' % pi).convert('L')).astype(float)
L = staves.find(a)[si]; s = (L[3]-L[0])/3
x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 200; x1 = int(sys.argv[4]) if len(sys.argv) > 4 else 1600
y0 = int(L[0]-2.6*s); y1 = int(L[3]+3.6*s)
im = Image.open('/tmp/rt/page%d.png' % pi).convert('RGB').crop((x0, y0, x1, y1))
d = ImageDraw.Draw(im)
try: f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
except Exception: f = None
for p in range(-3, 10):
    y = L[3] - p*s/2 - y0
    col = (0, 120, 255) if p % 2 == 0 else (255, 140, 0)
    for xx in range(0, im.width, 6): d.point((xx, y), fill=col)
    d.text((2, y-8), chr(ord('d')+p), fill=col, font=f)
    d.text((im.width-14, y-8), chr(ord('d')+p), fill=col, font=f)
for xx in range(0, im.width, 100): d.text((xx, 0), str(xx+x0), fill=(0,160,0), font=f)
sc = float(sys.argv[5]) if len(sys.argv) > 5 else 1.25; im = im.resize((int(im.width*sc), int(im.height*sc)))
im.save('/tmp/rt/vs.png')
