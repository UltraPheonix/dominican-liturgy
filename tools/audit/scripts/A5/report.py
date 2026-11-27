import sys,json; sys.path.insert(0,'/tmp/A5')
from cmp import *
keys=sys.argv[1:] or A5
res=run(keys)
json.dump(res,open('/tmp/A5/res.json','w'),ensure_ascii=False,indent=0)
with open('/tmp/A5/res.txt','w') as f:
    for k,o in res.items():
        f.write(f"=== {k} | {M[k]['title'] if k in M else ''} | {O.get(k,{}).get('src','')[:70]}\n")
        for p,r in o['or'].items():
            if not r['found']: f.write(f"  {p}: NOT FOUND\n"); continue
            cflag='' if r['conc_site']==r['conc_m'] else f" CONC site={r['conc_site']} m={r['conc_m']}"
            f.write(f"  {p}: pdf{r['pdf']} L{r['line']} diffs{len(r['diffs'])}{cflag}\n")
            for d in r['diffs']: f.write(f"     {d[0]} [{d[1]}] -> [{d[2]}]  ctx: {d[3]}\n")
        for r in o['rd']:
            if not r['found']: f.write(f"  RD {r['ref']}: NOT FOUND\n"); continue
            f.write(f"  RD {r['ref']}: pdf{r['pdf']} L{r['line']} diffs{len(r['diffs'])} alts{r['alts']} after: {r['after'][:60]}\n")
            for d in r['diffs']: f.write(f"     {d[0]} [{d[1][:200]}] -> [{d[2][:200]}]  ctx: {d[3]}\n")
