import sys,difflib,re
sys.path.insert(0,'/tmp/A4')
from load import load
RD=load('data/readings33.js'); O=load('data/orations.js')
def tk(s): return re.findall(r"\w+|[^\w\s]",s)
def cmp(a,b,lab=''):
    A,B=tk(a),tk(b); sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
    out=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': out.append(f"{op} [{' '.join(A[max(0,i1-3):i2+2])}] -> [{' '.join(B[max(0,j1-3):j2+2])}]")
    print(lab, 'SAME' if not out else ''); [print('   ',x) for x in out]
if __name__=='__main__':
    k1,k2=sys.argv[1],sys.argv[2]
    what=sys.argv[3] if len(sys.argv)>3 else 'r'
    if what=='r':
        for i,(x,y) in enumerate(zip(RD[k1],RD[k2])):
            cmp(x['la'],y['la'],f'{i} la'); cmp(x['en'],y['en'],f'{i} en')
    else:
        for p in ('or','se','pc'):
            if p in O.get(k1,{}) and p in O.get(k2,{}): cmp(O[k1][p][0],O[k2][p][0],p)
