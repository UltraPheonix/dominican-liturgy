"""OCR the 1939 Missale O.P. by column, marking red (rubric) lines.
usage: ocr39.py BOOKPAGE [BOOKPAGE...]  -> /home/claude/build/m39hw/p<page>.json  [{red, text, y}]
pdf index = (bookpage - 2)//2 + 34?  computed from the known spread 138|139 = pdf page 103 (1-based)."""
import sys, os, json, subprocess, numpy as np, pymupdf
from PIL import Image
D='/home/claude/dl/p60'; OUT='/home/claude/build/m39hw'
FILES=[(1,60,'M39-001-060.pdf'),(61,120,'M39-061-120.pdf'),(121,180,'M39-121-180.pdf'),(181,240,'M39-181-240.pdf'),(241,300,'M39-241-300.pdf'),(301,360,'M39-301-360.pdf'),(361,420,'M39-361-420.pdf'),(421,463,'M39-421-463.pdf')]
def spread(bp):
    # book pages 138 (left) and 139 (right) are on pdf page 103
    pdfp = 103 + (bp - (bp % 2)) // 2 - 69
    side = 0 if bp % 2 == 0 else 1
    return pdfp, side
def render(pdfp):
    for a,b,f in FILES:
        if a<=pdfp<=b:
            d=pymupdf.open(os.path.join(D,f)); p=d[pdfp-a]
            pix=p.get_pixmap(dpi=300); return np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,:3]
def columns(img):
    g=img.mean(2); dark=(g<140)
    H,W=dark.shape
    col=dark[int(H*0.08):int(H*0.95)].sum(0).astype(float)
    col[col>H*0.45]=0          # the vertical rule between the columns
    sm=np.convolve(col,np.ones(15)/15,'same')
    on=sm>H*0.01
    xs=np.where(on)[0]
    if len(xs)==0: return []
    a,b=xs[0],xs[-1]; m0,m1=a+(b-a)*0.4,a+(b-a)*0.6
    mid=int(m0+np.argmin(sm[int(m0):int(m1)]))
    return [(a,mid),(mid,b)]
def _unused(img):
    g=img.mean(2); dark=(g<140); H,W=dark.shape
    col=dark[int(H*0.08):int(H*0.95)].sum(0)
    # find text runs separated by gaps
    on=col>H*0.004
    runs=[]; x=0
    while x<W:
        if on[x]:
            x0=x
            while x<W and (on[x] or (x+25<W and on[x:x+25].any())): x+=1
            if x-x0>W*0.08: runs.append((x0,x))
        x+=1
    return runs
def ocr(img):
    f='/tmp/m39c.png'; Image.fromarray(img).save(f)
    r=subprocess.run(['tesseract',f,'-','-l','lat','--psm','4','-c','tessedit_create_tsv=1'],capture_output=True,text=True,env={**os.environ,'TESSDATA_PREFIX':'/home/claude/tess'})
    lines={}
    for row in r.stdout.split('\n')[1:]:
        c=row.split('\t')
        if len(c)<12 or not c[11].strip(): continue
        k=(int(c[2]),int(c[3]),int(c[4]))
        x,y,w,h=map(int,c[6:10])
        L=lines.setdefault(k,{'words':[],'box':[x,y,x+w,y+h]})
        L['words'].append(c[11]); b=L['box']; L['box']=[min(b[0],x),min(b[1],y),max(b[2],x+w),max(b[3],y+h)]
    return sorted(lines.values(),key=lambda L:L['box'][1])
def run(bp):
    pdfp,side=spread(bp); img=render(pdfp); H,W,_=img.shape
    half=img[:, :W//2] if side==0 else img[:, W//2:]
    cols=columns(half); out=[]
    red=(half[:,:,0].astype(int)>110)&(half[:,:,0].astype(int)-half[:,:,1]>45)&(half[:,:,0].astype(int)-half[:,:,2]>35)
    dark=half.mean(2)<150
    for ci,(x0,x1) in enumerate(cols):
        sub=half[:, max(0,x0-14):x1+14]
        for L in ocr(sub):
            bx=L['box']; X0=max(0,x0-14)+bx[0]; X1=max(0,x0-14)+bx[2]
            rr=red[bx[1]:bx[3],X0:X1].sum(); dd=(dark|red)[bx[1]:bx[3],X0:X1].sum()+1
            out.append({'c':ci,'y':int(bx[1]),'red':bool(rr/dd>0.2),'t':' '.join(L['words'])})
    json.dump(out,open('%s/p%d.json'%(OUT,bp),'w'),ensure_ascii=False,indent=0)
    return out
if __name__=='__main__':
    for a in sys.argv[1:]:
        o=run(int(a)); print(a,len(o),'lines',sum(x['red'] for x in o),'red')
