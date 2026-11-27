import sys,re; sys.path.insert(0,'/tmp/A5')
from missal import *
def segs(lo=70391,hi=81600):
    starts=[i for i in range(lo,hi) if L[i].strip().startswith('Officium')]
    out=[]
    for a,b in zip(starts,starts[1:]+[hi]):
        txt=' '.join(L[i].strip() for i in range(a,b) if not L[i].startswith('@@'))
        txt=re.sub(r'­\s*','',txt)
        out.append((a,pdf[a],txt))
    return out
LAB=['Officium','Oratio','Lectio','Sequentia sancti Evangelii','Offertorium','Secreta','Communio','Postcommunio','Tractus','Alleluia, alleluia']
def parts(txt):
    res=[]
    for lb in LAB:
        for m in re.finditer(re.escape(lb),txt):
            res.append((m.start(),lb,txt[m.end():m.end()+70]))
    res.sort()
    return res
if __name__=='__main__':
    for a,p,txt in segs():
        print('#### L%d pdf%d'%(a,p))
        for _,lb,t in parts(txt):
            print('   %-12s %s'%(lb[:12],t))
