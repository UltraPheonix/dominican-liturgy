"""zs.py PAGE STAFF X0 X1 [scale] : plain zoomed crop of a staff (lines are the guide) with x ruler -> /tmp/rt/zs.png"""
import sys, numpy as np
sys.path.insert(0,'/home/claude/build/omr'); import staves
from PIL import Image, ImageDraw
pi, si, x0, x1 = map(int, sys.argv[1:5]); sc = float(sys.argv[5]) if len(sys.argv) > 5 else 1.6
a = np.array(Image.open('/tmp/rt/page%d.png' % pi).convert('L')).astype(float)
L = staves.find(a)[si]; s = (L[3]-L[0])/3
y0 = int(L[0]-2.2*s); y1 = int(L[3]+3.3*s)
im = Image.open('/tmp/rt/page%d.png' % pi).convert('RGB').crop((x0, y0, x1, y1))
im = im.resize((int(im.width*sc), int(im.height*sc)))
d = ImageDraw.Draw(im)
for xx in range(0, x1-x0, 50): d.line([(xx*sc, 0), (xx*sc, 8)], fill=(0,150,0)); d.text((xx*sc+2, 0), str(xx+x0), fill=(0,150,0))
im.save('/tmp/rt/zs.png'); print(L, s)
