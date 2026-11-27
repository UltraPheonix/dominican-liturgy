import json,sys,re,difflib
sys.path.insert(0,'/tmp/A2')
from lib import load
d={}; exec(open('/tmp/A2/rows.py').read(),d)
done=[k for k,(p,r) in d['ROWS'].items() if r.startswith('FIXED')]
F={f['k']:f for f in json.load(open('/tmp/A2/fixes_raw.json'))}
P=json.load(open('/tmp/A2/props.json'))
E={(e['file'],json.dumps(e['path'])):e for e in json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'))}
cache={}
def cur(fn,path):
    if fn not in cache: cache[fn]=load(fn)
    x=cache[fn]
    for p in path: x=x[p]
    return x
for key,v in P.items():
    k=key.split('|')[0]
    if k not in done and k not in sys.argv[1:]: continue
    if sys.argv[1:] and k not in sys.argv[1:]: continue
    prop=F[key]['new'] if key in F else v['old']
    e=E.get((v['file'],json.dumps(v['path'])))
    tgt=e['new'] if e else cur(v['file'],v['path'])
    if prop==tgt: continue
    tok=lambda s: re.findall(r"[^\s,;:.?!]+|[,;:.?!]",s)
    a,b=tok(tgt),tok(prop)
    out=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if op=='equal': continue
        out.append('%s [%s]→[%s]'%(' '.join(a[max(0,i1-3):i1]),' '.join(a[i1:i2]),' '.join(b[j1:j2])))
    print('##',key,v['pages'],len(out)); [print('   ',o) for o in out[:40]]
