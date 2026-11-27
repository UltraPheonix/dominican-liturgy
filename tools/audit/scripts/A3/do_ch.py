import json,sys,re,os
from load import *
import eng
from eng import stream, where
D=load('data/masses.js'); M=D['masses']; C=D['chants']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
def gtext(cid):
    fn=ROOT+'/gabc/%s.gabc'%cid
    if not os.path.exists(fn): return None
    s=open(fn,encoding='utf8').read()
    if '%%' in s: s=s.split('%%',1)[1]
    s=re.sub(r'\([^)]*\)','',s); s=re.sub(r'<[^>]*>','',s); s=re.sub(r'\[[^\]]*\]','',s); s=re.sub(r'\{|\}','',s)
    s=s.replace('*','').replace('†','').replace('V/.','').replace('R/.','')
    s=re.sub(r'\s+',' ',s).strip()
    return s
def chk(key, extra_pages=()):
    m=M[key]; rng=eng.mass_ranges(m['month'],m['day'],extra_pages)
    out=[]
    def one(lab,ent):
        cid=ent.get('id') if isinstance(ent,dict) else ent
        t=gtext(cid); inc=(C.get(str(cid)) or {}).get('i')
        if not t: out.append('   %s %s NO GABC (inc %s)'%(lab,cid,inc)); return
        w=t.split(); t2=' '.join(w[:14])
        S,mr=eng.best_match(t2,rng,extra=20)
        if not mr: out.append('   %s %s NOTFOUND: %s'%(lab,cid,t2)); return
        r,inr=mr
        ctx=' '.join(x[1] for x in stream[max(0,r[3]-4):r[3]])
        out.append('   %s %-8s %.2f %s %s | %s | before: %s'%(lab,cid,r[0],'IN ' if inr else 'OUT',where(r[3]),t2[:60],ctx))
    for p,v in m.get('parts',{}).items():
        for e in v: one(p,e)
    for sn,sv in (m.get('season') or {}).items():
        if isinstance(sv,dict):
            for p,v in sv.items():
                if isinstance(v,list):
                    for e in v: one(sn+':'+p,e)
        else: out.append('   season %s %s'%(sn,str(sv)[:100]))
    return out
if __name__=='__main__':
    for key in (sys.argv[1:] or G):
        m=M[key]; print('=====',key,m.get('title'),'| req',m.get('req'),'| page',m.get('page'),m.get('conf'))
        print('\n'.join(chk(key)))
