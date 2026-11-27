import json,sys,re
from load import *
import eng
from eng import stream, where, before
R=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']
ACC=json.load(open(ROOT+'/tools/orat39/accdict.json'))
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
def run(key, extra_pages=()):
    m=M[key]; rr=R.get(key) or []
    rng=eng.mass_ranges(m['month'],m['day'],extra_pages)
    res=[]
    for n,x in enumerate(rr):
        out={'n':n,'x':x}
        for fld in ('la',):
            t=x.get(fld) or ''
            S,mr=eng.best_match(t,rng,extra=80)
            if not mr: out[fld]=None; continue
            r,inr=mr
            new,ch=eng.propose(t,S,r,ACC)
            out[fld]=dict(score=round(r[0],3),inr=inr,at=where(r[3]),k=r[3],end=r[1],new=new,ch=ch,before=before(r[3],16),after=eng.after(r[1],8))
        res.append(out)
    return res
if __name__=='__main__':
    for key in (sys.argv[1:] or G):
        m=M[key]
        print('=====',key,m.get('title'),'| masses.js readings:',[(x.get('type'),x.get('ref')) for x in m.get('readings',[])])
        for o in run(key):
            x=o['x']; print('  [%d] %s | %s | %s | p33 %s'%(o['n'],x.get('type'),x.get('ref'),x.get('title'),x.get('p33')))
            for fld in ('la',):
                d=o[fld]
                if not d: print('    %s NOTFOUND'%fld); continue
                print('    %s %.3f %s %s | before: %s | after: %s'%(fld,d['score'],'IN ' if d['inr'] else 'OUT',d['at'],d['before'],d['after']))
                for c in d['ch']: print('       %s [%s] -> [%s] @%s'%(c[0],c[1],c[2],where(c[3])))
            en=x.get('en') or ''; la=x.get('la') or ''
            print('    en: %d/%d chars ratio %.2f | en-end: %s'%(len(en),len(la),len(en)/max(1,len(la)),en[-70:]))
