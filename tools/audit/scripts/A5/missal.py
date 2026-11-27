import re,unicodedata
L=open('/home/claude/dominican-liturgy/tools/orat39/m39lin.txt',encoding='utf8').read().split('\n')
# map line -> pdf page
pdf=[0]*len(L); pg=0
for i,l in enumerate(L):
    m=re.match(r'@@PAGE (\d+)',l)
    if m: pg=int(m.group(1))+1
    pdf[i]=pg
def fold(s):
    s=s.replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('Œ','oe').replace('ǽ','ae').replace('ǿ','oe')
    s=unicodedata.normalize('NFD',s); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    s=s.lower().replace('j','i')
    return s
def toks(s):
    return re.findall(r"[a-z]+|[,;:.?!]",fold(s))
# build missal token stream with line numbers; join soft hyphen line breaks
TK=[];TL=[]
buf=''
for i,l in enumerate(L):
    if l.startswith('@@PAGE'): continue
    s=l.rstrip()
    if re.fullmatch(r'\s*\d+\s*\*?\s*',s) or re.fullmatch(r'-?0\d0',s.strip()): continue
    if s.endswith('­') or s.endswith('­'):
        buf+=s.rstrip('­'); continue
    s=buf+s; buf=''
    for t in toks(s):
        TK.append(t); TL.append(i)
WI={}
words=[(k,t) for k,t in enumerate(TK) if t.isalpha()]
import json as _j
_PN=_j.load(open('/tmp/A5/pnums.json'))
_P2={}
for k,v in _PN.items():
    for x in v: _P2.setdefault(x,int(k))
def p2pdf(p):
    p=str(p).strip()
    if p in _P2: return _P2[p]
    star=p.endswith('*'); n=int(p.rstrip('*'))
    for d in range(1,6):
        for q in (n-d,n+d):
            k=str(q)+('*' if star else '')
            if k in _P2: return _P2[k]+ (n//2 - q//2)
    return None
def pdf2lines(pg):
    return [i for i in range(len(L)) if pdf[i]==pg]
