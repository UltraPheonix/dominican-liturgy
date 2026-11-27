import sys,re,difflib; sys.path.insert(0,'/tmp/A5')
from cmp import *
TOKRE=re.compile(r"[^\W\d_]+|[,;:.?!]")
def otoks(s):
    out=[]
    for m in TOKRE.finditer(s):
        f=toks(m.group())
        if len(f)!=1: f=[''.join(f)] if f else ['']
        out.append((f[0],m.start(),m.end()))
    return out
JUNK=set('c'.split())
def autofix(s, near, body_end=None):
    """s: site string (may include conclusion; pass body_end to restrict). Returns (new_s, applied, manual, r)"""
    body=s if body_end is None else s[:body_end]
    T=otoks(body); S=[t[0] for t in T]
    # locate
    best=None
    for st in locate_all(S):
        d=abs(pdf[TL[st]]-near) if near else 0
        if best is None or d<best[0]: best=(d,st)
    if best is None: return s,[],['NOT FOUND'],None
    st=best[1]; W=TK[st:st+len(S)+80]
    ops=difflib.SequenceMatcher(None,S,W,autojunk=False).get_opcodes()
    while ops and ops[0][0]=='insert': ops=ops[1:]
    while ops and ops[-1][0]=='insert': ops=ops[:-1]
    edits=[]; manual=[]
    P=set(',;:.?!')
    for tag,i1,i2,j1,j2 in ops:
        if tag=='equal': continue
        a=S[i1:i2]; b=W[j1:j2]; pg=pdf[TL[st+j1]] if st+j1<len(TL) else None
        ctx=' '.join(S[max(0,i1-4):i1])
        if all(x in P for x in a) and all(x in P for x in b) and len(a)<=1 and len(b)<=1:
            edits.append((tag,i1,a,b,pg,ctx))
        else:
            # ignore drop-cap / letterspacing noise
            if tag=='replace' and all(x.isalpha() for x in a+b) and (''.join(a)==''.join(b) or (len(b)>1 and difflib.SequenceMatcher(None,''.join(a),''.join(b)).ratio()>0.8)): continue
            if tag=='insert' and ' '.join(b) in ('. c','c .','. c .','c','. , c'): continue
            if i1==0 and tag=='replace' and len(a)==1 and any(difflib.SequenceMatcher(None,''.join(b[-k:]),a[0]).ratio()>0.75 for k in range(1,min(8,len(b))+1)): continue
            manual.append((tag,' '.join(a),' '.join(b),pg,ctx))
    # apply edits from the end
    new=body
    for tag,i1,a,b,pg,ctx in sorted(edits,key=lambda e:-e[1]):
        if tag=='insert':
            pos=T[i1-1][2]; new=new[:pos]+b[0]+new[pos:]
        elif tag=='delete':
            _,s0,e0=T[i1]; 
            # remove the char and a following space if the punct is followed by space and preceded by word
            new=new[:s0]+new[e0:]
        else:
            _,s0,e0=T[i1]; new=new[:s0]+b[0]+new[e0:]
            if b[0] in '.?!' and a[0] not in '.?!' and i1+1<len(T):
                ns=T[i1+1][1]; 
                if new[ns].islower(): new=new[:ns]+new[ns].upper()+new[ns+1:]
            if a[0] in '.?!' and b[0] in ',;:' and i1+1<len(T):
                ns=T[i1+1][1]
                if new[ns].isupper() and T[i1+1][0] in ('et','qui','quia','sed','non','ut','si','nam','quod','in','ad','cum','sicut','quoniam','ego','tunc','dixit','haec','hic','ecce','propter','omnis','omnes','nisi','vos','quis','quid','aut','vel','nos','ac','atque','ita','beatus','beati','iam','quae','quem','neque','nec','dico','amen','illi','ille','ipse','autem','enim','fratres','alioquin','sic'):
                    new=new[:ns]+new[ns].lower()+new[ns+1:]
    new=re.sub(r' +([,;:.?!])',r'\1',new)
    after=' '.join(TK[st+(ops[-1][4] if ops else 0): st+(ops[-1][4] if ops else 0)+12])
    return new+s[len(body):] if body_end is not None else new, edits, manual, {'pdf':pdf[TL[st]],'after':after}
