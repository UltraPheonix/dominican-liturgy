"""Draft a long text from the M39 OCR, repairing OCR damage against a reference text (DO).
Usage: merge.py first_page first_col start_regex last_page last_col end_regex reffile"""
import json, re, sys, unicodedata, difflib
sys.path.insert(0,'/home/claude/build/m39hw'); import accent
def strip(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
def strip_keep(w):
    w=w.replace('æ','ae').replace('œ','oe').replace('ǽ','áe')
    return ''.join(ch for ch in w if ch.isalpha())
ACC={'a':'á','e':'é','i':'í','o':'ó','u':'ú','y':'ý','æ':'ǽ','œ':'œ́'}
def transfer(core, ow):
    # letters and ligatures from the reference, accents as printed (OCR reads ü for ú)
    ow=ow.replace('ü','ú')
    base=strip(core.replace('ǽ','æ'))
    acc=[]; k=0
    for ch in ow:
        if not ch.isalpha(): continue
        acc.append(ch in 'áéíóúý')
    # map the accented letter positions of the printed word onto the reference word (same skeleton length after ligatures)
    flat=[]
    for ch in base: flat+= ['a','e'] if ch=='æ' else ['o','e'] if ch=='œ' else [ch]
    if len(flat)!=len(acc) or not any(acc) or 'ë' in core or 'ï' in core: return core
    out=''; i=0
    for ch in base:
        n=2 if ch in 'æœ' else 1
        a=any(acc[i:i+n]); i+=n
        out+= (('ǽ' if ch=='æ' else ch) if a and ch in 'æœ' else (ACC[ch.lower()].upper() if ch.isupper() else ACC[ch.lower()]) if a and ch.lower() in ACC else ch) if a else ch
    if out[:1].isalpha() and core[:1].isupper(): out=out[0].upper()+out[1:]
    return out
def norm(w):
    w=strip(w.lower()).replace('æ','ae').replace('œ','oe')
    w=re.sub(r'[^a-z]','',w)
    return w.replace('j','i')
def ocrnorm(w):  # OCR spellings of the ligatures
    w=w.lower()
    w=re.sub(r'(?<=[a-z])(ze|z|a)(?=[,.;:?!]*$)','æ',w) if False else w
    return norm(w)
p0,c0,rx0,p1,c1,rx1,ref=sys.argv[1:8]; p0,c0,p1,c1=int(p0),int(c0),int(p1),int(c1)
lines=[]
for p in range(p0,p1+1):
    L=json.load(open('/home/claude/build/m39hw/p%d.json'%p))
    for c in (0,1):
        if (p,c)<(p0,c0) or (p,c)>(p1,c1): continue
        cl=[l for l in L if l['c']==c][1:]   # drop running head
        lines+= [l['t'] for l in cl]
txt=' \n'.join(lines)
txt=re.sub(r'\s*\|[^\n]*?(?=\n)','',txt) if False else txt
# rule debris at line starts/ends
L2=[]
for t in lines:
    t=re.sub(r'^(?:[|;,.:\'"()\-!]+\s*|[a-zA-Z1]\s*\|+\s*)+','',t.strip()) if re.match(r'^(?:[|;,.:\'"()\-!]+\s|[a-zA-Z1]\s*\|)',t.strip()) else t.strip()
    t=re.sub(r'\s*(?:\|[^\s]*)+\s*$','',t)
    L2.append(t)
s=''
for t in L2:
    if s.endswith('-'): s=s[:-1]+t
    else: s+=(' ' if s else '')+t
i=re.search(rx0,s).start(); j=re.search(rx1,s).end(); s=s[i:j]
s=re.sub(r'(»\S*|\*I\*|\*\.|"\S*|5x|xx|»:«|»F-?|»J|»1«|»3«|»I\*?|I(?= [A-Z]))(?=\s)','✠',s)
ocr=s.split()
R=open(ref).read().split()
A=[norm(accent.fix_word(w)) for w in ocr]; B=[norm(w) for w in R]
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
out=[]; flags=0
for op,a0,a1,b0,b1 in sm.get_opcodes():
    if op=='equal':
        for k in range(a1-a0):
            o=ocr[a0+k]; r=R[b0+k]
            # take the reference word (accents, ligatures), keep the printed punctuation
            core=re.sub(r'[,.;:?!]+$','',r); pun=re.search(r'[,.;:?!]*$',o).group()
            ow=re.sub(r'[,.;:?!]+$','',o)
            if ow[:1].isupper() and core[:1].islower(): core=core[0].upper()+core[1:]
            if ow[:1].islower() and core[:1].isupper() and core not in ('Jesus','Jesu','Jesum'): core=core[0].lower()+core[1:]
            oa=[i for i,ch in enumerate(strip_keep(ow)) if ch in 'áéíóú']; ra=[i for i,ch in enumerate(strip_keep(core)) if ch in 'áéíóúǽ']
            out.append(transfer(core, ow)+pun)
    else:
        seg=' '.join(accent.fix_word(w) for w in ocr[a0:a1])
        if seg: out.append('⟦'+seg+'⟧'+('{'+' '.join(R[b0:b1])+'}' if b1>b0 else '')); flags+=1
res=' '.join(out)
res=re.sub(r' ([:;?!])',r' \1',res)
print(res); print('FLAGS',flags,file=sys.stderr)
