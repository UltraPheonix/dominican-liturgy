import json, re, unicodedata, collections
GB=json.load(open('gb_op.json')); OT=json.load(open('office_texts.json'))
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    s=s.replace('æ','ae').replace('œ','oe').replace('j','i').replace('v','u')
    s=re.sub(r'e u o u a e.*$','',s)
    s=re.sub(r'[^a-z ]',' ',s); return s.split()
idx=collections.defaultdict(list)
for cid,e in GB.items():
    w=norm(e['text']); 
    if len(w)>=2: idx[' '.join(w[:4])].append(cid)
def find(t,kind):
    w=norm(t)
    best=None
    for n in (4,3):
        for cid in idx.get(' '.join(w[:n]),[]) if n==4 else []:
            gw=norm(GB[cid]['text'])
            # proportion of office words matched in order
            m=sum(1 for a,b in zip(w,gw) if a==b)/max(1,len(w))
            if GB[cid]['part'] in ({'an':('an',),'rb':('rb','re'),'hy':('hy',)}[kind]) and (not best or m>best[0]): best=(m,cid)
    return best
stat=collections.Counter(); miss=[]
for o in OT:
    b=find(o['t'],o['kind'])
    ok=b and b[0]>0.6
    stat[o['kind'],bool(ok)]+=1; stat[o['kind'],'occ',bool(ok)]+=o['n']
    if not ok and o['kind']=='an': miss.append((o['n'],o['t'][:70],o['where'][0]))
print(stat)
miss.sort(reverse=True); print('\n'.join(map(str,miss[:40])))
