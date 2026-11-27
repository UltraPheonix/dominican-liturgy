import re, unicodedata, json
LIN='/home/claude/dominican-liturgy/tools/orat39/m39lin.txt'
def fold(w):
    w=w.lower().replace('æ','ae').replace('ǽ','ae').replace('œ','oe').replace('j','i').replace('ë','e')
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if unicodedata.category(c)!='Mn')
    return w
TOK=re.compile(r"[A-Za-zÀ-ÿæǽœŒÆĀ-ſ]+|[:;,.!?()]")
def toks(s):
    s=s.replace('\xad','')
    return [(fold(m.group()),m.group()) for m in TOK.finditer(s)]
L=open(LIN,encoding='utf8').read().split('\n')
HEAD=re.compile(r'^(Festa|Dominica|Feria|Sabbato|Commune|Missae|Missa|In |Vigilia|Hebdomada|Tempus|Ordo|Proprium|Orationes|Praefationes|Appendix|Supplementum)')
drop=set(); pdfleft={}
RH=re.compile(r'^\s*(Festa\s*[A-Z]|Proprium\s|Commune\s|Dominica\s.*\(\S{1,4}\)\s*$|Feria\s.*\(\S{1,4}\)\s*$)')
pdf=0
for i,l in enumerate(L):
    if l.startswith('@@PAGE'): pdf=int(l.split()[1]); continue
    if RH.match(l) and len(l.strip())<34 and not re.search(r'[:;,]',l): drop.add(i)
    if re.fullmatch(r'\s*\d{1,4}\*?\s*',l):
        drop.add(i)
        if L[i-1].startswith('@@PAGE'): pdfleft[pdf]=l.strip()
        for j in (i-1,i+1):
            if 0<=j<len(L) and len(L[j])<40 and HEAD.match(L[j].strip()) and not re.search(r'[:,;]',L[j]): drop.add(j)
stream=[]
pdf=0; pending=''; pline=0
def flush(text, ln, p):
    for f,o in toks(text): stream.append((f,o,ln,p))
ppdf=0
for i,l in enumerate(L):
    if l.startswith('@@PAGE'):
        pdf=int(l.split()[1]); continue
    if i in drop: continue
    s=l.rstrip()
    if pending:
        if pending.endswith('\xad') or (pending.endswith('-') and not pending.endswith(' -')):
            pending=pending[:-1]+s.lstrip(); continue
        flush(pending,pline,ppdf)
    pending=s; pline=i+1; ppdf=pdf
flush(pending,pline,ppdf)
_s=[]
for n,t in enumerate(stream):
    if t[1]=='c' and n+1<len(stream) and stream[n+1][0]=='.': continue
    if t[0]=='.' and n>0 and stream[n-1][1]=='c' : continue
    if t[0]=='arnen': t=('amen','Amen*',t[2],t[3])
    _s.append(t)
stream[:]=_s
F=[t[0] for t in stream]
W=[k for k,t in enumerate(stream) if t[0][0].isalpha()]   # word positions
WF=[F[k] for k in W]
from collections import defaultdict
IDX=defaultdict(list)
for n in range(len(WF)-3): IDX[' '.join(WF[n:n+4])].append(n)
def where(k):
    t=stream[min(k,len(stream)-1)]; p=t[3]
    return 'pdf %d (p. %s), line %d'%(p+1, pdfleft.get(p,'?'), t[2])
def find(sitetoks, near=None, maxc=20):
    """candidate stream positions where the site's text starts (by its first word 4-grams)"""
    sw=[f for f,o in sitetoks if f[0].isalpha()]
    cands=defaultdict(int)
    for off in range(0,min(len(sw)-3,40)):
        g=' '.join(sw[off:off+4])
        for n in IDX.get(g,[]):
            if n-off>=0: cands[n-off]+=1
    if not cands: return []
    best=sorted(cands.items(), key=lambda x:(-x[1], abs(W[x[0]]-near) if near is not None else 0))
    return [W[n] for n,c in best[:maxc]]
