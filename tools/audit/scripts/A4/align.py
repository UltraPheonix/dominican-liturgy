import re, difflib, collections
from tok import *
W=[(n,t[0]) for n,t in enumerate(MS) if t[0] not in ',;:.?!']
TRI=collections.defaultdict(list)
for a in range(len(W)-2):
    TRI[(W[a][1],W[a+1][1],W[a+2][1])].append(a)
WPOS=[n for n,_ in W]
CONCL=re.compile(r'\s*(Per (?:Dóminum|eúndem|eúmdem|Christum)|Qui (?:vivis|tecum|vivit|cum)|qui tecum vivit)\b(?!.*\b(?:Per Dóminum|Per eúndem|Qui vivis)\b).*$')
def site_toks(s):
    return [(fold(t),t) for t,_ in toks(s)]
def locate(st, expect_line=None, win=None):
    sw=[f for f,_ in st if f not in ',;:.?!']
    votes=collections.Counter()
    for o in range(0,max(1,len(sw)-2)):
        for a in TRI.get(tuple(sw[o:o+3]),[]):
            if win and not (win[0]<=MS[WPOS[a]][2]<=win[1]): continue
            votes[a-o]+=1
    if not votes: return None,0
    best=max(votes.values())
    cands=[a for a,v in votes.items() if v>=best*0.6]
    if expect_line is not None:
        cands.sort(key=lambda a:(-(votes[a]>=best*0.9), abs(MS[WPOS[max(0,min(a,len(W)-1))]][2]-expect_line)))
    else: cands.sort(key=lambda a:-votes[a])
    a=max(0,cands[0]); return WPOS[a], votes[cands[0]]/max(1,len(sw)-2)
def compare(s, expect_line=None, extra=40, win=None):
    st=site_toks(s)
    start,score=locate(st,expect_line,win)
    if start is None and win: start,score=locate(st,expect_line)
    if start is None: return None
    lo=max(0,start-8); hi=start+len(st)+extra
    mt=MS[lo:hi]
    a=[f for f,_ in st]; b=[t[0] for t in mt]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    ops=sm.get_opcodes()
    eq=[o for o in ops if o[0]=='equal']
    if not eq: return None
    b0=eq[0][3]-eq[0][1] if eq[0][1]>0 else eq[0][3]   # align start
    b1=eq[-1][4]+(len(a)-eq[-1][2])
    diffs=[]
    for tag,i1,i2,j1,j2 in ops:
        if tag=='equal':
            for x in range(i2-i1):
                ra=st[i1+x][1]; rb=mt[j1+x][1]
                if ra[0].isalpha() and rb[0].isalpha() and not rb.isupper() and (lo+j1+x)>start and ra[0].isupper()!=rb[0].isupper() and len(rb)>1:
                    diffs.append(('case',ra,rb,' '.join(y for _,y in st[max(0,i1+x-3):i1+x]),mt[j1+x][2],lo+j1+x,lo+j1+x+1,i1+x,i1+x+1))
            continue
        if j2<=b0 and i1==0 and tag=='insert': continue
        if j1>=b1 and tag=='insert': continue
        sa=' '.join(x for _,x in st[i1:i2]); sb=' '.join(t[1] for t in mt[j1:j2])
        ctx=' '.join(x for _,x in st[max(0,i1-3):i1])
        diffs.append((tag,sa,sb,ctx, mt[min(j1,len(mt)-1)][2], lo+j1, lo+j2, i1, i2))
    ln=mt[min(max(b0,0),len(mt)-1)][2]
    return dict(spos=[(p,p+len(t)) for t,p in toks(s)],score=score,line=ln,page=pageof(ln),diffs=diffs,end=mt[min(b1,len(mt)-1)][2],endi=lo+min(b1,len(mt)))
