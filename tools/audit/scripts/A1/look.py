# look.py PDFPAGE(1-based) "phrase" [above_pt] [below_pt] [out] [xshift]
import sys, json, fitz, warnings, re, unicodedata, collections
warnings.filterwarnings('ignore')
S=json.load(open('/tmp/A1/stream.json'))
DOC=fitz.open('/home/claude/dl/missal/M39.pdf')
def f(w): 
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if not unicodedata.combining(c))
    return re.sub(r'[^a-z]','',w.lower().replace('æ','ae'))
p=int(sys.argv[1])-1; ph=[f(x) for x in sys.argv[2].split()]
up=float(sys.argv[3]) if len(sys.argv)>3 else 20; dn=float(sys.argv[4]) if len(sys.argv)>4 else 150
out=sys.argv[5] if len(sys.argv)>5 else '/tmp/A1/look.png'
xs=float(sys.argv[6]) if len(sys.argv)>6 else 0
idx=[i for i,w in enumerate(S) if w[0]==p]
toks=[(i,f(S[i][5])) for i in idx]; toks=[t for t in toks if t[1]]
hit=None
for k in range(len(toks)-len(ph)+1):
    if all(toks[k+j][1]==ph[j] for j in range(len(ph))): hit=toks[k][0]; break
if hit is None: print('NOT FOUND'); sys.exit(1)
w=S[hit]
pg=DOC[p]; cb=pg.cropbox; ox,oy=cb.x0,cb.y0-pg.mediabox.y0
# column left: min x0 of words on this page within +-100pt vertically and within 175pt left
near=[S[i] for i in idx if abs(S[i][2]-w[2])<120 and w[1]-175<S[i][1]<=w[1]+1]
c=collections.Counter(round(x[1]/5) for x in near)
cl=[k*5 for k,n in c.items() if n>=3]
left=min(cl) if cl else w[1]
clip=fitz.Rect(left-6+xs,w[2]-up,left+170+xs,w[2]+dn)
pix=pg.get_pixmap(dpi=220,clip=clip); pix.save(out); print(out)
