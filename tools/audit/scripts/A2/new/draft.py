import sys,json,re,unicodedata
ACC=json.load(open('/home/claude/dominican-liturgy/tools/orat39/accdict.json'))
def base(c): return ''.join(x for x in unicodedata.normalize('NFD',c) if unicodedata.category(x)!='Mn')
def accent(w):
    lw=w.lower(); key=lw.replace('æ','ae').replace('œ','oe').replace('j','i')
    r=ACC.get(key)
    if r is None: return w+'¤'
    # restore j and capitals by alignment
    out=[]; k=0
    for c in r:
        bc=base(c).lower()
        n=2 if bc in ('æ','œ') else 1
        orig=lw.replace('æ','ae').replace('œ','oe')[k:k+n]
        if orig=='j': c='j'
        out.append(c); k+=n
    r=''.join(out)
    if w[0].isupper(): r=r[0].upper()+r[1:]
    if w.isupper() and len(w)>1: r=r.upper()
    return r
def text(fn,a,b):
    L=open(fn,encoding='utf8').read().split('\n')
    txt=''
    for l in L[a-1:b]:
        l=l.rstrip()
        if not l.strip(): continue
        if txt.endswith('­') or re.search(r'[a-z]-$',txt):
            txt=txt[:-1]+l.lstrip()
        else:
            txt+=(' ' if txt else '')+l.strip()
    out=re.sub(r"[A-Za-zæœÆŒ]+",lambda m:accent(m.group(0)),txt)
    return re.sub(r'\s+',' ',out)
if __name__=='__main__':
    print(text(sys.argv[1],int(sys.argv[2]),int(sys.argv[3])))
