import sys; sys.path.insert(0,'/tmp/A2')
from cmp2 import *
from collections import Counter, defaultdict
acc=defaultdict(Counter)
def walk(x):
    if isinstance(x,str):
        for w in TOK.findall(x):
            if w[0].isalpha(): acc[fold(w)][w.lower()]+=1
    elif isinstance(x,list):
        for y in x: walk(y)
    elif isinstance(x,dict):
        for y in x.values(): walk(y)
walk(O); walk(R)
def accent(w):
    c=acc.get(fold(w))
    if not c: return None
    a=c.most_common(1)[0][0]
    return a[0].upper()+a[1:] if w[0].isupper() else a
def ocrn(w):
    w=fold(w); return w.replace('rn','m').replace('cc','oe').replace('ce','oe').replace('li','h')
def render(tt):
    out=''
    for t in tt:
        if t[0].isalpha(): out+=(' ' if out else '')+t
        else: out+=t
    return out
def propose(txt, s):
    spans=[(m.start(),m.end(),m.group()) for m in TOK.finditer(txt)]
    site=[x[2] for x in spans]
    sf=[fold(w) for w in site]
    W=len(site)+40+len(site)//6
    win=MT[s:s+W]; wf=MF[s:s+W]
    sm=difflib.SequenceMatcher(None,sf,wf,autojunk=False)
    bl=[b for b in sm.get_matching_blocks() if b.size]
    end=bl[-1].b+bl[-1].size; st=bl[0].b
    if end<len(wf) and not wf[end][0].isalpha() and sf and sf[-1][0].isalpha(): end+=1
    mt=win[st:end]; mf=wf[st:end]
    sm=difflib.SequenceMatcher(None,sf,mf,autojunk=False)
    edits=[]; notes=[]
    ops=sm.get_opcodes()
    for oi,(op,i1,i2,j1,j2) in enumerate(ops):
        S=site[i1:i2]; Mx=mt[j1:j2]
        if op=='equal':
            for k,(a,b) in enumerate(zip(S,Mx)):
                i=i1+k
                if a[0].isalpha() and i>0 and not (len(b)>1 and b.isupper()) and a[0].isupper()!=b[0].isupper() and not (a[0] in 'íÍ' and b[0]=='I'):
                    a2=(a[0].upper() if b[0].isupper() else a[0].lower())+a[1:]
                    notes.append(('case',a,a2)); edits.append((spans[i][0],spans[i][1],a2))
            continue
        if oi==0 and op=='delete' and i1==0: notes.append(('start?',' '.join(S),'')); continue
        if not S and all(w in ('C','S','F','h','N','I','L') for w in Mx): continue
        if not S and len(Mx)<=2 and all(w in ('C','S') or not w[0].isalpha() for w in Mx): continue
        sw=[w for w in S if w[0].isalpha()]; mw=[w for w in Mx if w[0].isalpha()]
        if sw and [ocrn(w) for w in sw]==[ocrn(w) for w in mw]:
            it=iter(sw); rep=[next(it) if w[0].isalpha() else w for w in Mx]
        elif sw and ocrn(''.join(sw))==ocrn(''.join(mw)):
            notes.append(('split?',' '.join(S),' '.join(Mx)))
            # keep site words, take missal punct structure only if trivial
            continue
        elif not sw and not mw:
            g=s+st+j1-1
            if not Mx and 0<=g<len(ML)-1 and ML[g]!=ML[g+1]:
                notes.append(('eol?',' '.join(site[max(0,i1-2):i2+1]),'kept')); continue
            if Mx and all(w in ('.',) for w in Mx) and S==[','] and 0<=g<len(ML)-1 and ML[g+1]!=ML[g+2]:
                notes.append(('eol?',' '.join(site[max(0,i1-2):i2+1]),'kept')); continue
            rep=Mx; notes.append(('punct',' '.join(site[max(0,i1-2):i2+1]),' '.join(Mx) or '∅'))
        else:
            JUNK=re.compile(r'^(Feria|Dominica|Domin|Septembris|Ps|Pr\S?\S?d|Hic|pausatur|aliquantulum|aliquántulum|genu\S*ectitur|post|Pascha|Pentecosten|Pentecostes|quinta|sexta|tertia|quarta|secunda|Hebdomadae|Sanctae|Quadrag|Passionis|Oct|Octavam|T|C|S|W|E|i|h|F)$')
            mw_=[w for w in Mx if w[0].isalpha()]
            if not sw and mw_ and (all(JUNK.match(w) for w in mw_) or 'pausatur' in mw_):
                notes.append(('junk',' '.join(Mx),''))
                pm=[w for w in Mx if not w[0].isalpha()]
                if [w for w in S if not w[0].isalpha()]==pm or (not S and not pm): continue
                if S and any(w[0].isalpha() for w in S): continue
                rep=pm
                r=render(rep)
                if i1<i2: edits.append((spans[i1][0],spans[i2-1][1],r))
                else:
                    a=spans[i1-1][1] if i1>0 else 0; edits.append((a,a,r))
                continue
            if sw and len(sw)==len(mw_) and all(difflib.SequenceMatcher(None,fold(a),fold(b)).ratio()>=0.6 and (fold(b) not in acc) for a,b in zip(sw,mw_)):
                notes.append(('VAR?',' '.join(S),' '.join(Mx))); continue
            rep=[]
            for w in Mx:
                if w[0].isalpha():
                    a=accent(w); rep.append(a if a else w+'¿')
                else: rep.append(w)
            notes.append(('WORD',' '.join(site[max(0,i1-3):i2+3]),' '.join(S)+' => '+' '.join(rep)))
        r=render(rep)
        if i1<i2:
            a,b=spans[i1][0],spans[i2-1][1]
            if rep and rep[0][0].isalpha() and not S[0][0].isalpha(): r=' '+r if txt[a-1:a]!=' ' else r
            if not rep and i2<len(spans) and S[0][0].isalpha():  # deleting words: eat following space
                b=spans[i2][0]
            edits.append((a,b,r))
        else:
            a=spans[i1-1][1] if i1>0 else 0
            if rep and rep[0][0].isalpha(): r=' '+r
            edits.append((a,a,r))
    out=txt
    for a,b,r in sorted(edits,key=lambda e:(e[0],e[1]),reverse=True):
        out=out[:a]+r+out[b:]
    out=re.sub(r' +',' ',out)
    return out, notes, s+st, s+end, sm.ratio()
