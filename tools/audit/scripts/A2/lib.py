import json, re, unicodedata, difflib, os
ROOT='/home/claude/dominican-liturgy'
def load(fn):
    s=open(os.path.join(ROOT,fn),encoding='utf8').read()
    i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end(); j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
def fold(w):
    w=w.replace('æ','ae').replace('Æ','ae').replace('œ','oe').replace('Œ','oe').replace('ǽ','ae').replace('Ǽ','ae')
    w=unicodedata.normalize('NFD',w)
    w=''.join(c for c in w if unicodedata.category(c)!='Mn').lower()
    return w.replace('j','i').replace('v','u')
TOK=re.compile(r"[A-Za-zÀ-ÿĀ-žǼǽæœÆŒ]+|[,;:.!?]")
def toks(s): return TOK.findall(s)
# Missal token stream
lines=open(ROOT+'/tools/orat39/m39lin.txt',encoding='utf8').read().split('\n')
MT=[]; MP=[]; ML=[]  # token, page(@@PAGE n), line no
page=0; carry=''
SKIP=set()
for ln,l in enumerate(lines,1):
    if re.match(r'^\s*\d{1,3}\s*$',l):
        SKIP.add(ln)
        nx=lines[ln] if ln<len(lines) else ''
        if len(nx.strip())<48 and re.match(r'^[A-Z]',nx.strip() or 'x') and ':' not in nx and not nx.isupper(): SKIP.add(ln+1)
    if re.match(r'^\s*Pr\S{0,3}d\.?\s*$',l) or re.match(r'^\s*Praed\.',l): SKIP.add(ln)
HDR=set(lines[ln-1].strip() for ln in SKIP if not re.match(r'^\s*\d',lines[ln-1]))
HDR={h for h in HDR if len(h.split())>=2}
for ln,l in enumerate(lines,1):
    if l.startswith('@@PAGE'):
        page=int(l.split()[1]); continue
    if ln in SKIP or l.strip() in HDR: continue
    t=l.rstrip()
    # join hyphenation
    if carry:
        t=carry+t.lstrip(); carry=''
    if re.search(r'[A-Za-z][­-]\s*$',t) :
        m=re.search(r'(\S+)[­-]\s*$',t)
        carry=m.group(1); t=t[:m.start()]
    for w in toks(t):
        MT.append(w); MP.append(page); ML.append(ln)
MF=[fold(w) for w in MT]
def find(words, lo=0, hi=None):
    """positions where folded words sequence occurs"""
    hi=hi or len(MF); n=len(words); out=[]
    for i in range(lo,hi-n):
        if MF[i]==words[0] and MF[i:i+n]==words: out.append(i)
    return out
WI=[i for i,w in enumerate(MF) if w[0].isalpha()]
WF=[MF[i] for i in WI]
WS=' '.join(WF)
import bisect
_offs=[]; o=0
for w in WF: _offs.append(o); o+=len(w)+1
def findw(words):
    """token indices (into MT) where the word sequence starts"""
    pat=' '.join(words); out=[]; st=0
    while True:
        k=WS.find(pat,st)
        if k<0: break
        j=bisect.bisect_left(_offs,k)
        if j<len(_offs) and _offs[j]==k: out.append(WI[j])
        st=k+1
    return out
