import json,re
S=json.load(open('site_refs.json')); O=json.load(open('readings33b.json'))
def norm(ref):
    m=re.match(r'(.*?)\s*(\d+)\s*:\s*(\d+)',ref or '');
    return (m.group(1).strip()[:6].lower(),int(m.group(2)),int(m.group(3))) if m else None
ag=dis=0; D=[]
for k,v in O.items():
    if k not in S: continue
    for r in v['readings']:
        s=[x for x in S[k]['r'] if (x[0]=='Gospel')==(r['type']=='Gospel')]
        a=norm(r['ref']); 
        if not s: continue
        if any(norm(x[1])==a or (norm(x[1]) and a and norm(x[1])[:2]==a[:2] and abs(norm(x[1])[2]-a[2])<=1) for x in s): ag+=1
        else: dis+=1; D.append((k,r['type'],r['ref'],[x[1] for x in s],r.get('flag')))
print(ag,dis)
json.dump(D,open('dis.json','w'),ensure_ascii=False)
