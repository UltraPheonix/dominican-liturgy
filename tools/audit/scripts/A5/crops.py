import sys,re,json,subprocess,os; sys.path.insert(0,'/tmp/A5')
from PIL import Image, ImageDraw
from missal import p2pdf
from lib import *
G=json.load(open(ROOT+'tools/audit/groups.json'))['A5']
B=[k for k in G if k.startswith('S') and k in O and 'Missale' in O[k].get('src','')]
PDF='/home/claude/dl/missal/M39.pdf'; S=150/72
def words(n):
    fn='/tmp/A5/bb%d.html'%n
    if not os.path.exists(fn): subprocess.run(['pdftotext','-f',str(n),'-l',str(n),'-bbox',PDF,fn])
    return [(float(a),float(b),float(c),float(d),w) for a,b,c,d,w in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<',open(fn).read())]
def img(n):
    fn='/tmp/A5/img/r150_%d.png'%n
    if not os.path.exists(fn): subprocess.run(['pdftoppm','-f',str(n),'-l',str(n),'-r','150','-png','-singlefile',PDF,fn[:-4]])
    return Image.open(fn)
crops=[]
for k in B:
    src=O[k]['src']; p=re.search(r'p\. (\d+)',src).group(1); n=p2pdf(p)
    title=M[k]['title']; nm=re.search(r'B+\. (\w+)',title)
    key=nm.group(1)[:5].upper().replace('IOANN','JOANN').replace('IACOB','JACOB').replace('IORDA','JORDA').replace('Æ','') if nm else ''
    hit=None
    for pg in (n,n+1,n-1):
        W=words(pg)
        for i,w in enumerate(W):
            if w[4].upper().replace('Æ','AE').startswith(key[:4]) and w[4].isupper() and len(w[4])>3:
                hit=(pg,i,W); break
        if hit: break
    if not hit: print(k,'no hit',key); continue
    pg,i,W=hit; x0=W[i][0]; y0=W[i][1]
    # column: find left margin = min xMin of words within 120pt below with x within 120 of x0
    col=[w for w in W if 0<w[1]-y0<140 and abs(w[0]-x0)<150]
    cx0=min(w[0] for w in col)-4; cx1=max(w[2] for w in col)+4
    # end: first 'Oratio' / 'ORATIO' / 'Officium' line after rubric, else +110
    ye=y0+120
    for w in W[i+1:]:
        if w[1]>y0+8 and cx0<=w[0]<=cx1 and w[4] in ('Oratio','Secreta'): ye=w[3]+2; break
    im=img(pg); c=im.crop((int(cx0*S),int((y0-22)*S),int(cx1*S),int(ye*S)))
    crops.append((k,c))
# montage, 2 columns
def save(lst,fn):
    wmax=max(c.size[0] for _,c in lst); 
    H=sum(c.size[1]+24 for _,c in lst)
    out=Image.new('RGB',(wmax+10,H),'white'); d=ImageDraw.Draw(out); y=0
    for k,c in lst:
        d.text((4,y+4),k,fill=(255,0,0)); out.paste(c,(4,y+20)); y+=c.size[1]+24
    out.save(fn)
for j in range(0,len(crops),6):
    save(crops[j:j+6],'/tmp/A5/img/mont%02d.png'%(j//6))
print(len(crops))
