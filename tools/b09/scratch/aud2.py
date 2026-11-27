import json,glob,re,sys,collections,unicodedata
exec(open('/tmp/audit.py').read().split('stats=')[0])
# words: skip drop-cap fragments (word preceded by single capital + space)
per=collections.Counter(); samp={}
for f in sorted(glob.glob(root+'/data/office1909/20*/*.json')):
    day=f[-15:-5]; d=json.load(open(f))
    for h,rows in d['h'].items():
        for r in rows:
            t=r[0] if isinstance(r,list) else r; t=C.get(t,t)
            if isinstance(t,list): t=t[0]
            t=str(t); t=re.sub(r'<c>(\w)</c>\s*',r'\1',t); t=re.sub(r'\b([A-Z]) (?=[a-zæœáéíóúý])',r'\1',t)
            t=re.sub(r'<n>.*?</n>|<h>.*?</h>',' ',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
            ws=[w for w in re.findall(r"[A-Za-zÀ-ÿǽǼæœÆŒ]+",t) if len(w)>2]
            b=[w for w in ws if norm(w) not in known]
            if ws and len(b)/len(ws)>0.04 and len(b)>=3:
                k=(day,h); per[k]+=len(b); samp[k]=(len(b),len(ws),' '.join(b[:8]))
print('rows-with >4% unknown words: days',len(set(k[0] for k in per)),'hours',len(per))
mon=collections.Counter(k[0][:7] for k in per); print(sorted(mon.items()))
for k,v in sorted(samp.items(),key=lambda x:-x[1][0])[:25]: print(k,v)
