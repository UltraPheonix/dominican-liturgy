import sys,re; sys.path.insert(0,'/tmp/A5'); sys.path.insert(0,'/tmp/A6')
from lib import *
from missal import p2pdf
L=open(ROOT+'tools/orat39/m39lin.txt').read().split('\n')
pidx={}
for i,l in enumerate(L):
    m=re.match(r'@@PAGE (\d+)',l)
    if m: pidx[int(m.group(1))+1]=i
def rubric(k):
    src=O.get(k,{}).get('src','') or M[k].get('page','')
    m=re.search(r'p\. ?(\d+)',src) or re.search(r'^(\d+)',M[k].get('page',''))
    if not m: return None,'no page'
    n=p2pdf(m.group(1)); 
    t=M[k]['title']; d=re.match(r'(\d+) (\w+)',t)
    s=pidx.get(n-1,0); e=pidx.get(n+2,len(L))
    txt=L[s:e]
    # find "Die D" lines
    out=[]
    for i,l in enumerate(txt):
        if re.match(r'\s*Die %d\b'%int(k[3:5]),l):
            out.append(' '.join(x.strip() for x in txt[i:i+12]))
    return n,out
if __name__=='__main__':
    for k in sys.argv[1:]:
        n,o=rubric(k); print('==',k,M[k]['title'],'| pdf',n,'|',[r['ref'] for r in R.get(k,[])] or [r['ref'] for r in M[k].get('readings',[])])
        for x in (o or []): print('   ',x[:420])
