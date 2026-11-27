# crop a staff with detected heads and pitch grid; usage: crop.py PNM X0 X1 L1,L2,L3,L4 OUT [SEGW]
import sys, subprocess, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
pnm, x0, x1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
L = [float(v) for v in sys.argv[4].split(',')]; out = sys.argv[5]
segw = int(sys.argv[6]) if len(sys.argv) > 6 else 1000
SC = float(sys.argv[7]) if len(sys.argv) > 7 else 1.15
gap = (L[3]-L[0])/3
r = subprocess.run(['python3','/home/claude/dominican-liturgy/tools/g28/blobs.py',pnm,str(x0),str(x1),sys.argv[4]],capture_output=True,text=True).stdout.split()
heads=[(int(t.split(':')[0]), t.split(':')[1][0]) for t in r]
full=Image.open(pnm).convert('L')
y0=int(L[0]-4.5*gap); y1=int(L[3]+3.3*gap)
arr=np.array(full).astype(float)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
i=0; xs=x0
while xs < x1:
    xe=min(x1, xs+segw)
    sx0=max(0,xs-40)
    band=arr[:, sx0:xe+40] < 100
    prof=band.mean(1)
    LL=[]
    for Ly in L:
        a,b=int(Ly-14),int(Ly+14); LL.append(a+int(np.argmax(prof[a:b])))
    im=ImageOps.autocontrast(full.crop((sx0,y0,xe+40,y1)),cutoff=1).convert('RGB')
    im=im.resize((int(im.width*SC),int(im.height*SC)))
    can=Image.new('RGB',(im.width+30, im.height+50),(255,255,255)); can.paste(im,(30,50))
    dr=ImageDraw.Draw(can)
    hl=(LL[3]-LL[0])/6
    for k in range(-4,11):
        y=(LL[3]-k*hl-y0)*SC+50
        col=(230,0,0) if k%2==0 else (0,110,255)
        dr.text((2,y-11),'abcdefghijklmn'[3+k] if 0<=3+k<14 else '?',fill=col,font=font)
        for x in range(30,can.width,40): dr.line([(x,y),(x+5,y)],fill=col)
    cnt={}
    for x,l in heads:
        if sx0<=x<xe+40:
            px=(x-sx0)*SC+30; k=int(px//28); o=cnt.get(k,0); cnt[k]=o+1
            dr.text((px,2+(o%2)*22),l,fill=(200,0,0),font=font)
    for x in range(xs, xe, 100):
        dr.text(((x-sx0)*SC+30, can.height-22), str(x), fill=(0,140,0), font=font)
    can.save('%s_%d.png'%(out,i)); i+=1; xs=xe
print(' '.join('%d:%s'%h for h in heads))
