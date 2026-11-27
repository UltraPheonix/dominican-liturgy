import sys,re
from pages import L, blocks
def page_at(i):
    p=None
    for b in blocks:
        if b[1]<=i: p=b
    return p
def join(a,b):
    s=[]
    for i in range(a,b):
        l=L[i].rstrip()
        if l.startswith('@@PAGE'): s.append(f' [[{l}]] '); continue
        if l.endswith('\xad'): s.append(l[:-1].strip()); 
        else: s.append(l.strip()+' ')
    return re.sub(r' +',' ',''.join(s))
if __name__=='__main__':
    a,b=int(sys.argv[1]),int(sys.argv[2]); print(join(a,b))
