import json,re
ROOT='/home/claude/dominican-liturgy/'
def load(fn):
    s=open(ROOT+fn).read(); i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end(); j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
D=load('data/masses.js'); M=D['masses']; CH=D['chants']
O=load('data/orations.js'); R=load('data/readings33.js')
# Revert, in memory only, A6 fixes the coordinator has already applied, so "old" stays the pre-fix value.
import os as _os
_A6=ROOT+'tools/audit/fixes/A6.json'
_FX=json.load(open(_A6)) if _os.path.exists(_A6) else []
def canon(v):
    if isinstance(v, str):
        v = v.replace('Fílium tuum: qui tecum', 'Fílium tuum; qui tecum').replace('Fílium tuum: Qui tecum', 'Fílium tuum; qui tecum')
        v = re.sub(r'Spíritus Sancti,? Deus[,:]? per ómnia', 'Spíritus Sancti Deus: per ómnia', v)
        v = re.sub(r'Spíritus Sancti Deus per ómnia', 'Spíritus Sancti Deus: per ómnia', v)
        v = re.sub(r'cum Deo Patre,? in unitáte', 'cum Deo Patre; in unitáte', v)
        return v
    if isinstance(v, list): return [canon(x) for x in v]
    if isinstance(v, dict): return {k: canon(x) for k, x in v.items()}
    return v
def revert(fn,obj):
    for e in _FX:
        if e['file']!=fn: continue
        cur=obj
        try:
            for p in e['path'][:-1]: cur=cur[p]
            if canon(cur[e['path'][-1]])==canon(e['new']): cur[e['path'][-1]]=e['old']
        except (KeyError,IndexError,TypeError): pass
    return obj
revert('data/masses.js',D); revert('data/orations.js',O); revert('data/readings33.js',R)
