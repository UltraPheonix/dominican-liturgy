import difflib, re
import m39
from m39 import stream, toks, find, where
CONC=re.compile(r'\s*\b(Per (?:Dóminum|Dominum|eúmdem|eúndem|eumdem|eundem|Christum|ipsum)|Qui (?:vivis|tecum|vivit|cum Patre|cum Deo)|qui tecum vivit)\b(?!.*\b(?:Per Dóminum|Per eúndem|Per eúmdem|Qui vivis|Qui tecum)\b).*$')
def split_concl(la):
    m=CONC.search(la)
    if not m: return la, ''
    return la[:m.start()], la[m.start():].strip()
def fz(s):
    s=s.replace(' ','').replace('rn','m').replace('l','i').replace('1','i').replace('*','')
    return s
def align(S, k, extra=60):
    k0=max(0,k-15)
    M=stream[k0:k+int(len(S)*1.4)+extra]
    a=[f for f,o in S]; b=[t[0] for t in M]
    bl=[x for x in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks() if x.size>=2]
    if bl: k=max(0,k0+bl[0].b-bl[0].a)
    return align0(S,k,extra)
def align0(S, k, extra=60):
    M=stream[k:k+int(len(S)*1.4)+extra]
    a=[f for f,o in S]; b=[t[0] for t in M]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    bl=[x for x in sm.get_matching_blocks() if x.size]
    if not bl: return 0,k,[],k
    end=bl[-1].b+bl[-1].size
    rem=len(a)-(bl[-1].a+bl[-1].size)
    while rem>0 and end<len(b):
        if b[end] in ':.;' and end+1<len(b) and b[end+1] in ('per','qui'): break
        if b[end] in ('per','qui') and end+1<len(b) and b[end+1] in ('dominum','eumdem','eundem','vivis','tecum'): break
        end+=1; rem-=1
    # trim: missal end = end of last block that is matched near the end of S
    sm2=difflib.SequenceMatcher(None,a,b[:end],autojunk=False)
    ops=[]
    for o in sm2.get_opcodes():
        if o[0]=='equal': continue
        t,i1,i2,j1,j2=o
        sa=fz(''.join(a[i1:i2])); mb=fz(''.join(b[j1:j2]))
        if sa==mb: continue
        if i1==0 and t=='replace' and sa.endswith(mb): continue   # drop-cap garble
        ops.append(o)
    matched=sum(x.size for x in sm2.get_matching_blocks())
    return matched/max(1,len(a)), k+end, ops, k
def compare(text, near=None, extra=60):
    S=toks(text)
    if not S: return None
    best=None
    for k in find(S, near):
        r=align(S,k,extra)
        if best is None or r[0]>best[0]+1e-9: best=r
    if best is None:
        # try from later words (garbled incipit)
        for off in (5,10,20):
            if len(S)>off+8:
                for k in find(S[off:], near):
                    r=align(S, max(0,k-off*2), extra+off*2)
                    if best is None or r[0]>best[0]: best=r
            if best: break
    return S,best
def show(S,best,ctx=3):
    score,end,ops,k=best
    M=stream[k:end]
    out=[]
    for tag,i1,i2,j1,j2 in ops:
        s=' '.join(o for f,o in S[max(0,i1-ctx):i1])
        sa=' '.join(o for f,o in S[i1:i2]); mb=' '.join(t[1] for t in M[j1:j2])
        out.append('   %s site[%s] missal[%s]  ...%s  @%s'%(tag,sa,mb,s, where(k+j1)))
    return out
def after(end,n=10):
    return ' '.join(t[1] for t in stream[end:end+n])
def before(k,n=8):
    return ' '.join(t[1] for t in stream[max(0,k-n):k])
