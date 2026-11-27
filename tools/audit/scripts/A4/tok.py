import re, unicodedata
from pages import L, blocks
def fold(w):
    w=w.replace('æ','ae').replace('Æ','Ae').replace('œ','oe').replace('Œ','Oe').replace('ǽ','ae').replace('Ǽ','Ae')
    w=unicodedata.normalize('NFD',w); w=''.join(c for c in w if unicodedata.category(c)!='Mn')
    w=w.lower().replace('j','i')
    return w
TOKRE=re.compile(r"[A-Za-zÀ-ÿĀ-žǼǽæœÆŒ]+|[,;:.?!]")
def toks(s):
    return [(m.group(0), m.start()) for m in TOKRE.finditer(s)]
# Missal stream: join lines with soft hyphen handling; keep line index per token
def build():
    out=[]  # (folded, raw, lineno)
    carry=None
    for i,l in enumerate(L):
        if l.startswith('@@PAGE'): continue
        s=l.rstrip()
        parts=toks(s)
        for j,(t,pos) in enumerate(parts):
            if carry is not None and j==0 and t not in ',;:.?!':
                f,r,ln=carry; out[-1]=(fold(r+t),r+t,ln); carry=None; continue
            carry=None
            out.append((fold(t),t,i))
        if s.endswith('\xad') or s.endswith('-') :
            if out and out[-1][0] not in ',;:.?!': carry=out[-1]
    return out
MS=build()
import bisect
BL=[b[1] for b in blocks]
def pageof(line):
    k=bisect.bisect_right(BL,line)-1
    b=blocks[k]; return b[2], b[0]+1   # printed page (left), pdf page
