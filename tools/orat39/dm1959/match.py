import pickle, re, json, difflib, collections, unicodedata, sys
sys.path.insert(0,'/tmp'); from dmv_load import loadjs
pairs,_,_=pickle.load(open('/tmp/dmv/pairs.pkl','rb'))
CL=re.compile(r'(Per\s+(Dominum|D[o0]min|eumdem|eundem|Christum|eund|eumd)|Qui\s+(vivis|tecum|vivit|cum\s+Deo|cum\s+Patre|vivi)|J>er Dominum)')
CLS=re.compile(r'\s*(Per (?:Dóminum|eúndem|eúmdem|Christum)|Qui (?:vivis|tecum|vivit)|qui tecum vivit|Dóminum nostrum I[eé]sum Christum Fílium tuum: Qui)\b(?!.*\b(?:Per Dóminum|Per eúndem|Qui vivis)\b).*$')
def F(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    s=s.replace('æ','ae').replace('œ','oe').replace('Æ','ae').replace('Œ','oe').lower()
    s=re.sub(r'[^a-z]','',s).replace('j','i').replace('v','u').replace('y','i')
    return s.replace('ae','e').replace('oe','e')
def labody(t):
    ms=list(CL.finditer(t))
    return t[:ms[-1].start()] if ms else t
DM=[]
for x in pairs:
    b=labody(x['la']); DM.append(dict(x, f=F(b)))
idx=collections.defaultdict(set)
for i,d in enumerate(DM):
    f=d['f']
    for k in range(0,max(1,len(f)-8),3): idx[f[k:k+8]].add(i)
def cands(f):
    c=collections.Counter()
    for k in range(0,max(1,len(f)-8),2):
        for i in idx.get(f[k:k+8],()): c[i]+=1
    return [i for i,_ in c.most_common(8)]
def best(la):
    m=CLS.search(la); body=la[:m.start()] if m else la
    f=F(body); out=[]
    for i in cands(f):
        r=difflib.SequenceMatcher(None,f,DM[i]['f'],autojunk=False).ratio(); out.append((r,i))
    out.sort(reverse=True)
    return f,out

OCRP=set()
for a,b in [('rn','m'),('m','in'),('m','ni'),('u','li'),('u','ii'),('h','li'),('n','u'),('i','l'),('c','e'),('h','b'),('f','t'),('d','cl'),('m','nn'),('n','ii'),('i','t'),('l','t'),('in','m'),('ri','n')]:
    OCRP.add((a,b)); OCRP.add((b,a))
THIN=set('iltf')
def diffs(f,g):
    sm=difflib.SequenceMatcher(None,f,g,autojunk=False); real=[]; ocr=[]
    for t,a1,a2,b1,b2 in sm.get_opcodes():
        if t=='equal': continue
        a,b=f[a1:a2],g[b1:b2]
        ok=False
        if (a,b) in OCRP: ok=True
        elif not a and len(b)==1 and (b in THIN or (b1>0 and g[b1-1]==b) or g[b2:b2+1]==b): ok=True
        elif not b and len(a)==1 and (a in THIN or (a1>0 and f[a1-1]==a) or f[a2:a2+1]==a): ok=True
        (ocr if ok else real).append((a,b,f[max(0,a1-6):a2+6]))
    return real,ocr
