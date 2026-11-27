import sys
from load import load
O=load('data/orations.js'); D=load('data/masses.js'); M=D['masses']
for k in sys.argv[1:]:
    o=O.get(k,{}); m=M.get(k,{})
    print('==',k,m.get('title'),'| page',m.get('page'),'| readings',m.get('readings'))
    for p,v in o.items():
        if p in ('src',): print(' src:',v); continue
        if isinstance(v,list) and v and isinstance(v[0],str): print(f' {p}: {v[0]}')
        else: print(f' {p}: {str(v)[:300]}')
