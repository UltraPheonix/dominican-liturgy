import sys,re,json; sys.path.insert(0,'/tmp/A6')
from lib import *; from m39 import *
MM=revert('data/memoriae.js',load('data/memoriae.js'))
CONC=re.compile(r'\s*(Per (D[óo]minum|eú[mn]dem)|Qui (tecum|vivis))[^.]*?(sǽcula sæculórum|sæcula sæculorum)\.?\s*$')
def split(t):
    m=re.search(r'[\s]*(Per (D[óo]minum nostrum|eú[mn]dem Dóminum)|Qui (tecum|vivis) vivi?t? ?|Qui vivis)',t)
    # conclusion begins at last occurrence of one of the forms
    idx=[mm.start() for mm in re.finditer(r'(Per Dóminum nostrum Iesum|Per eú[mn]dem Dóminum|Qui tecum vivit|Qui vivis et regnas)',t)]
    if not idx: return t,''
    i=idx[-1]; return t[:i].rstrip(),t[i:]
def printed_conc(a,end):
    # the printed conclusion right after the body in the stream
    seg=[stream[x][0] for x in range(end,min(end+4,len(stream)))]
    return ' '.join(seg)
MON=['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
LP=[]; _p=0
for i,l in enumerate(lines):
    m_=re.match(r'@@PAGE (\d+)',l)
    if m_: _p=int(m_.group(1))+1
    LP.append(_p)
def daypages(md):
    mo=int(md[:2]); d=int(md[2:])
    ds=' ?'.join(str(d))
    pat=re.compile(r'^\s*(Die|Eadem die|Eadem Die)?\s*%s\s+%s'%(ds,MON[mo-1]))
    pg=[LP[i] for i,l in enumerate(lines) if re.search(r'Die\s+%s\s+%s\b'%(ds,MON[mo-1]),l) and LP[i]>150]
    return pg
def run(keys=None,rg=None):
    out={}
    for k,v in MM.items():
        if keys and k not in keys: continue
        dp=daypages(k[:4]) if k[:4].isdigit() else []
        RG=rg or (set(x for q in dp for x in (q-1,q,q+1,q+2)) if dp else range(1,700))
        for p in ('or','se','pc'):
            if p not in v: continue
            body,conc=split(v[p][0])
            T=toks(body); TF=[fold(t) for t in T]
            import difflib
            cands=[]
            for sk in (0,1,2):
                W=[w for w in TF[sk:] if w.isalpha()][:8]
                for a in range(len(F)):
                    if stream[a][1] not in RG or F[a]!=W[0]: continue
                    seq=[w for w in F[a:a+16] if w.isalpha()][:8]
                    if sum(x==y for x,y in zip(seq,W))>=5: cands.append((a,sk))
            if not cands: out[(k,p)]=('NOT FOUND',body[:60],conc[:30]); continue
            def score(c):
                a,sk=c; seg=F[a:a+len(TF)+12]; return difflib.SequenceMatcher(None,TF[sk:],seg,autojunk=False).ratio()
            a,sk=max(cands,key=score)
            seg=F[a:a+len(TF)+12]
            import difflib
            sm=difflib.SequenceMatcher(None,TF[sk:],seg,autojunk=False)
            bl=[x for x in sm.get_matching_blocks() if x.size]; end=bl[-1].b+bl[-1].size
            sm=difflib.SequenceMatcher(None,TF[sk:],seg[:end],autojunk=False)
            T2=T[sk:]
            d=[(op,' '.join(T2[max(0,i1-2):i2+2]),' '.join(t for t,_ in stream[a+max(0,j1-2):a+j2+2])) for op,i1,i2,j1,j2 in sm.get_opcodes() if op!='equal']
            out[(k,p)]=(stream[a][1],d,conc[:40],printed_conc(a,a+end))
    return out
if __name__=='__main__':
    o=run()
    for (k,p),r in o.items():
        if r[0]=='NOT FOUND': print(k,p,r); continue
        print(f'{k} {p} pdf{r[0]} conc[{r[2]}] printed[{r[3]}]')
        for x in r[1]: print('     ',x)
