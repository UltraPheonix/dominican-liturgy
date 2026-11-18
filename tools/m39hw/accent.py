"""Restore the printed accents and diphthongs (æ, œ) of OCR'd Latin from a corpus of accented Latin."""
import re, json, glob, unicodedata, collections, os, pickle
CACHE='/home/claude/build/m39hw/lexicon.pkl'
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
def skel(w, ocr=False):
    s=strip(w.lower()).replace('æ','e').replace('œ','e').replace('ae','e').replace('oe','e').replace('j','i')
    if ocr: s=s.replace('ze','e').replace('z','e').replace('ü','u')
    return s
def build():
    C=collections.Counter()
    files=glob.glob('/home/claude/build/site/data/office/202[67]/*.json')+glob.glob('/home/claude/src/do/web/www/missa/Latin/*/*.txt')+glob.glob('/home/claude/src/do/web/www/horas/Latin/*/*.txt')
    for f in files:
        try: t=open(f,encoding='utf8',errors='ignore').read()
        except: continue
        for w in re.findall(r"[A-Za-zÀ-ÿæœÆŒǽ]+",t):
            if any(ch in w for ch in 'áéíóúýǽæœÁÉÍÓÚÆŒ') or len(w)>2: C[w.lower()]+=1
    L={}
    for w,n in C.items():
        k=skel(w)
        if k not in L or n>C[L[k]]: L[k]=w
    pickle.dump(L,open(CACHE,'wb')); return L
LEX=pickle.load(open(CACHE,'rb')) if os.path.exists(CACHE) else build()
# words the corpus spells with a real z
REALZ=re.compile(r'(bapti[sz]|zel|zach|lazar|zoro|zab|gaz|zizan|amazon|nazar|ezech|azar|zorob|booz|elizab)',re.I)
def fix_word(w):
    m=re.match(r"^([^A-Za-zÀ-ÿæœÆŒǽ]*)([A-Za-zÀ-ÿæœÆŒǽ]+)([^A-Za-zÀ-ÿæœÆŒǽ]*)$",w)
    if not m: return w
    a,core,b=m.groups()
    damaged = (('z' in core.lower() and not REALZ.search(core)) or 'ü' in core or re.search(r'ae|oe', core.lower()))
    if not damaged: return w            # the OCR kept the printed accents: leave the word as printed
    k=skel(core, ocr=not REALZ.search(core))
    best=LEX.get(k)
    if not best:
        return a+core.replace('ü','ú')+b
    # keep the printed capital and j
    out=list(best)
    if core[:1].isupper(): out[0]=out[0].upper()
    lc=strip(core.lower())
    if 'j' in lc:
        # put back j where the OCR had j (the book prints j)
        o2=''.join(out)
        sk=[c for c in o2]
        idx=[i for i,c in enumerate(lc) if c=='j']
        res=list(o2)
        for i in idx:
            if i<len(res) and res[i].lower()=='i': res[i]='J' if res[i]=='I' else 'j'
        out=res
    return a+''.join(out)+b
def dropcap(w):
    # a paragraph whose first letter (a printed initial) the OCR lost
    m=re.match(r"^([A-Za-zÀ-ÿæœ]+)(.*)$",w)
    if not m or skel(m.group(1)) in LEX: return w
    for X in 'OIDSFAECPQUNMTVGLR':
        if skel(X+m.group(1)) in LEX: return X+m.group(1)+m.group(2)
    return w
def fix(text):
    return ' '.join(fix_word(w) for w in text.split(' '))
if __name__=='__main__':
    import sys; print(len(LEX)); print(fix(sys.argv[1]))
