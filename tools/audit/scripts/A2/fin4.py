# Safe merge (coordinator rule 27 Nov): never edit an applied entry; a later change is a NEW entry whose "old" is the live value.
# A pending (unapplied) entry of this session on the same path may be replaced.
import json,sys,os
sys.path.insert(0,'/tmp/A2'); sys.path.insert(0,'/home/claude/dominican-liturgy/tools/audit')
from lib import load
OUT='/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'
import re
def canon(v):
    if isinstance(v,str):
        v=v.replace('Fílium tuum: qui tecum','Fílium tuum; qui tecum').replace('Fílium tuum: Qui tecum','Fílium tuum; qui tecum')
        v=re.sub(r'Spíritus Sancti,? Deus[,:]? per ómnia','Spíritus Sancti Deus: per ómnia',v)
        v=re.sub(r'cum Deo Patre,? in unitáte','cum Deo Patre; in unitáte',v)
        return v.replace('Christum, Fílium tuum;','Christum Fílium tuum;')
    if isinstance(v,list): return [canon(x) for x in v]
    if isinstance(v,dict): return {k:canon(x) for k,x in v.items()}
    return v
d={}; exec(open('/tmp/A2/ver3.py').read(),d); VER,EXTRA=d['VER'],d['EXTRA']
raw={f['k']:f for f in json.load(open('/tmp/A2/fixes_raw.json'))}
cur=json.load(open(OUT)); cache={}
def live(fn,path):
    if fn not in cache: cache[fn]=load(fn)
    x=cache[fn]
    for p in path: x=x[p]
    return x
J=re.compile(r'[¿¤«»@]|\.,|,\.|\s[,.;:!?]|Arnen|  ')
added=0; repl=0
def put(fn,path,new,src,why,op=None):
    global added,repl
    s=json.dumps(new,ensure_ascii=False)
    m=J.search(s)
    if m: raise SystemExit('JUNK %r in %s %s'%(m.group(0),path,s[max(0,m.start()-40):m.end()+30]))
    try: lv=live(fn,path); have=True
    except (KeyError,IndexError,TypeError): lv=None; have=False
    if have and canon(lv)==canon(new): return
    if not have and op!='add': raise SystemExit('MISSING path %s'%path)
    same=[i for i,c in enumerate(cur) if c['file']==fn and c['path']==path]
    old=lv if have else None
    if same:
        c=cur[same[-1]]
        if canon(c['new'])==canon(new): return
        if have and canon(lv)!=canon(c['new']): old=c['new']    # chain on a pending link
    e={'file':fn,'path':path,'old':old,'new':new,'src':src,'why':why}
    if not have: e['op']='add'
    cur.append(e); added+=1
for k,(src,why) in VER.items():
    f=raw.get(k)
    if not f: continue
    put(f['file'],f['path'],f['new'],src,why)
for x in EXTRA:
    fn,path=x['file'],x['path']
    if x.get('op')=='add':
        put(fn,path,x['new'],x['src'],x['why'],op='add'); continue
    lv=live(fn,path)
    if 'subs' in x:
        new=lv; ok=True
        for a,b in x['subs']:
            if b in new: pass            # already done (b may contain a)
            elif a in new: new=new.replace(a,b)
            else: print('subs not found (skipped)',path,a[:50]); ok=False
        if not ok: continue
    else: new=x['new']
    put(fn,path,new,x['src'],x['why'])
json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
print('added',added,'replaced',repl,'total',len(cur))
