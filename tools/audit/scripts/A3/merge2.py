# append /tmp/A3/fx_*.json entries to tools/audit/fixes/A3.json (never edits/removes an existing entry; chains on same path)
import json,sys
FN='/home/claude/dominican-liturgy/tools/audit/fixes/A3.json'
cur=json.load(open(FN,encoding='utf8')); n0=len(cur)
seen={json.dumps(x,sort_keys=True,ensure_ascii=False) for x in cur}
for f in sys.argv[1:]:
    for e in json.load(open(f,encoding='utf8')):
        e.pop('_prefix',None)
        s=json.dumps(e,sort_keys=True,ensure_ascii=False)
        if s in seen: continue
        same=[x for x in cur if x['file']==e['file'] and x['path']==e['path'] and x.get('old')==e.get('old')]
        if same: print('WARN same path+old exists, skipping', e['path']); continue
        cur.append(e); seen.add(s)
json.dump(cur,open(FN,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('entries',n0,'->',len(cur))
