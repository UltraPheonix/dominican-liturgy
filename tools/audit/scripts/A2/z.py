import sys
from PIL import Image
# z.py PDF x0 y0 x1 y1 (fractions of full spread) [dpi]
N=int(sys.argv[1]); x0,y0,x1,y1=map(float,sys.argv[2:6]); dpi=int(sys.argv[6]) if len(sys.argv)>6 else 300
import os,subprocess
f='/tmp/A2/hi-%d-%d.png'%(N,dpi)
if not os.path.exists(f):
    subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(N),'-l',str(N),'-png','/home/claude/dl/missal/M39.pdf','/tmp/A2/hix'],check=True)
    import glob; g=glob.glob('/tmp/A2/hix-*%d.png'%N)[0]; os.rename(g,f)
im=Image.open(f); W,H=im.size
out='/tmp/A2/z-%d-%s.png'%(N,'_'.join(sys.argv[2:6]))
im.crop((int(W*x0),int(H*y0),int(W*x1),int(H*y1))).save(out); print(out)
