# dm.py "latin fragment(folded)" [n] : DM 1959 pairs matching; saves crop of the English rows to /tmp/A1/dm_<n>.png
import gzip,pickle,re,sys,fitz,warnings
warnings.filterwarnings('ignore')
P=pickle.load(gzip.open('/home/claude/dominican-liturgy/tools/orat39/dm1959/cache/pairs.pkl.gz'))
D=fitz.open('/tmp/A1/dmdl/dm.pdf')
def f(s): return re.sub(r'[^a-z]','',s.lower().replace('æ','ae').replace('j','i'))
q=f(sys.argv[1]); k=0
for x in P[0]:
    if q in f(x.get('la','')):
        print(k,x['typ'],'p',x['p'],'|',x['en'])
        rows=x['erows']; pg=rows[0][0]
        bb=[r[1][0] for r in rows if r[0]==pg]
        clip=fitz.Rect(min(b[0] for b in bb)-3,min(b[1] for b in bb)-14,max(b[2] for b in bb)+3,max(b[3] for b in bb)+3)
        D[pg].get_pixmap(dpi=150,clip=clip).save('/tmp/A1/dm_%d.png'%k); k+=1
