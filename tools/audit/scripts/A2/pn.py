import json,sys
F={f['k']:f for f in json.load(open('/tmp/A2/fixes_raw.json'))}
for k in sys.argv[1:]:
    f=F.get(k)
    if not f: print(k,'NO CHANGE'); continue
    print('##',k,f['pdf']); print(f['new']); print()
