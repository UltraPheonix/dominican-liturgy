# pg.py "phrase" [pdfpage-range lo hi 1-based]: Missal page(s) of a phrase from the stream
import json,re,sys,unicodedata
S=json.load(open('/tmp/A1/stream.json'))
def f(w):
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if not unicodedata.combining(c)); return re.sub(r'[^a-z]','',w.lower().replace('æ','ae'))
ph=[f(x) for x in sys.argv[1].split()]; lo,hi=int(sys.argv[2])-1,int(sys.argv[3])-1
H={}
for w in S:
    if lo<=w[0]<=hi and re.fullmatch(r'\d{1,3}\*?',w[5]) and w[2]<62: H.setdefault(w[0],[]).append((w[1],w[5]))
idx=[i for i,w in enumerate(S) if lo<=w[0]<=hi]
toks=[(i,f(S[i][5])) for i in idx]; toks=[t for t in toks if t[1]]
for k in range(len(toks)-len(ph)+1):
    if all(toks[k+j][1]==ph[j] for j in range(len(ph))):
        w=S[toks[k][0]]; hs=sorted(H.get(w[0],[]))
        side=0 if w[1]<400 else 1
        pgno=hs[side][1] if len(hs)>side else '?'
        print(sys.argv[1],'-> M39 p.',pgno,'(pdf %d)'%(w[0]+1))
