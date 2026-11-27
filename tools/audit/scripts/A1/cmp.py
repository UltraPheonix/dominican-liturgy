import json, re, sys, unicodedata, difflib, collections
ROOT='/home/claude/dominican-liturgy/'
def load(fn):
    s=open(ROOT+fn,encoding='utf8').read()
    i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end()
    j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
def fold(w):
    w=w.replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('Œ','oe').replace('ǽ','ae').replace('Ǽ','ae')
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if not unicodedata.combining(c))
    w=w.lower().replace('j','i').replace('v','u')
    return re.sub(r'[^a-z0-9]','',w)
PUN=',;:.?!'
def toks_site(t):
    out=[]
    for m in re.finditer(r"([^\s,;:.?!()\[\]«»“”\"]+)\s*([,;:.?!]*)",t):
        f=fold(m.group(1))
        if not f:
            if out and m.group(2): out[-1][1]+=m.group(2)
            continue
        out.append([f,m.group(2),m.group(1),m.start(1),m.end(1),m.start(2),m.end(2)])
    return out
S=json.load(open('/tmp/A1/stream.json'))
# Missal tokens
MT=[]  # [fold, punct, raw, streamidx]
i=0
def isup(w): 
    a=re.sub(r'[^A-Za-z]','',w); return a and a.isupper()
pend=None
toks=[]
for k,w in enumerate(S):
    if w[4]<66 and w[6]<1.5: continue
    if w[5].startswith('Pr') and w[5].endswith('d.') and w[2]>600: continue
    toks.append([w[5],k,w[6]])
# drop caps
j=0; T2=[]
skip=set()
for k,(raw,si,h) in enumerate(toks):
    if k in skip: continue
    if h>1.6 and re.fullmatch(r'[A-Z]',raw):
        if k+1<len(toks) and isup(toks[k+1][0]) and S[toks[k+1][1]][0]==S[si][0]:
            toks[k+1][0]=raw+toks[k+1][0]; continue
        # back search
        done=False
        for b in range(len(T2)-1,max(-1,len(T2)-9),-1):
            if isup(T2[b][0]) and S[T2[b][1]][0]==S[si][0] and len(re.sub(r'[^A-Za-z]','',T2[b][0]))<=6:
                T2[b][0]=raw+T2[b][0]; done=True; break
        if done: continue
    T2.append([raw,si,h])
# hyphen joins & split punctuation
merged=[]
k=0
while k<len(T2):
    raw,si,h=T2[k]
    sis=[si]
    while (raw.endswith('­') or raw.endswith('-')) and k+1<len(T2):
        k+=1; raw=raw.rstrip('­-')+T2[k][0]; sis.append(T2[k][1])
    merged.append((raw,sis)); k+=1
for raw,sis in merged:
    for m in re.finditer(r"([^\s,;:.?!]+)?([,;:.?!]*)",raw):
        if not m.group(0): continue
        f=fold(m.group(1) or '')
        if not f:
            if MT and m.group(2): MT[-1][1]+=m.group(2)
            continue
        MT.append([f,m.group(2),m.group(1),sis])
MF=[t[0] for t in MT]
idx=collections.defaultdict(list)
for p in range(len(MF)-2): idx[(MF[p],MF[p+1],MF[p+2])].append(p)
def pdf(p): return S[MT[p][3][0]][0]
def locate(st, lo=None, hi=None):
    f=[t[0] for t in st]
    votes=collections.Counter()
    for a in range(len(f)-2):
        for p in idx.get((f[a],f[a+1],f[a+2]),[]):
            if lo is not None and not (lo<=pdf(p)<=hi): continue
            votes[(p-a)//8]+=1
    return votes
def align(st, start):
    f=[t[0] for t in st]
    a0=max(0,start-10); a1=min(len(MF),start+int(len(f)*1.25)+30)
    sm=difflib.SequenceMatcher(None,f,MF[a0:a1],autojunk=False)
    ops=sm.get_opcodes()
    # trim leading/trailing missal-only
    return ops,a0
