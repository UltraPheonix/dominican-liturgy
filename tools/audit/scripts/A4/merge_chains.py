# Run AFTER apply_fixes.py has applied A4.json: collapses two entries on the same path (old->mid, mid->new) into one
# (old->new), so that the first no longer reports CONFLICT once the second is applied.
import json
fn='/home/claude/dominican-liturgy/tools/audit/fixes/A4.json';d=json.load(open(fn));seen={};out=[]
for e in d:
    k=(e['file'],json.dumps(e['path']))
    if k in seen and seen[k]['new']==e['old']:
        f=seen[k]; f['new']=e['new']; f['why']+='; then (session 3) '+e['why']
        if f['src']!=e['src']: f['src']+='; '+e['src']
    else: seen[k]=e; out.append(e)
json.dump(out,open(fn,'w'),ensure_ascii=False,indent=1); print(len(d),'->',len(out))
