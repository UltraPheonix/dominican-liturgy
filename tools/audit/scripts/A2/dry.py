import sys; sys.path.insert(0,'/tmp/A2')
from lib import load
from chk import chk
K=sys.argv[1]; lo,hi=int(sys.argv[2]),int(sys.argv[3])
d={}; exec(open('/tmp/A2/ver3.py').read(),d)
L={'data/orations.js':load('data/orations.js'),'data/readings33.js':load('data/readings33.js'),'data/masses.js':load('data/masses.js')}
for x in d['EXTRA']:
    if x['path'][0]!=K: continue
    v=L[x['file']]
    for p in x['path']: v=v[p]
    if 'subs' in x:
        new=v
        for a,b in x['subs']:
            if a not in new: print('!! sub not found',x['path'],a)
            new=new.replace(a,b)
    else: new=x['new']
    if x['path'][-1] in ('la',0) and isinstance(new,str):
        chk(new.split(' Per Dóminum nostrum Iesum')[0],lo,hi,str(x['path']))
