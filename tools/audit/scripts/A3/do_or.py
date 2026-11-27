import json,sys,re
from load import *
import eng
from eng import stream, where
O=load('data/orations.js'); D=load('data/masses.js'); M=D['masses']
ACC=json.load(open(ROOT+'/tools/orat39/accdict.json'))
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
CT=[('Per eumdem','Per eúmdem'),('Per eundem','Per eúndem'),('Per Dominum','Per Dóminum'),('Qui vivis','Qui vivis'),('Qui tecum','Qui tecum'),('qui tecum','Qui tecum'),('Per Christum','Per Christum'),('Qui cum Patre','Qui cum Patre'),('Qui vivit','Qui vivit')]
def ctype(s):
    f=eng.fold(s)
    for a,b in CT:
        if f.startswith(eng.fold(a)): return eng.fold(a).replace('eundem','eumdem')
    return '?'+f[:20]
def run(key, extra_pages=(), out=None):
    m=M[key]; o=O[key]
    rng=eng.mass_ranges(m['month'],m['day'],extra_pages)
    res=[]
    for p in ('or','se','pc'):
        la=o[p][0]; body,concl=eng.split_concl(la)
        b0=body.rstrip(); b1=re.sub(r'[\s.:;,]+$','',b0)
        S,mr=eng.best_match(b1, rng)
        if not mr: res.append((p,'NOTFOUND',la)); continue
        r,inr=mr
        new,ch=eng.propose(b1,S,r,ACC)
        end=r[1]; nxt=[t for t in stream[end:end+6]]
        fp=nxt[0][1] if nxt and not nxt[0][0][0].isalpha() else ''
        rest=' '.join(t[1] for t in nxt[1:] if True) if fp else ' '.join(t[1] for t in nxt)
        mct=ctype(rest); sct=ctype(concl)
        sitefp=b0[len(b1):].strip()
        newla=new+fp+' '+concl if concl else new+fp
        if sitefp!=fp: ch.append(('final',sitefp,fp,end))
        res.append(dict(p=p,score=round(r[0],3),inr=inr,at=where(r[3]),k=r[3],old=la,new=newla,ch=ch,mct=mct,sct=sct,body=b1))
    return res
if __name__=='__main__':
    for key in (sys.argv[1:] or G):
        print('=====',key,M[key].get('title'),'|',O[key].get('src'))
        for x in run(key):
            if isinstance(x,tuple): print('  ',x); continue
            flag='' if x['mct']==x['sct'] else '  CONCL MISMATCH site %s missal %s'%(x['sct'],x['mct'])
            print('  %s %.3f %s %s%s'%(x['p'],x['score'],'IN ' if x['inr'] else 'OUT',x['at'],flag))
            for c in x['ch']: print('     %s [%s] -> [%s] @%s'%(c[0],c[1],c[2],where(c[3])))
