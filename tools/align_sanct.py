import json, re, sys, io, difflib
_o=sys.stdout; sys.stdout=io.StringIO()
from build_temporale import norm, groups
from build_sanctorale import heads, lines, letters, MONTHS
sys.stdout=_o
blocks=[]
for k,(i,day,mon) in enumerate(heads):
    end = heads[k+1][0] if k+1 < len(heads) else i+300
    txt='\n'.join(lines[i:end])
    name=' '.join(l.strip() for l in lines[i+1:i+4])
    blocks.append({'i':i,'day':day,'mon':mon,'flat':letters(txt),'name':name})
sanct=[g for g in groups if g['section']=='sanctorum']
def probes(g):
    core=[g['introit']]+[c['incipit'] for c in g['chants'][1:4]]
    out=[]
    for k,s in enumerate(core):
        t=letters(s)
        if len(t)>=8: out.append((3.0 if k==0 else 1.0, t[1:12]))
    return out
P={g['gid']:probes(g) for g in sanct}
def sc(g,b):
    return sum(w for w,p in P[g['gid']] if p in b['flat'])
n,m=len(sanct),len(blocks)
F=[[0]*(m+1) for _ in range(n+1)];B=[[None]*(m+1) for _ in range(n+1)]
for i in range(1,n+1):
    F[i][0]=F[i-1][0]; B[i][0]='g'
for j in range(1,m+1):
    F[0][j]=0; B[0][j]='b'
for i in range(1,n+1):
    for j in range(1,m+1):
        s=sc(sanct[i-1],blocks[j-1])
        opts=[(F[i-1][j-1]+(s if s>0 else -9),'m'),(F[i-1][j],'g'),(F[i][j-1],'b')]
        F[i][j],B[i][j]=max(opts)
i,j,pairs=n,m,{}
while i>0 and j>0:
    if B[i][j]=='m': pairs[sanct[i-1]['gid']]=(j-1,sc(sanct[i-1],blocks[j-1])); i-=1; j-=1
    elif B[i][j]=='g': i-=1
    else: j-=1
res={}
for g in sanct:
    if g['gid'] in pairs:
        j,s=pairs[g['gid']]; b=blocks[j]
        res[g['gid']]={'month':b['mon'],'day':b['day'],'score':s,'missal_name':b['name'][:90]}
        print('%3d p.%-6s %-28s -> %2d %s  [%.0f] %s'%(g['gid'],g['page'],g['introit'][:28],b['day'],MONTHS[b['mon']][:4],s,b['name'][:70]))
    else:
        print('%3d p.%-6s %-28s -> ---'%(g['gid'],g['page'],g['introit'][:28]))
json.dump(res,open('sanct_dates.json','w'),ensure_ascii=False)
