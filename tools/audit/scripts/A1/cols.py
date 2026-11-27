# cols.py PDFPAGE(1-based) [dpi]: /tmp/A1/k_<p>_<n><a|b>.png for the 4 text columns (top/bottom halves)
import sys, fitz, warnings, json
warnings.filterwarnings('ignore')
S=json.load(open('/tmp/A1/stream.json'))
DOC=fitz.open('/home/claude/dl/missal/M39.pdf')
p=int(sys.argv[1])-1; dpi=int(sys.argv[2]) if len(sys.argv)>2 else 200
pg=DOC[p]; cb=pg.cropbox; ox,oy=cb.x0,cb.y0-pg.mediabox.y0
ws=[w for w in S if w[0]==p and w[6]<1.6]
xs=sorted(w[1] for w in ws)
# gaps between columns: find 3 largest gaps in the sorted x0/x1 coverage
cov=sorted((w[1],w[3]) for w in ws)
segs=[]
for a,b in cov:
    if segs and a<=segs[-1][1]+4: segs[-1][1]=max(segs[-1][1],b)
    else: segs.append([a,b])
segs=[s for s in segs if s[1]-s[0]>60]
segs2=[]
for a,b in segs:
    if b-a>250:
        m=(a+b)/2; segs2+= [[a,m+3],[m-3,b]]
    else: segs2.append([a,b])
segs=segs2
ys=sorted(w[2] for w in ws); y0=ys[int(len(ys)*0.01)]-25; y1=max(w[4] for w in ws)+8
for n,(a,b) in enumerate(segs):
    mid=(y0+y1)/2
    for h,(t0,t1) in zip('ab',[(y0,mid+15),(mid-15,y1)]):
        clip=fitz.Rect(a-4,t0,b+4,t1)
        pg.get_pixmap(dpi=dpi,clip=clip).save('/tmp/A1/k_%d_%d%s.png'%(p+1,n,h))
print(p+1,len(segs),[(round(a),round(b)) for a,b in segs])
