import json,re,unicodedata
ROOT='/home/claude/dominican-liturgy/'
def load(fn):
    s=open(ROOT+fn).read(); i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end(); j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
D=load('data/masses.js'); M=D['masses']; CH=D['chants']
O=load('data/orations.js'); R=load('data/readings33.js')
A5=json.load(open(ROOT+'tools/audit/groups.json'))['A5']
def chinc(cid):
    c=CH.get(str(cid),{}); return c.get('i','?')
# Revert, in memory only, any A5 fixes the coordinator has already applied, so that "old" values stay pre-fix.
def _revert():
    import os
    fn=ROOT+'tools/audit/fixes/A5.json'
    if not os.path.exists(fn): return
    objs={'data/orations.js':O,'data/readings33.js':R,'data/masses.js':D}
    for e in json.load(open(fn)):
        cur=objs[e['file']]
        try:
            for p in e['path'][:-1]: cur=cur[p]
            if cur[e['path'][-1]]==e['new']: cur[e['path'][-1]]=e['old']
        except (KeyError,IndexError,TypeError): pass
_revert()
