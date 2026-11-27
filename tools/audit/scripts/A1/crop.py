# usage: crop.py out.png "label|idx" ...   (idx = stream index)
import sys, json, os, subprocess
from PIL import Image, ImageDraw, ImageFont
S=json.load(open('/tmp/A1/stream.json'))
Z=150/72
import fitz
DOC=fitz.open('/home/claude/dl/missal/M39.pdf')
def page(i):
    fn='/tmp/A1/pg/p-%03d.png'%(i+1)
    if not os.path.exists(fn):
        os.makedirs('/tmp/A1/pg',exist_ok=True)
        subprocess.run(['pdftoppm','-r','150','-f',str(i+1),'-l',str(i+1),'-png','/home/claude/dl/missal/M39.pdf','/tmp/A1/pg/p'])
        if not os.path.exists(fn):  # pdftoppm pads differently
            alt=[f for f in os.listdir('/tmp/A1/pg') if f.endswith('-%d.png'%(i+1)) or f.endswith('-%02d.png'%(i+1))]
            if alt: os.rename('/tmp/A1/pg/'+alt[0],fn)
    return Image.open(fn)
out=sys.argv[1]; items=[a.split('|') for a in sys.argv[2:]]
crops=[]
font=ImageFont.load_default()
for lab,idx in items:
    w=S[int(idx)]; im=page(w[0])
    cb=DOC[w[0]].cropbox; ox,oy=cb.x0,cb.y0-DOC[w[0]].mediabox.y0
    x0,y0,x1,y1=w[1]+ox,w[2]+oy,w[3]+ox,w[4]+oy
    cx=(x0+x1)/2
    X0=max(0,cx-105); X1=min(im.width/Z,cx+105)
    Y0=max(0,y0-14); Y1=y1+20
    c=im.crop((int(X0*Z),int(Y0*Z),int(X1*Z),int(Y1*Z)))
    d=ImageDraw.Draw(c); 
    # underline target
    d.line([((x0-X0)*Z,(y1-Y0)*Z+2),((x1-X0)*Z,(y1-Y0)*Z+2)],fill=(0,160,0),width=2)
    lab_im=Image.new('RGB',(c.width,16),'white'); ImageDraw.Draw(lab_im).text((2,2),lab[:80],fill='blue',font=font)
    t=Image.new('RGB',(c.width,c.height+16),'white'); t.paste(lab_im,(0,0)); t.paste(c,(0,16)); crops.append(t)
cols=2; W=max(c.width for c in crops)
rows=(len(crops)+cols-1)//cols
H=[max(crops[r*cols+k].height for k in range(cols) if r*cols+k<len(crops)) for r in range(rows)]
M=Image.new('RGB',(W*cols+10,sum(H)+4*rows),'gray')
y=0
for r in range(rows):
    for k in range(cols):
        n=r*cols+k
        if n<len(crops): M.paste(crops[n],(k*(W+10),y))
    y+=H[r]+4
M.save(out); print(out,M.size)
