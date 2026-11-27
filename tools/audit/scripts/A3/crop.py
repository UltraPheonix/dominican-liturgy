import fitz, sys, json
from PIL import Image, ImageDraw
D=fitz.open('/home/claude/dl/missal/M39.pdf')
def locate(pg, words):
    page=D[pg]
    for n in (4,3,2,1):
        for s in range(0,max(1,len(words)-n+1)):
            ph=' '.join(words[s:s+n])
            if len(ph)<3: continue
            r=page.search_for(ph)
            if r: return r
    return []
def crop(pg, rect, padx=(90,150), pady=(16,16), zoom=4):
    page=D[pg]
    clip=fitz.Rect(rect.x0-padx[0], rect.y0-pady[0], rect.x1+padx[1], rect.y1+pady[1]) & page.rect
    pix=page.get_pixmap(matrix=fitz.Matrix(zoom,zoom), clip=clip)
    return Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
def montage(items, out, padx=(90,150), pady=(16,16)):
    ims=[]
    for lab,pg,words in items:
        rs=locate(pg, words)
        if not rs: ims.append((lab+' [NOT LOCATED]',None)); continue
        ims.append((lab, crop(pg, rs[0], padx, pady)))
    W=max([i.width for l,i in ims if i] or [400]); H=sum((i.height if i else 0)+28 for l,i in ims)
    m=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(m); y=0
    for l,i in ims:
        d.text((4,y+6),l,fill='blue'); y+=28
        if i: m.paste(i,(0,y)); y+=i.height
    m.save(out)
if __name__=='__main__':
    items=json.load(open(sys.argv[1])); montage(items, sys.argv[2])
