"""pomr.py PDFPAGE [clef] : staves and note heads of a Processionarium page"""
import sys, numpy as np, pymupdf
sys.path.insert(0,'/home/claude/build/omr'); import staves
from PIL import Image
pi=int(sys.argv[1]); clef=sys.argv[2] if len(sys.argv)>2 else 'c4'
d=pymupdf.open('/home/claude/dl/proc/proc.pdf'); pix=d[pi].get_pixmap(dpi=300)
a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].mean(2)
Image.fromarray(a.astype(np.uint8)).save('/tmp/rt/page%d.png'%pi)
for i,L in enumerate(staves.find(a)):
    print(i,[round(v) for v in L], round((L[3]-L[0])/3,1))
    print('  ',' '.join('%d:%s'%(x,staves.name(p,clef)) for x,w,p in staves.read(a,L)))
