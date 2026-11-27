import json,sys
from align import *
from load import *
O=load('data/orations.js')
G=json.load(open('/home/claude/dominican-liturgy/tools/audit/groups.json'))['A4']
res={}
for k in G:
    o=O.get(k)
    if not o: print(k,'NO ORATIONS'); continue
    exp=None
    for p in ('or','se','pc'):
        if p not in o or not o[p]: print(k,p,'MISSING'); continue
        la=o[p][0]; m=CONCL.search(la); body=la[:m.start()] if m else la
        r=compare(body,exp)
        if not r: print(k,p,'NOT FOUND',la[:60]); continue
        if exp is None: exp=r['line']
        # missal conclusion: tokens after end
        e=r['end']
        idx=next(n for n,t in enumerate(MS) if t[2]>=e)
        # find the conclusion following
        seg=[t[1] for t in MS[idx:idx+12]]
        res[(k,p)]=r
        dd='; '.join(f"{t}[{a}|{b}]@{c}" for t,a,b,c,_ in r['diffs'])
        print(k,p,f"{r['score']:.2f}",r['page'],'|',(m.group(0)[:22] if m else 'NOCONCL'),'|M:',' '.join(seg),'|',dd)
