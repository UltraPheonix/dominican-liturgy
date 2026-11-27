import json,glob,os,time,sys
seen=set(json.load(open('/tmp/b09/seen.json'))) if os.path.exists('/tmp/b09/seen.json') else set()
t0=time.time(); new=[]
while time.time()-t0 < float(sys.argv[1]):
    for f in sorted(glob.glob('/home/claude/dominican-liturgy/tools/b09/fix/*.json')):
        try: d=json.load(open(f))
        except Exception: continue
        for k,v in d.items():
            if k.startswith('_') or k in seen: continue
            seen.add(k); new.append((os.path.basename(f),k,sorted(x for x in v if x not in ('pages',)), v.get('not_ok'), (v.get('note') or '')[:160]))
    if new: break
    time.sleep(20)
json.dump(sorted(seen),open('/tmp/b09/seen.json','w'))
for n in new: print(n)
print('total done',len(seen))
