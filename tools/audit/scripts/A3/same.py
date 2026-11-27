# same.py DST SRC [n...]: make fixes setting DST readings n to SRC's current (scan-checked) la/en/ref where they differ
import json,sys
from load import *
R=load('data/readings33.js')
dst,src=sys.argv[1],sys.argv[2]; ns=[int(x) for x in sys.argv[3:]] or range(len(R[src]))
pg=json.load(open('/tmp/A3/same_src.json')) if False else None
out=[]
for n in ns:
    for f in ('la','en','ref'):
        a=R[dst][n].get(f); b=R[src][n].get(f)
        if a!=b:
            out.append({"file":"data/readings33.js","path":[dst,n,f],"old":a,"new":b,"src":"","why":""})
            print(n,f,'DIFF'); 
            import difflib
            print('  ',[x for x in difflib.ndiff((a or '').split(),(b or '').split()) if x[0] in '+-'][:30])
json.dump(out,open('/tmp/A3/fx_%s_same.json'%dst,'w'),ensure_ascii=False,indent=1)
