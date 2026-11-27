# Merge verified proposals (ver.py: VER, EXTRA) into tools/audit/fixes/A2.json.
# VER: {propkey: (src, why)}; EXTRA: list of dicts {file,path,new,src,why} (old taken from current data).
import json,sys
sys.path.insert(0,'/tmp/A2')
from lib import load
OUT='/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'
d={}; exec(open('/tmp/A2/ver.py').read(),d)
VER,EXTRA=d['VER'],d['EXTRA']
import os as _o
if _o.path.exists('/tmp/A2/ver2.py'):
    d2={}; exec(open('/tmp/A2/ver2.py').read(),d2); VER.update(d2['VER']); EXTRA=EXTRA+d2['EXTRA']
raw={f['k']:f for f in json.load(open('/tmp/A2/fixes_raw.json'))}
cur=json.load(open(OUT))
import os
SEEN='/home/claude/dominican-liturgy/tools/audit/scripts/A2/seen.json'
seen=json.load(open(SEEN)) if os.path.exists(SEEN) else []
have={(e['file'],json.dumps(e['path']),json.dumps(e['new'],ensure_ascii=False)) for e in cur}|{tuple(x) for x in seen}
cache={}
def getval(fn,path):
    if fn not in cache: cache[fn]=load(fn)
    x=cache[fn]
    for p in path: x=x[p]
    return x
add=0
for k,(src,why) in VER.items():
    f=raw.get(k)
    if not f: print('no proposal/change for',k); continue
    if any(c['file']==f['file'] and c['path']==f['path'] for c in cur): continue   # later changes go through EXTRA only
    if '¿' in f['new'] or '.,.' in f['new']: print('GARBAGE in proposal, skipped',k); continue
    e={'file':f['file'],'path':f['path'],'old':f['old'],'new':f['new'],'src':src,'why':why}
    if (e['file'],json.dumps(e['path']),json.dumps(e['new'],ensure_ascii=False)) in have: continue
    cur.append(e); have.add((e['file'],json.dumps(e['path']),json.dumps(e['new'],ensure_ascii=False))); add+=1
def latest(fn,path):
    v=None
    for e in cur:
        if e['file']==fn and e['path']==path: v=e['new']
    return v if v is not None else getval(fn,path)
for x in EXTRA:
    if x.get('op')=='add':
        if any(c['file']==x['file'] and c['path']==x['path'] for c in cur): continue
        cur.append({'file':x['file'],'path':x['path'],'op':'add','old':None,'new':x['new'],'src':x['src'],'why':x['why']}); add+=1; continue
    old=latest(x['file'],x['path'])
    new=x.get('new')
    if 'subs' in x:
        new=old; skip=False
        for a,b in x['subs']:
            if a not in new:
                if b in new: skip=True; break
                raise SystemExit('subs not found %r %r'%(x['path'],a))
            new=new.replace(a,b)
        if skip: continue
    if (x['file'],json.dumps(x['path']),json.dumps(new,ensure_ascii=False)) in have: continue
    if old==new: print('no change',x['path']); continue
    cur.append({'file':x['file'],'path':x['path'],'old':old,'new':new,'src':x['src'],'why':x['why']}); add+=1
    have.add((x['file'],json.dumps(x['path']),json.dumps(new,ensure_ascii=False)))
# collapse chains on the same path into one entry (old of the first, new of the last)
merged=[]; idx={}
for e in cur:
    k=(e['file'],json.dumps(e['path']))
    if k in idx:
        m=merged[idx[k]]
        if True:
            m.setdefault('_chain',[]).append(m['new']); m.setdefault('_chain',[]).append(e['old'])
            m['new']=e['new']
            if e['src'] not in m['src']: m['src']+='; '+e['src']
            if e['why'] not in m['why']: m['why']+='; '+e['why']
    else:
        idx[k]=len(merged); merged.append(dict(e))
# if the coordinator already applied an intermediate step of a chain, start the merged entry from the current value
for m in merged:
    try: v=getval(m['file'],m['path'])
    except Exception: continue
    if v!=m['old'] and v!=m['new'] and v in m.get('_chain',[]): m['old']=v
for m in merged: m.pop('_chain',None)
cur=merged
json.dump(sorted(have),open(SEEN,'w'),ensure_ascii=False)
json.dump(cur,open(OUT,'w'),ensure_ascii=False,indent=1)
print('added',add,'total',len(cur))
