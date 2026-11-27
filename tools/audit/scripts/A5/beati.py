import sys,json; sys.path.insert(0,'/tmp/A5')
from lib import *
G=json.load(open(ROOT+'tools/audit/groups.json'))['A5']
B=[k for k in G if k.startswith('S')]
fx=json.load(open(ROOT+'tools/audit/fixes/A5.json'))
# old reading texts of commune keys -> (key,i,new)
OLD={}
for e in fx:
    if e['file']=='data/readings33.js' and e['path'][2]=='la':
        OLD[e['old']]=(e['path'][0],e['path'][1],e['new'])
CUR={}
for k in R:
    if k.startswith('C'):
        for i,r in enumerate(R[k]): CUR.setdefault(r['la'],[]).append((k,i))
out=[]
for k in B:
    m=M.get(k)
    if not m: print(k,'NOT IN masses'); continue
    rd=R.get(k,[])
    ch={p:[x.get('id') for x in v] for p,v in (m.get('parts') or {}).items()}
    info=[]
    for i,r in enumerate(rd):
        t=r['la']
        if t in OLD: info.append('rd%d=OLD %s.%d'%(i,OLD[t][0],OLD[t][1]))
        elif t in CUR: info.append('rd%d=same %s'%(i,'/'.join('%s.%d'%x for x in CUR[t])))
        else: info.append('rd%d=OWN %s'%(i,r['ref']))
    print(k,'|',m.get('title')[:45],'|',m.get('introit'),'|',' '.join(info),'|',O.get(k,{}).get('src','')[:60])
