import pickle, re, difflib
LEX=pickle.load(open('/tmp/dmv/lex.pkl','rb'))
exec(open('/tmp/dmv/lex.py').read().split('R=')[0])
def N(w):
    w=re.sub(r'(.)\1+',r'\1',w)
    w=w.replace('ch','c').replace('th','t').replace('ph','f').replace('intelleg','intellig').replace('mpn','mn')
    w=re.sub(r'ci(?=[aeiou])','ti',w)
    return w
LEXN={}
for w,c in LEX.items(): LEXN[N(w)]=LEXN.get(N(w),0)+c
def words(s): return [N(W(w)) for w in re.findall(r'[^\W\d_]+',s) if W(w)]
OCRP=set()
for a,b in [('rn','m'),('m','in'),('m','ni'),('u','li'),('u','ii'),('h','li'),('n','u'),('i','l'),('c','e'),('h','b'),('f','t'),('d','cl'),('m','nn'),('n','ii'),('i','t'),('l','t'),('in','m'),('ri','n'),('m','lli'),('m','iii'),('n','li'),('u','ri'),('n','ri')]:
    OCRP.add((a,b)); OCRP.add((b,a))
THIN=set('iltf')
def chardiff(f,g):
    sm=difflib.SequenceMatcher(None,f,g,autojunk=False); real=[]
    for t,a1,a2,b1,b2 in sm.get_opcodes():
        if t=='equal': continue
        a,b=f[a1:a2],g[b1:b2]
        if (a,b) in OCRP: continue
        if not a and len(b)==1 and b in THIN: continue
        if not b and len(a)==1 and a in THIN: continue
        real.append((a,b))
    return real
def compare(ours, dm):
    A,B=words(ours),words(dm)
    sm=difflib.SequenceMatcher(None,A,B,autojunk=False); real=[]; fuzzy=[]
    for t,a1,a2,b1,b2 in sm.get_opcodes():
        if t=='equal': continue
        a=''.join(A[a1:a2]); b=''.join(B[b1:b2])
        if a==b: continue
        if a1==len(A) and re.match(r'(per|qui|pe|j)',b): continue
        cd=chardiff(a,b)
        if not cd: continue
        dmw=B[b1:b2]
        if a and b and all(LEXN.get(w,0)==0 for w in dmw) and difflib.SequenceMatcher(None,a,b).ratio()>=0.7 and len(cd)<=2:
            fuzzy.append((' '.join(A[a1:a2]),' '.join(dmw))); continue
        real.append((' '.join(A[a1:a2]),' '.join(dmw)))
    return real,fuzzy
