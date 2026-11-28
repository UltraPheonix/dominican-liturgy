import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import fitz, sys, subprocess, os, warnings
warnings.filterwarnings('ignore')
doc=fitz.open(PDF)
part,n=int(sys.argv[1]),int(sys.argv[2])
NEED=[int(x) for x in open(W_('need.txt'))]
for p in NEED:
    if p%n!=part: continue
    out=W_('tess/')+f'{p:04d}'
    if os.path.exists(out+'.tsv'): continue
    png=W_('tess/')+f'tmp{part}.png'
    doc[p].get_pixmap(dpi=300).save(png)
    subprocess.run(['tesseract',png,out,'-l','eng','--psm','6','tsv'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
