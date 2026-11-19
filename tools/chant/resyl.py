"""Re-split gabc syllables in proper liturgical form, keeping the neumes in order.
python3 resyl.py in.gabc > out.gabc"""
import re,sys
V='aeiouyáéíóúýæǽœAEIOUYÁÉÍÓÚÆǼŒ'
KEEP=('ch','ph','th','gn','qu','gu','st','sp','sc')
def nuclei(w):
    out=[];i=0;lw=w.lower()
    while i<len(w):
        if w[i] in V:
            j=i+1
            if lw[i:i+2] in ('ae','au','oe','eu') and lw[i:i+2]!='eu' : j=i+2
            # qu/gu + vowel: u is consonantal
            if lw[i]=='u' and i>0 and lw[i-1] in 'qg' and i+1<len(w) and w[i+1] in V: i+=1; continue
            out.append((i,j)); i=j
        else: i+=1
    return out
def split(w):
    n=nuclei(w)
    if len(n)<=1: return [w]
    cuts=[]
    for (a,b),(c,d) in zip(n,n[1:]):
        cl=w[b:c].lower()
        if len(cl)<=1: cuts.append(b)
        else:
            k=len(cl)-1
            if cl[-2:] in KEEP or (cl[-2] in 'bcdfgpt' and cl[-1] in 'lr') : k=len(cl)-2
            if len(cl)>=3 and cl[-3:] in ('str','spl','scr','spr'): k=len(cl)-3
            cuts.append(b+k)
    parts=[];p=0
    for c in cuts: parts.append(w[p:c]); p=c
    parts.append(w[p:]); return parts
def fix(g):
    head,body=g.split('%%',1) if '%%' in g else ('',g)
    toks=re.findall(r'([^()]*)\(([^)]*)\)',body)
    out=[];word=[]
    def flush():
        if not word: return
        txt=''.join(t for t,_ in word); lead=re.match(r'^\s*',txt).group(); core=txt.strip()
        m=re.match(r'^(.*?)([.,:;?!]*)$',core); w,punct=m.group(1),m.group(2)
        if '<' in core or not w or len(word)==1: out.extend(word); word.clear(); return
        parts=split(w)
        if len(parts)!=len(word): out.extend(word); word.clear(); return
        parts[0]=lead+parts[0]; parts[-1]+=punct
        out.extend(zip(parts,[n for _,n in word])); word.clear()
    for t,n in toks:
        if t.startswith(' ') or t=='' : flush()
        if t.strip()=='' : flush(); out.append((t,n)); continue
        word.append((t,n))
    flush()
    return (head+'%%' if head else '')+''.join('%s(%s)'%x for x in out)
if __name__=='__main__': sys.stdout.write(fix(open(sys.argv[1]).read()))
