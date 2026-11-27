import re,unicodedata,difflib
lines=open('/home/claude/dominican-liturgy/tools/orat39/m39lin.txt',encoding='utf8').read().split('\n')
def fold(w):
    w=w.replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('ǽ','ae').replace('Œ','oe')
    w=''.join(c for c in unicodedata.normalize('NFD',w) if unicodedata.category(c)!='Mn').lower()
    return w.replace('j','i')
def toks(s):
    s=re.sub(r'[­-]\s*\n\s*','',s); s=s.replace('\n',' ')
    return re.findall(r"[A-Za-zÀ-ÿæœǽÆŒ]+|[,;:.!?]",s)
stream=[]; pg=0; buf=[]
for L in lines+['@@PAGE 9999']:
    m=re.match(r'@@PAGE (\d+)',L)
    if m:
        stream+=[(t,pg+1) for t in toks('\n'.join(buf))]; pg=int(m.group(1)); buf=[]; continue
    buf.append(L)
F=[fold(t) for t,_ in stream]
def find(txt,rg,n=8):
    T=toks(txt); TF=[fold(t) for t in T]; words=[w for w in TF if w.isalpha()][:n]
    best=None
    for a in range(len(F)):
        if stream[a][1] not in rg or not F[a].isalpha() or F[a]!=words[0]: continue
        seq=[w for w in F[a:a+2*n] if w.isalpha()][:n]
        sc=sum(x==y for x,y in zip(seq,words))
        if sc>=n*0.6 and (best is None or sc>best[0]): best=(sc,a)
    return best
def diff(txt,rg,show=True,tail=15,skip=0):
    T=toks(txt)[skip:]; TF=[fold(t) for t in T]
    b=find(' '.join(T),rg)
    if not b: return None,'NOT FOUND'
    a=b[1]; seg=F[a:a+len(TF)+tail]
    sm=difflib.SequenceMatcher(None,TF,seg,autojunk=False)
    bl=[x for x in sm.get_matching_blocks() if x.size]; end=bl[-1].b+bl[-1].size; seg=seg[:end]
    sm=difflib.SequenceMatcher(None,TF,seg,autojunk=False)
    d=[(op,' '.join(T[max(0,i1-2):i2+2]),' '.join(t for t,_ in stream[a+max(0,j1-2):a+j2+2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
    return (stream[a][1],stream[a+end-1][1]),d
