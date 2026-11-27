import sys,re,json; sys.path.insert(0,'/tmp/A5')
from missal import *
from lib import *
G=json.load(open(ROOT+'tools/audit/groups.json'))['A5']
B=[k for k in G if k.startswith('S') and k in O and 'Missale' in O[k].get('src','')]
def pagetext(n):
    ls=[i for i in range(len(L)) if pdf[i] in (n,n+1)]
    return ' '.join(L[i].strip() for i in ls)
for k in B:
    src=O[k]['src']; m=re.search(r'p\. (\d+)',src); p=m.group(1)
    n=p2pdf(p)
    t=pagetext(n); t=re.sub(r'­\s*','',t)
    # name word from title
    title=M[k]['title']
    nm=re.search(r'B+\. (\w+)',title)
    w=nm.group(1)[:5].upper() if nm else ''
    w=w.replace('IOANN','JOANN').replace('IACOB','JACOB').replace('IORDA','JORDA')
    j=t.upper().find(w) if w else -1
    seg=t[j-20:j+330] if j>=0 else 'NOTFOUND '+w
    print(k,'p',p,'pdf',n,'|',seg.replace('\n',' '))
    print()
