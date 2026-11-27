# wc.py: column crop around a word. usage from python: wcrop(pdf, word, before_lines, after_lines, out, nth=0)
import subprocess,re,html,os
from PIL import Image, ImageDraw
PDF='/home/claude/dl/missal/M39.pdf'; DPI=220; S=DPI/72
_bb={}
def words(pg):
    if pg not in _bb:
        x=subprocess.run(['pdftotext','-bbox','-f',str(pg),'-l',str(pg),PDF,'-'],capture_output=True,text=True).stdout
        pw=float(re.search(r'<page width="([\d.]+)"',x).group(1))
        W=[(float(a),float(b),float(c),float(d),html.unescape(w)) for a,b,c,d,w in re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',x)]
        _bb[pg]=(pw,W)
    return _bb[pg]
def img(pg):
    fn='/tmp/A6/img/w%d.png'%pg
    if not os.path.exists(fn): subprocess.run(['pdftoppm','-r',str(DPI),'-f',str(pg),'-l',str(pg),'-png','-singlefile',PDF,fn[:-4]])
    return Image.open(fn)
def colof(pg,x):
    pw,W=words(pg)
    cov=[0]*int(pw+2)
    for a,b,c,d,_ in W:
        for i in range(int(a),int(c)): cov[i]+=1
    xs=[i for i in range(len(cov)) if cov[i]>0]
    segs=[];s0=xs[0];prev=xs[0]
    for i in xs[1:]:
        if i-prev>5: segs.append((s0,prev)); s0=i
        prev=i
    segs.append((s0,prev)); segs=[s for s in segs if s[1]-s[0]>60]
    ns=[]
    for a,c in segs:
        if c-a>250:
            lo=a+(c-a)//3; hi=a+2*(c-a)//3; m=min(range(lo,hi),key=lambda i:cov[i]); ns+=[(a,m),(m,c)]
        else: ns.append((a,c))
    for a,c in ns:
        if a-3<=x<=c: return a-4,c+4
    return x-10,x+170
def wcrop(pg,word,before=2,after=10,nth=0):
    pw,W=words(pg)
    hits=[w for w in W if word.lower() in w[4].lower()]
    if len(hits)<=nth: return None
    x0,y0,x1,y1,_=hits[nth]
    # column: quarter of the spread
    lx,rx=colof(pg,x0)
    lh=11.2
    im=img(pg)
    return im.crop((int(lx*S),int((y0-before*lh-3)*S),int(rx*S),int((y0+after*lh)*S)))
def montage(items,out):
    ims=[(lab,c) for lab,c in items if c is not None]
    if not ims: return
    W=max(c.size[0] for _,c in ims)+10; H=sum(c.size[1]+26 for _,c in ims)
    o=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(o); y=0
    for lab,c in ims:
        d.text((4,y+4),lab,fill=(255,0,0)); o.paste(c,(4,y+22)); y+=c.size[1]+26
    o.save(out)
