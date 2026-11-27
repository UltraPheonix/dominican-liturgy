# cols.py PDFPAGE [nparts] : crop the 4 text columns of a spread at 250 dpi into nparts vertical pieces: img/s{pg}_{c}{r}.png
import sys,subprocess,re,os
from PIL import Image
pg=int(sys.argv[1]); parts=int(sys.argv[2]) if len(sys.argv)>2 else 2; dpi=250; S=dpi/72
x=subprocess.run(['pdftotext','-bbox','-f',str(pg),'-l',str(pg),'/home/claude/dl/missal/M39.pdf','-'],capture_output=True,text=True).stdout
pw,ph=map(float,re.search(r'<page width="([\d.]+)" height="([\d.]+)"',x).groups())
W=[(float(a),float(b),float(c),float(d)) for a,b,c,d in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)"',x)]
# column boundaries: histogram of coverage
cov=[0]*int(pw+1)
for a,b,c,d in W:
    for i in range(int(a),int(c)): cov[i]+=1
xs=[i for i in range(len(cov)) if cov[i]>0]
# find gaps >=6pt
segs=[];s0=xs[0];prev=xs[0]
for i in xs[1:]:
    if i-prev>5: segs.append((s0,prev)); s0=i
    prev=i
segs.append((s0,prev))
segs=[s for s in segs if s[1]-s[0]>60]
ns=[]
for a,c in segs:
    if c-a>250:
        lo=a+(c-a)//3; hi=a+2*(c-a)//3; m=min(range(lo,hi),key=lambda i:cov[i]); ns+=[(a,m),(m,c)]
    else: ns.append((a,c))
segs=ns
fn='/tmp/A6/img/full%d_%d'%(pg,dpi)
if not os.path.exists(fn+'.png'): subprocess.run(['pdftoppm','-r',str(dpi),'-f',str(pg),'-l',str(pg),'-png','-singlefile','/home/claude/dl/missal/M39.pdf',fn])
im=Image.open(fn+'.png')
ys=[b for a,b,c,d in W]; ye=[d for a,b,c,d in W]; y0=min(ys)-5; y1=max(ye)+5
out=[]
for ci,(a,c) in enumerate(segs):
    for r in range(parts):
        t0=y0+(y1-y0)*r/parts-8; t1=y0+(y1-y0)*(r+1)/parts+8
        o='/tmp/A6/img/s%d_%d%d.png'%(pg,ci+1,r+1)
        im.crop((int((a-4)*S),int(t0*S),int((c+4)*S),int(t1*S))).save(o); out.append(o)
print(len(segs),'cols',segs)
