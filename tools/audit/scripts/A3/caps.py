# capitals as printed: case differences of the first letter of aligned (equal) words
import difflib, re
from m39 import stream
UP={'á':'A','é':'E','í':'I','ó':'O','ú':'U','ý':'Y','ǽ':'Æ'}
def capdiffs(S, r):
    score,end,ops,k=r
    M=stream[k:end]
    a=[f for f,o in S]; b=[t[0] for t in M]
    out=[]
    for t,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if t!='equal': continue
        for n in range(i2-i1):
            i=i1+n; j=j1+n
            so=S[i][1]; mo=M[j][1]
            if not so[0].isalpha() or i==0: continue
            if len(mo)>1 and mo.isupper(): continue     # small caps / drop cap incipit
            if mo.endswith('*'): continue
            if so[0].isupper()!=mo[0].isupper():
                out.append((i, so, mo, k+j))
    return out
def apply(text, sp, cds, skip=()):
    s=list(text)
    for n,(i,so,mo,kk) in enumerate(cds):
        if n in skip: continue
        p=sp[i][0]; c=s[p]
        s[p]=(UP.get(c,c.upper())) if mo[0].isupper() else c.lower()
    return ''.join(s)
