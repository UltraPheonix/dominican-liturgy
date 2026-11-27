import re
from pages import blocks, L
P2L={}
for b in blocks:
    p=b[2]
    if not p: continue
    star=p.endswith('*'); n=int(p.rstrip('*'))
    for q in (n,n+1):
        key=f"{q}*" if star else str(q)
        P2L.setdefault(key,b[1])
def pages_from(src):
    m=re.search(r'p\. (\d+\*?)(?:\s*-\s*(\d+\*?))?',src or '')
    if not m: return None
    a=m.group(1); b=m.group(2) or a
    return a,b
