import sys,json,copy; sys.path.insert(0,'/tmp/A6')
from lib import *
FILES={'data/orations.js':O,'data/readings33.js':R,'data/masses.js':D}
def _obj(f):
    if f not in FILES:
        if f=='data/memoriae.js':   # baseline = git HEAD (the working copy already carries A6's applied memoriae fixes)
            import subprocess,re as _r
            t=subprocess.run(['git','-C',ROOT,'show','a80ac66:'+f],capture_output=True,text=True).stdout
            FILES[f]=json.loads(t[_r.search(r'window\.\w+\s*=\s*',t).end():t.rfind('}')+1])
        else: FILES[f]=revert(f,load(f))
    return FILES[f]
ORIG={}; CUR={}; WHY={}; SRC={}; ORDER=[]; CHAIN={}
def _get(file,path):
    obj=_obj(file)
    for p in path: obj=obj[p]
    return obj
def cur(file,path):
    k=(file,tuple(path))
    if k not in CUR: ORIG[k]=copy.deepcopy(_get(file,path)); CUR[k]=copy.deepcopy(ORIG[k]); ORDER.append(k)
    return CUR[k]
def setv(file,path,val,src,why):
    k=(file,tuple(path)); cur(file,path); CUR[k]=val
    WHY.setdefault(k,[]).append(why); SRC[k]=src
def _sub(s,subs,ctx):
    for a,b in subs:
        n=s.count(a)
        if n!=1: raise Exception(f'{ctx}: "{a}" occurs {n} times in: {s[:300]}')
        s=s.replace(a,b)
    return s
def orat(k,p,subs,src,why,i=0,file='data/orations.js'):
    s=cur(file,[k,p,i]); setv(file,[k,p,i],_sub(s,subs,f'{k}.{p}'),src,why)
def orat_set(k,p,la,en,src,why):
    old=cur('data/orations.js',[k,p]); setv('data/orations.js',[k,p],[la,en]+old[2:],src,why)
def orsrc(k,new,why): cur('data/orations.js',[k,'src']); setv('data/orations.js',[k,'src'],new,'',why)
def rd(k,i,field,subs,src,why):
    s=cur('data/readings33.js',[k,i,field]); setv('data/readings33.js',[k,i,field],_sub(s,subs,f'{k}.rd{i}.{field}'),src,why)
def rdset(k,i,field,new,src,why): cur('data/readings33.js',[k,i,field]); setv('data/readings33.js',[k,i,field],new,src,why)
def mem(key,p,subs,src,why,i=0): orat(key,p,subs,src,why,i,file='data/memoriae.js')
def save():
    out=[]
    for k in ORDER:
        if CUR[k]==ORIG[k]: continue
        f,path=k
        if k in CHAIN:   # already applied in an earlier form: chain old -> applied -> corrected
            mid,why2=CHAIN[k]
            out.append({'file':f,'path':list(path),'old':ORIG[k],'new':mid,'src':SRC.get(k,''),'why':'; '.join(dict.fromkeys(WHY[k]))+' (earlier form, already applied)'})
            if mid!=CUR[k]: out.append({'file':f,'path':list(path),'old':mid,'new':CUR[k],'src':SRC.get(k,''),'why':why2})
            continue
        out.append({'file':f,'path':list(path),'old':ORIG[k],'new':CUR[k],'src':SRC.get(k,''),'why':'; '.join(dict.fromkeys(WHY[k]))})
    json.dump(out,open(ROOT+'tools/audit/fixes/A6.json','w'),ensure_ascii=False,indent=1)
    print(len(out),'fix entries')
