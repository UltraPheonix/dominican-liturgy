import json,sys
from load import *
from cmp import *
O=load('data/orations.js'); D=load('data/masses.js'); M=D['masses']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
keys=sys.argv[1:] or G
for key in keys:
    m=M.get(key,{}); o=O.get(key)
    print('=====',key,'|',m.get('title'),'| page',m.get('page'),m.get('conf'),'| orsrc:',(o or {}).get('src'))
    if not o: print('  NO ORATIONS'); continue
    for p in ('or','se','pc'):
        if p not in o: print('  ',p,'MISSING'); continue
        v=o[p]
        if not isinstance(v,list) or len(v)<2: print('  ',p,'STRUCT',type(v),len(v) if isinstance(v,list) else ''); 
        la=v[0]; b,c=split_concl(la)
        r=compare(b)
        if not r or not r[1]: print('  ',p,'NOT FOUND:',la[:80]); continue
        S,best=r
        print('  %s %.3f %s | concl site: %s | missal next: %s'%(p,best[0],where(best[3]),' '.join(c.split()[:3]),after(best[1],5)))
        for l in show(S,best): print(l)
        if len(v)>2: print('   extra fields:',v[2:])
