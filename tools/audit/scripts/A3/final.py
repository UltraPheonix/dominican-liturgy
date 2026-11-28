# final(fn,path): current data value with all pending A3 fixes (chained) applied
import json,sys
sys.path.insert(0,'/tmp/A3')
from manual import cur
FX=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A3.json',encoding='utf8'))
def final(fn,path):
    v=cur(fn,path)
    for e in FX:
        if e['file']==fn and e['path']==path and e.get('old')==v: v=e['new']
    return v
