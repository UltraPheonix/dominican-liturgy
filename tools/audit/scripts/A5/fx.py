import sys,json,copy; sys.path.insert(0,'/tmp/A5')
from lib import *
from auto import autofix, split_conc
ORIG={}; CUR={}; WHY={}; SRC={}; REVIEW=[]
def _get(file,path):
    obj={'data/orations.js':O,'data/readings33.js':R,'data/masses.js':D}[file]
    for p in path: obj=obj[p]
    return obj
def _key(file,path): return (file,tuple(path))
def cur(file,path):
    k=_key(file,path)
    if k not in CUR: ORIG[k]=copy.deepcopy(_get(file,path)); CUR[k]=copy.deepcopy(ORIG[k])
    return CUR[k]
def setv(file,path,val,src,why):
    k=_key(file,path); cur(file,path); CUR[k]=val
    WHY.setdefault(k,[]).append(why); SRC[k]=src
def _sub(s,subs,ctx):
    for a,b in subs:
        n=s.count(a)
        if n!=1: raise Exception(f'{ctx}: "{a}" occurs {n} times in: {s[:300]}')
        s=s.replace(a,b)
    return s
def orat(k,p,subs,src,why):
    s=cur('data/orations.js',[k,p,0]); setv('data/orations.js',[k,p,0],_sub(s,subs,f'{k}.{p}'),src,why)
def oraten(k,p,subs,src,why):
    s=cur('data/orations.js',[k,p,1]); setv('data/orations.js',[k,p,1],_sub(s,subs,f'{k}.{p}.en'),src,why)
def orat_set(k,p,la,en,src,why):
    old=cur('data/orations.js',[k,p]); setv('data/orations.js',[k,p],[la,en]+old[2:],src,why)
def orsrc(k,new,why): cur('data/orations.js',[k,'src']); setv('data/orations.js',[k,'src'],new,'',why)
def rd(k,i,field,subs,src,why):
    s=cur('data/readings33.js',[k,i,field]); setv('data/readings33.js',[k,i,field],_sub(s,subs,f'{k}.rd{i}.{field}'),src,why)
def rdset(k,i,field,new,src,why): cur('data/readings33.js',[k,i,field]); setv('data/readings33.js',[k,i,field],new,src,why)
def title(k,new,src,why): cur('data/masses.js',['masses',k,'title']); setv('data/masses.js',['masses',k,'title'],new,src,why)
def pg(n):
    return 'pdf %d'%n
def auto_or(k,near,src,parts=('or','se','pc'),skip=()):
    for p in parts:
        if p not in O.get(k,{}) or p in skip: continue
        s=cur('data/orations.js',[k,p,0])
        b,c=split_conc(s)
        new,ed,man,r=autofix(s,near,body_end=len(b))
        REVIEW.append((k,p,r and r['pdf'],[(e[0],e[2],e[3],e[5]) for e in ed],man,r and r['after']))
        if ed: setv('data/orations.js',[k,p,0],new,src or ('M39 pdf %s'%(r['pdf'])),'punctuation as printed')
def auto_rd(k,near,src=None,idx=None,skip=()):
    for i,it in enumerate(R.get(k,[])):
        if idx is not None and i not in idx: continue
        if i in skip: continue
        s=cur('data/readings33.js',[k,i,'la'])
        new,ed,man,r=autofix(s,near)
        REVIEW.append((k,'rd%d %s'%(i,it['ref']),r and r['pdf'],[(e[0],e[2],e[3],e[5]) for e in ed],man,r and r['after']))
        if ed: setv('data/readings33.js',[k,i,'la'],new,src or ('M39 pdf %s'%(r['pdf'])),'punctuation as printed')
def save():
    out=[]
    for k in ORIG:
        if CUR[k]==ORIG[k]: continue
        f,path=k
        out.append({'file':f,'path':list(path),'old':ORIG[k],'new':CUR[k],'src':SRC.get(k,''),'why':'; '.join(dict.fromkeys(WHY[k]))})
    json.dump(out,open(ROOT+'tools/audit/fixes/A5.json','w'),ensure_ascii=False,indent=1)
    with open('/tmp/A5/review.txt','w') as f:
        for k,p,pdfn,ed,man,after in REVIEW:
            f.write(f'## {k} {p} pdf{pdfn}  after: {after}\n')
            for e in ed: f.write(f'   P {e}\n')
            for m in man: f.write(f'   M {m}\n')
    print(len(out),'fix entries')
