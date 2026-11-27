import sys, re, difflib, json, collections
sys.path.insert(0,'/tmp/A5')
from missal import *
from lib import *
W=[(k,t) for k,t in enumerate(TK) if t.isalpha()]
G4=collections.defaultdict(list)
for n in range(len(W)-3):
    G4[tuple(t for _,t in W[n:n+4])].append(W[n][0])
CONC=re.compile(r'(Per (Dóminum|Dominum|eúndem|eúmdem|eumdem|eundem|Christum|ipsum|quem)|Qui (vivis|tecum|vivit|cum Patre))\b')
def split_conc(la):
    ms=list(CONC.finditer(la))
    for m in reversed(ms):
        if m.start()>len(la)*0.3 or len(la)<120:
            return la[:m.start()].rstrip(), la[m.start():]
    return la, ''
def locate_all(S):
    sw=[(i,t) for i,t in enumerate(S) if t.isalpha()]
    votes=collections.Counter(); first={}
    for a in range(0,max(1,len(sw)-3)):
        g=tuple(t for _,t in sw[a:a+4])
        cs=G4.get(g,[])
        if len(cs)>300: continue
        for c in cs:
            off=c - sw[a][0]; b=off//25; votes[b]+=1
            first[b]=min(first.get(b,off),off)
    if not votes: return []
    best=max(votes.values())
    return [max(0,first[b]-10) for b,v in votes.items() if v>=best*0.4]
def locate(S, near=None):
    sw=[(i,t) for i,t in enumerate(S) if t.isalpha()]
    votes=collections.Counter(); first={}
    for a in range(0,max(1,len(sw)-3)):
        g=tuple(t for _,t in sw[a:a+4])
        cs=G4.get(g,[])
        if len(cs)>300: continue
        for c in cs:
            off=c - sw[a][0]
            b=off//25
            votes[b]+=1
            first.setdefault(b,off)
            first[b]=min(first[b],off)
    if not votes: return None, 0
    best=max(votes.values())
    bs=[b for b,v in votes.items() if v>=best*0.8]
    if near: bs.sort(key=lambda b: abs(pdf[TL[max(0,first[b])]]-near))
    else: bs.sort(key=lambda b:-votes[b])
    return max(0,first[bs[0]]-10), len(bs)
def similar_join(a, b):
    return ''.join(a)==''.join(b) or difflib.SequenceMatcher(None,''.join(a),''.join(b)).ratio()>0.8 and len(b)>1
def compare(text, near=None, extra=60, at=None):
    S=toks(text)
    if at is not None: st,nc=at,0
    else: st,nc=locate(S,near)
    if st is None: return {'found':False}
    Wd=TK[st:st+len(S)+extra+20]
    sm=difflib.SequenceMatcher(None,S,Wd,autojunk=False)
    ops=sm.get_opcodes()
    # trim leading/trailing inserts
    while ops and ops[0][0]=='insert': ops=ops[1:]
    while ops and ops[-1][0]=='insert': ops=ops[:-1]
    diffs=[]
    for tag,i1,i2,j1,j2 in ops:
        if tag=='equal': continue
        a=S[i1:i2]; b=Wd[j1:j2]
        if tag=='replace' and all(x.isalpha() for x in a+b) and similar_join(a,b) and (len(b)>1 or len(a)>1): continue
        ctx=' '.join(S[max(0,i1-4):i1])
        diffs.append((tag,' '.join(a),' '.join(b),ctx, pdf[TL[st+j1]] if st+j1<len(TL) else None))
    end=st+(ops[-1][4] if ops else 0)
    after=' '.join(TK[end:end+14])
    return {'found':True,'pdf':pdf[TL[st]],'ncand':nc,'diffs':diffs,'after':after,'line':TL[st]}

def clean_diffs(r):
    out=[]
    for i,d in enumerate(r['diffs']):
        tag,a,b,ctx,pg=d
        if tag=='insert' and b.strip() in ('. c','c .','. c .','c','.  c'): continue
        if i==0 and tag=='replace' and len(a.split())==1:
            bt=b.split(); w=a
            if any(difflib.SequenceMatcher(None,''.join(bt[-k:]),w).ratio()>0.75 for k in range(1,min(8,len(bt))+1)): continue
        out.append(d)
    r['diffs']=out; return r
def srcpage(src):
    m=re.search(r'pp?\. (\d+\*?)',src or '')
    return p2pdf(m.group(1)) if m else None
def conc_type(c):
    f=fold(c)
    t='qui vivis' if f.startswith('qui vivis') else 'qui tecum' if f.startswith('qui tecum') else 'per eundem' if re.match(r'per eu[mn]dem',f) else 'per dominum' if f.startswith('per dominum') else f[:15]
    return t+(' +eiusdem' if 'eiusdem' in f or 'eiúsdem' in f else '')
def mconc(after):
    a=after.split()
    t=' '.join(a[:2]).replace('eumdem','eundem')
    tail=' '.join(a[:16])
    m=re.match(r'(per dominum|per eundem|qui vivis|qui tecum|per christum)',t)
    return (m.group(1) if m else '?'+t)+(' +eiusdem' if re.search(r'^[^.]*\. ?\.? ?\.? ?in unitate eiusdem|eiusdem',' '.join(a[:12])) else '')
def run(keys):
    res={}
    for k in keys:
        out={'or':{},'rd':[]}
        if k in O:
            near=srcpage(O[k].get('src'))
            for p in ('or','se','pc'):
                if p not in O[k]: continue
                la=O[k][p][0]
                b,c=split_conc(la)
                r=compare(b,near)
                if r['found']: clean_diffs(r); r['conc_site']=conc_type(c); r['conc_m']=mconc(r['after'])
                out['or'][p]=r
        for it in R.get(k,[]):
            rs=compare_best(it['title']+' '+it['la'])
            r=rs[0] if rs else {'found':False}
            if rs: r['alts']=[(x['pdf'],len(x['diffs'])) for x in rs[1:6]]
            r['ref']=it['ref']; out['rd'].append(r)
        res[k]=out
    return res

def compare_best(text):
    S=toks(text); rs=[]
    for st in locate_all(S):
        r=compare(text,at=st)
        if r['found']: clean_diffs(r); rs.append(r)
    rs.sort(key=lambda r:len(r['diffs']))
    return rs

def compare_near(text, near):
    S=toks(text); best=None
    for st in locate_all(S):
        d=abs(pdf[TL[st]]-near)
        if best is None or d<best[0]: best=(d,st)
    if best is None: return {'found':False}
    r=compare(text,at=best[1]); clean_diffs(r); return r
def show(k, near, near_rd=None, parts=('or','se','pc'), out=print):
    near_rd=near_rd or near
    out(f"=== {k} | {M[k]['title'] if k in M else ''} | near {near}")
    if k in O:
        for p in parts:
            if p not in O[k]: continue
            b,c=split_conc(O[k][p][0]); r=compare_near(b,near)
            if not r['found']: out(f'  {p}: NOT FOUND'); continue
            out(f"  {p}: pdf{r['pdf']} L{r['line']} conc site={conc_type(c)} m={mconc(r['after'])}")
            for d in r['diffs']: out(f"     {d[0]} [{d[1]}] -> [{d[2]}]  ctx: {d[3]}")
    for it in R.get(k,[]):
        r=compare_near(it['title']+' '+it['la'],near_rd)
        if not r['found']: out(f"  RD {it['ref']}: NOT FOUND"); continue
        out(f"  RD {it['ref']}: pdf{r['pdf']} L{r['line']} after: {r['after'][:70]}")
        for d in r['diffs']: out(f"     {d[0]} [{d[1][:300]}] -> [{d[2][:300]}]  ctx: {d[3]}")
