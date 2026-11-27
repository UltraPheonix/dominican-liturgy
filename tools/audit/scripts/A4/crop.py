import re, os, subprocess, html, sys, json
from PIL import Image, ImageDraw
sys.path.insert(0,'/tmp/A4')
from tok import fold
PDF='/home/claude/dl/missal/M39.pdf'
_bb={}
def words(pdf):
    if pdf in _bb: return _bb[pdf]
    fn=f'/tmp/A4/bb/{pdf}.html'
    os.makedirs('/tmp/A4/bb',exist_ok=True)
    if not os.path.exists(fn): subprocess.run(['pdftotext','-f',str(pdf),'-l',str(pdf),'-bbox',PDF,fn],check=True)
    s=open(fn,encoding='utf8').read()
    W=[(float(a),float(b),float(c),float(d),html.unescape(t)) for a,b,c,d,t in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<',s)]
    pw,ph=map(float,re.search(r'page width="([\d.]+)" height="([\d.]+)"',s).groups())
    # column order: 4 text columns (2 printed pages x 2 columns); order by column, then line (y), then x
    cov=[0]*(int(pw)+2)
    for w in W:
        if w[3]-w[1]>20: continue
        for x in range(int(w[0]),int(w[2])+1): cov[x]+=1
    # gutters: runs of zero coverage of width>=4 between text
    xs=[x for x in range(len(cov)) if cov[x]]
    lo,hi=min(xs),max(xs); cuts=[]; x=lo
    while x<hi:
        if cov[x]<=2:
            y=x
            while y<hi and cov[y]<=2: y+=1
            if y-x>=6: cuts.append((x+y)/2)
            x=y
        else: x+=1
    def col(w):
        c=(w[0]+w[2])/2; return sum(1 for k in cuts if k<c)
    W.sort(key=lambda w:(col(w), w[3], w[0]))
    # group lines: within a column, words whose yMax within 3 of the line's
    out=[];cur=None
    for w in W:
        k=(col(w),)
        if cur and cur[0]==k and abs(w[3]-cur[1])<=4: out[-1].append(w)
        else: out.append([w]); cur=(k,w[3])
        cur=(k,cur[1] if cur and cur[0]==k and abs(w[3]-cur[1])<=4 else w[3])
    W=[w for line in out for w in sorted(line,key=lambda z:z[0])]
    _bb[pdf]=(W,pw,ph); return _bb[pdf]
_img={}
def image(pdf):
    fn=f'/tmp/A4/img/{pdf}.png'
    os.makedirs('/tmp/A4/img',exist_ok=True)
    if not os.path.exists(fn):
        subprocess.run(['pdftoppm','-r','200','-f',str(pdf),'-l',str(pdf),'-png','-singlefile',PDF,fn[:-4]],check=True)
    if pdf not in _img: _img[pdf]=Image.open(fn)
    return _img[pdf]
def find(pdf, ctx):
    W,pw,ph=words(pdf)
    f=[re.sub(r'[^a-z]','',fold(w[4])) for w in W]
    c=[re.sub(r'[^a-z]','',fold(x)) for x in ctx.split()]
    c=[x for x in c if x]
    best=None
    for i in range(len(W)):
        # match c sequentially allowing hyphen splits: concatenate
        j=i; k=0; ok=0
        while k<len(c) and j<len(W):
            if not f[j]: j+=1; continue
            if f[j]==c[k]: ok+=1; j+=1; k+=1
            elif c[k].startswith(f[j]) and j+1<len(W) and (f[j]+f[j+1])==c[k][:len(f[j]+f[j+1])]:
                # split word across lines
                j+=2 if (f[j]+f[j+1])==c[k] else 1; k+=1; ok+=1
            else: break
        if ok>=max(1,len(c)-0) and (best is None): best=(i,j)
    return best
def crop(pdf, ctx, pad=6):
    W,pw,ph=words(pdf); im=image(pdf); sx=im.width/pw; sy=im.height/ph
    r=find(pdf,ctx)
    if not r: return None
    ws=W[r[0]:r[1]]
    # crop: the lines covered, full column width around
    x0=min(w[0] for w in ws); x1=max(w[2] for w in ws); y0=min(w[1] for w in ws); y1=max(w[3] for w in ws)
    if x1-x0 < 120: x0-=60; x1+=60
    c=im.crop((int((x0-pad)*sx),int((y0-1.5)*sy),int((x1+pad)*sx),int((y1+1.5)*sy)))
    return c.resize((int(c.width*0.6),int(c.height*0.6)))
def montage(items, out, maxh=1500):
    ims=[]
    for pdf,ctx,label in items:
        try: c=crop(pdf,ctx)
        except Exception as e: c=None
        if c is None:
            c=Image.new('RGB',(500,24),'white'); ImageDraw.Draw(c).text((5,5),'NOT FOUND: '+ctx[:60],fill='blue')
        if c.width>900: c=c.crop((0,0,900,c.height))
        ims.append((label,c))
    pages=[];cur=[];h=0
    for it in ims:
        hh=it[1].height+16
        if cur and h+hh>maxh: pages.append(cur); cur=[]; h=0
        cur.append(it); h+=hh
    if cur: pages.append(cur)
    outs=[]
    for n,pg in enumerate(pages):
        W=max(c.width for _,c in pg)+10; H=sum(c.height+16 for _,c in pg)
        M=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(M); y=0
        for label,c in pg:
            d.text((4,y+2),label,fill='red'); y+=14
            M.paste(c.convert('RGB'),(5,y)); y+=c.height+2
        fn=out.replace('.png',f'_{n}.png'); M.save(fn); outs.append(fn)
    return outs
if __name__=='__main__':
    items=json.load(open(sys.argv[1]))
    if len(sys.argv)>3: items=[x for x in items if x[2].split()[0] in sys.argv[3].split(',')]
    print(montage(items,sys.argv[2]))
