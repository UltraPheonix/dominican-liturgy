# q.py PDFPAGE(1-based) x0 y0 x1 y1 (fractions) out
import sys,os,subprocess
from PIL import Image
p=int(sys.argv[1]); fn='/tmp/A1/pg/p-%03d.png'%p
if not os.path.exists(fn):
    subprocess.run(['pdftoppm','-r','150','-f',str(p),'-l',str(p),'-png','/home/claude/dl/missal/M39.pdf','/tmp/A1/pg/p'])
im=Image.open(fn); W,H=im.size
x0,y0,x1,y1=map(float,sys.argv[2:6])
im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H))).save(sys.argv[6])
