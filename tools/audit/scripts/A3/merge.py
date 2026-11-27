# merge /tmp/A3/fx_<KEY>.json (+ extra json files) into tools/audit/fixes/A3.json, replacing same (file,path)
import json,sys
FN='/home/claude/dominican-liturgy/tools/audit/fixes/A3.json'
cur=json.load(open(FN,encoding='utf8'))
n0=len(cur)
for f in sys.argv[1:]:
    for e in json.load(open(f,encoding='utf8')):
        e.pop('_prefix',None)
        k=(e['file'],json.dumps(e['path']))
        cur=[x for x in cur if (x['file'],json.dumps(x['path']))!=k]
        cur.append(e)
json.dump(cur,open(FN,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('entries',n0,'->',len(cur))
