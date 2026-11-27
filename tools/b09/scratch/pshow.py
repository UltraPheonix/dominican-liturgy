import sys,json
sys.path.insert(0,'/home/claude/dominican-liturgy/tools/b09')
import proper as P
vol,md=sys.argv[1],sys.argv[2]
a,b,st,en=P.VOLS[vol]
if len(sys.argv)>4: a,b=int(sys.argv[3]),int(sys.argv[4])
for d,title,rk,ch in P.chunks_cal(vol,a,b,st,en):
    if d!=md: continue
    X=P.parse(ch); print(title,len(ch))
    for k in ('v1','mat','laud','v2'): print(k, json.dumps(X.get(k),ensure_ascii=False))
    for x in X.get('lessons',[]):
        r=x.get('resp'); print(x['n'],x.get('src'),'|',x['la'][:50],'…',x['la'][-50:])
        if r: print('   R',r['src'],'|',r['a'],'*',r['b'],'| V',r['v'],r['gloria'])
    print('Q',X.get('q'))
