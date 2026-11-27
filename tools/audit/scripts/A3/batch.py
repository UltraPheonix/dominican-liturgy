import json,sys,re,os
from load import *
import eng, crop
from eng import stream, where
O=load('data/orations.js'); MEM=load('data/memoriae.js'); R=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']
ACC=json.load(open(ROOT+'/tools/orat39/accdict.json'))
HINT=json.load(open('/tmp/A3/hints.json')) if os.path.exists('/tmp/A3/hints.json') else {}
def fields(key):
    """yield (fid, path, text, kind)"""
    o=O.get(key,{})
    for p in ('or','se','pc'):
        if p in o: yield ('%s.%s'%(key,p), [key,p,0], o[p][0], 'or')
    m=M[key]; md='%02d%02d'%(m['month']+1,m['day']) if 'month' in m else None
    for mk,mv in MEM.items():
        if md and mv.get('md')==md:
            for p in ('or','se','pc'):
                if p in mv: yield ('%s.M[%s].%s'%(key,mk,p), ['MEM',mk,p,0], mv[p][0], 'or')
    for n,x in enumerate(R.get(key) or []):
        yield ('%s.r%d'%(key,n), [key,n,'la'], x.get('la',''), 'rd')
def analyse(key):
    m=M[key]; h=HINT.get(key,{})
    rng=eng.mass_ranges(m['month'],m['day'],h.get('pages',[]))
    out=[]
    for fid,path,text,kind in fields(key):
        if fid in h.get('skip',[]): continue
        if kind=='or':
            body,concl=eng.split_concl(text); b0=body.rstrip(); b1=re.sub(r'[\s.:;,]+$','',b0)
            S,mr=eng.best_match(b1, rng)
        else:
            b1=text; concl=''; b0=text
            S,mr=eng.best_match(text, rng, extra=80)
        if fid in h.get('at',{}):   # forced Missal start line
            k=eng.sidx(h['at'][fid]); from cmp import align
            r=align(S,k,80 if kind=='rd' else 60); mr=(r,True)
        if not mr: out.append(dict(fid=fid,notfound=True)); continue
        r,inr=mr
        new,ch=eng.propose(b1,S,r,ACC)
        d=dict(fid=fid,path=path,kind=kind,old=text,b1=b1,b0=b0,concl=concl,S=S,r=r,inr=inr,ch=ch,score=r[0],at=where(r[3]))
        if kind=='or':
            end=r[1]; nxt=stream[end:end+6]
            fp=nxt[0][1] if nxt and not nxt[0][0][0].isalpha() else ''
            d['fp']=fp; d['sitefp']=b0[len(b1):].strip()
            d['mnext']=' '.join(t[1] for t in nxt)
        out.append(d)
    return out
def build(d, skip=(), over=None, fp=None):
    new,_=eng.propose(d['b1'],d['S'],d['r'],ACC,skip,over)
    if d['kind']=='or':
        f=d['fp'] if fp is None else fp
        return new+f+(' '+d['concl'] if d['concl'] else '')
    return new
import difflib as _dl
def garble(c):
    tag,sa,mb,k=c
    if tag=='insert' and re.fullmatch(r'[A-Z]|[a-z]',mb.strip()): return True
    if tag!='replace': return False
    sw=sa.split(); mw=mb.split()
    if len(sw)!=1 or not sw[0][0].isalpha(): return False
    f=eng.fold(sw[0]); g=eng.fold(''.join(mw))
    if not g.replace(' ','').isalpha(): return True
    if g in ACC and g!=f and (ACC[g]!=g or len(g)>5): return False
    return _dl.SequenceMatcher(None,f,g).ratio()>=0.5
def crops(items, out):
    crop.montage(items, out, padx=(70,120), pady=(10,10))
def ctx_words(k, nb=3, na=2):
    ws=[]; j=k-1
    while j>=0 and len(ws)<nb:
        if stream[j][0][0].isalpha(): ws.insert(0,stream[j][1])
        j-=1
    j=k
    while j<len(stream) and len([w for w in ws])<nb+na:
        if stream[j][0][0].isalpha(): ws.append(stream[j][1])
        j+=1
    return ws
SHOWP=False
if __name__=='__main__':
    keys=[a for a in sys.argv[1:] if not a.startswith('-')]; SHOWP='-p' in sys.argv
    allc=[]; rep=[]
    for key in keys:
        for d in analyse(key):
            if d.get('notfound'): rep.append('%s NOTFOUND'%d['fid']); continue
            rep.append('%s %.3f %s %s%s'%(d['fid'],d['score'],'IN' if d['inr'] else 'OUT',d['at'], (' | site-final[%s] missal-final[%s] next: %s'%(d['sitefp'],d['fp'],d['mnext'])) if d['kind']=='or' else ''))
            for i,c in enumerate(d['ch']):
                cid='%s#%d'%(d['fid'],i)
                g=garble(c)
                rep.append('   %s %s%s [%s] -> [%s] @%s'%(cid,'~GARBLE~ ' if g else '',c[0],c[1],c[2],where(c[3])))
                if not g and (('-p' not in sys.argv[0:1]) and (c[1].strip() not in ',:;.' or c[2].strip() not in ',:;.' ) or SHOWP): allc.append((cid, stream[c[3]][3], ctx_words(c[3])))
            if d['kind']=='or' and d['sitefp']!=d['fp']:
                cid='%s#F'%d['fid']; k=d['r'][1]
                rep.append('   %s final [%s] -> [%s]'%(cid,d['sitefp'],d['fp']))
                allc.append((cid, stream[k][3], ctx_words(k,3,1)))
    print('\n'.join(rep))
    tag=keys[0]
    for n in range(0,len(allc),14):
        fn='/tmp/A3/m_%s_%d.png'%(tag,n//14)
        crops([(a+' | '+' '.join(w),b,w) for a,b,w in allc[n:n+14]], fn); print('IMG',fn)
