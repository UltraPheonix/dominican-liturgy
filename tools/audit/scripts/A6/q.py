# q.py PDFPAGE [dpi] : render page, write quarter crops /tmp/A6/img/pPAGE_{L,R}{1,2,3}.png (column x third)
import sys,subprocess
from PIL import Image
pg=int(sys.argv[1]); dpi=int(sys.argv[2]) if len(sys.argv)>2 else 220
fn='/tmp/A6/img/full%d_%d'%(pg,dpi)
import os
if not os.path.exists(fn+'.png'):
    subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(pg),'-l',str(pg),'-png','-singlefile','/home/claude/dl/missal/M39.pdf',fn])
im=Image.open(fn+'.png'); W,H=im.size
parts=int(sys.argv[3]) if len(sys.argv)>3 else 3
for ci,(x0,x1) in enumerate([(0,W//2+15),(W//2-15,W)]):
    for r in range(parts):
        y0=max(0,int(H*r/parts)-30); y1=min(H,int(H*(r+1)/parts)+30)
        im.crop((x0,y0,x1,y1)).save('/tmp/A6/img/p%d_%s%d.png'%(pg,'LR'[ci],r+1))
print(W,H)
