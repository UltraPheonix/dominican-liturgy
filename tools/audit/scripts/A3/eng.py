import re, json, bisect, difflib
import m39
from m39 import stream, toks, find, where, L, TOK, fold
from cmp import align, split_concl, fz
import region as RG
LINES=[t[2] for t in stream]
def sidx(line): return bisect.bisect_left(LINES, line)
# printed page -> pdf index
P2PDF={}
for p,v in m39.pdfleft.items():
    star=v.endswith('*'); n=int(v.rstrip('*'))
    P2PDF[(n,star)]=p; P2PDF[(n+1,star)]=p
def pdf_of(pg):
    s=str(pg).strip(); star=s.endswith('*'); n=int(s.rstrip('*'))
    if (n,star) in P2PDF: return P2PDF[(n,star)]
    # interpolate
    ks=sorted(k for k in P2PDF if k[1]==star)
    lo=max((k for k in ks if k[0]<n), default=None)
    return P2PDF[lo]+ (n-lo[0])//2 if lo else None
def page_range(pdf):
    """stream index range for a pdf page"""
    idx=[i for i,t in enumerate(stream) if t[3]==pdf]
    return (idx[0], idx[-1]) if idx else None
_pr={}
def prange(pdf):
    if pdf not in _pr:
        a=bisect.bisect_left([t[3] for t in stream] if False else PDFS, pdf); b=bisect.bisect_right(PDFS,pdf)
        _pr[pdf]=(a,b)
    return _pr[pdf]
PDFS=[t[3] for t in stream]
def mass_ranges(month, day, extra_pages=()):
    rs=[]
    for a,b in RG.region(month,day):
        rs.append((sidx(a),sidx(b),0.25))
        # pages referenced in the region
        txt=' '.join(L[a:b])
        for m in re.finditer(r'pag\.\s*(\d+\*?)', txt):
            p=pdf_of(m.group(1))
            if p is not None:
                for q in (p,p+1): rs.append(prange(q)+(0.12,))
    for pg in extra_pages:
        p=pdf_of(pg)
        if p is not None:
            for q in (p,p+1): rs.append(prange(q)+(0.2,))
    return rs
def best_match(text, ranges=(), extra=60, prefer=0.15):
    S=toks(text)
    if not S: return S,None
    cands=find(S, None, 60)
    best=None
    for k in cands:
        r=align(S,k,extra)
        bon=max([w for a,b,w in ranges if a<=r[3]<b] or [0])
        inr=bon>0
        sc=r[0]+bon
        if best is None or sc>best[0]: best=(sc,r,inr)
    if best is None:
        for off in (6,12,25):
            if len(S)>off+8:
                for k in find(S[off:],None,30):
                    r=align(S,max(0,k-off*2),extra+off*2)
                    bon=max([w for a,b,w in ranges if a<=r[3]<b] or [0])
                    inr=bon>0
                    sc=r[0]+bon
                    if best is None or sc>best[0]: best=(sc,r,inr)
            if best: break
    if best is None: return S,None
    return S,(best[1],best[2])
def render(ts):
    out=''
    for f,o in ts:
        if f in ':;,.!?)':
            out=out.rstrip()+o
        elif out and not out.endswith('('): out+=' '+o
        else: out+=o
        if f in ':;,.!?)': pass
    return out
def spans(text):
    s=text.replace('\xad','')
    return [(m.start(),m.end()) for m in TOK.finditer(text)]
def propose(text, S, res, acc=None, skip=(), over=None):
    """apply Missal ops to site text. returns new text and list of (op, siteseg, missalseg, k_missal)"""
    score,end,ops,k=res
    M=stream[k:end]
    sp=spans(text); assert len(sp)==len(S), (len(sp),len(S))
    new=text; changes=[]
    ops2=sorted(ops, key=lambda o:(o[1],o[3]))
    for idx in range(len(ops2)-1,-1,-1):
        tag,i1,i2,j1,j2=ops2[idx]
        mt=[(t[0],t[1]) for t in M[j1:j2]]
        changes.append((tag,' '.join(o for f,o in S[i1:i2]),' '.join(o for f,o in mt),k+j1))
        if idx in skip: continue
        mt2=[]
        for f,o in mt:
            if f[0].isalpha():
                w=(acc or {}).get(f,o)
                if o[0].isupper() and len(o)>1 and o[1:].islower(): w=w[0].upper()+w[1:]
                elif o.isupper() and len(o)>2: w=w  # all caps garble: keep dict form
                mt2.append((f,w))
            else: mt2.append((f,o))
        seg=render(mt2)
        if over and idx in over: seg=over[idx]; mt2=toks(seg) if seg else []
        if tag=='replace' and not mt2: tag='delete'
        if tag=='insert':
            pos=sp[i1-1][1] if i1>0 else 0
            ins=seg if (mt2 and mt2[0][0] in ':;,.!?)') else ' '+seg
            new=new[:pos]+ins+new[pos:]
        else:
            a=sp[i1][0]; b=sp[i2-1][1]
            if tag=='delete':
                # remove the tokens; fix double spaces
                if S[i1][0][0].isalpha():
                    if a>0 and new[a-1]==' ': a-=1
                new=new[:a]+new[b:]
            else:
                if mt2 and mt2[0][0] in ':;,.!?)' and S[i1][0][0].isalpha() and a>0 and new[a-1]==' ': a-=1
                if mt2 and mt2[0][0][0].isalpha() and not S[i1][0][0].isalpha(): seg=' '+seg if not new[a-1:a]==' ' else seg
                new=new[:a]+seg+new[b:]
    new=re.sub(r'  +',' ',new)
    return new, changes[::-1]

from cmp import before, after
