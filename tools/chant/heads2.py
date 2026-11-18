"""heads.py PDFPAGE : per staff, note heads as x:pos (pos 0 = bottom line, 1 = space above, ...), plus lyric words with x"""
import sys, numpy as np, pymupdf, subprocess, re
sys.path.insert(0,'/home/claude/build/omr'); import staves
from scipy import ndimage as ndi
from PIL import Image
pi=int(sys.argv[1])
a=np.array(Image.open('/tmp/rt/page%d.png'%pi).convert('L')).astype(float) if len(sys.argv)<3 else None
def read(a,L):
    s=(L[3]-L[0])/3; y0=int(L[0]-2.2*s); y1=int(L[3]+2.2*s)
    B=(a[y0:y1]<150); R=staves.vrun(B); C=B.copy()
    for y in L:
        yy=int(round(y))-y0; C[yy-3:yy+4]&=(R[yy-3:yy+4]>s*0.45)
    C=ndi.binary_closing(C,structure=np.ones((5,5))); C=ndi.binary_fill_holes(C)
    C=ndi.binary_opening(C,structure=np.ones((int(s*0.32),int(s*0.32))))
    lab,n=ndi.label(C); out=[]
    for sl in ndi.find_objects(lab):
        ys,xs=sl; h=ys.stop-ys.start; w=xs.stop-xs.start
        if w<s*0.3 or w>s*1.6 or h<s*0.3: continue
        k=max(1,round(h/(s*0.5)))
        sub=(lab[sl]==lab[sl][lab[sl]>0].max()) if False else (C[sl])
        for j in range(k):
            ya=int(j*h/k); yb=int((j+1)*h/k)
            cols=np.where(sub[ya:yb].any(0))[0]
            cx=xs.start+(int(cols.mean()) if len(cols) else w//2)
            cy=ys.start+(j+0.5)*h/k+y0
            out.append((cx,w,round((L[3]-cy)/(s/2))))
    out.sort(key=lambda t:(t[0],t[2])); return out
st=staves.find(a)
for i,L in enumerate(st):
    s=(L[3]-L[0])/3
    print('staff',i,'lines',[round(v) for v in L])
    hs=[(x,p) for x,w,p in read(a,L) if -2<=p<=8]
    if not hs: continue
    clef=min(x for x,p in hs)
    cp=[p for x,p in hs if x<clef+25]
    hs=[(x,p) for x,p in hs if x>clef+30]
    out=[]
    for x,p in sorted(hs):
        if out and abs(out[-1][0]-x)<6 and out[-1][1]==p: continue
        out.append((x,p))
    print('   clef pos',sorted(set(cp)),' notes:',' '.join('%d%s'%(x,chr(ord('d')+p)) for x,p in out))
    y0=int(L[3]+0.6*s); y1=int(L[3]+3.2*s)
    Image.fromarray(a[y0:y1].astype(np.uint8)).save('/tmp/rt/ly.png')
    h=subprocess.run(['tesseract','/tmp/rt/ly.png','-','--psm','7','hocr'],capture_output=True,text=True).stdout
    words=re.findall(r"bbox (\d+) \d+ (\d+) \d+; x_wconf \d+'>([^<]+)<",h)
    print('   lyrics:',' '.join('%s@%s'%(w,x0) for x0,x1,w in words))
