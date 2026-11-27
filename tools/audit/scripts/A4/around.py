import sys;sys.path.insert(0,'/tmp/A4')
from crop import words,image,find
from PIL import Image
def around(pdf,ctx,up=40,down=120,out=None):
    W,pw,ph=words(pdf); im=image(pdf); sx=im.width/pw; sy=im.height/ph
    r=find(pdf,ctx); ws=W[r[0]:r[1]]
    x0=min(w[0] for w in ws); y0=min(w[1] for w in ws)
    # column: guess width 175pt
    colw=pw/4.6
    xs=x0-colw*0.6
    c=im.crop((int(max(0,xs)*sx),int((y0-up)*sy),int((xs+colw*1.25)*sx),int((y0+down)*sy)))
    c.save(out); return out
if __name__=='__main__':
    print(around(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]))
