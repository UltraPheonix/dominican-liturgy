# manual fix helper: mk(file,path,[(a,b),...],src,why) -> entry using current data value
import json
from load import *
_C={}
def cur(fn,path):
    if fn not in _C: _C[fn]=load(fn)
    v=_C[fn]
    for k in path: v=v[k]
    return v
def mk(fn,path,subs,src,why):
    old=cur(fn,path); new=old
    for a,b in subs:
        assert new.count(a)==1,(path,a,new.count(a)); new=new.replace(a,b)
    return {"file":fn,"path":path,"old":old,"new":new,"src":src,"why":why}
def save(key,entries):
    json.dump(entries,open('/tmp/A3/fx_%s.json'%key,'w'),ensure_ascii=False,indent=1)
