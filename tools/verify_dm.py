"""Check each Collect/Secret/Postcommunion (orations.js) against the St Dominic Missal (1959) Latin."""
import json, re, unicodedata
def key(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub('[^a-z]','',s.replace('æ','ae').replace('œ','oe').replace('j','i').replace('y','i'))
T=key(open('/home/claude/dl/txt/dm.txt',encoding='utf8',errors='replace').read())
O=json.loads(open('/home/claude/build/site/data/orations.js').read()[len('window.ORATIONS = '):-2])
res={}; bad=[]
for k,v in O.items():
    for c in ('or','se','pc'):
        if c not in v: continue
        t=key(v[c][0])
        wins=[t[i:i+18] for i in (0,18,36,54,72) if len(t)>=i+18]
        hits=[T.find(w) for w in wins]
        ok=sum(h>=0 for h in hits)
        res[(k,c)]=ok/len(wins) if wins else 0
        if not wins or ok/len(wins)<0.4: bad.append((k,c,v[c][0][:70]))
print('checked',len(res),'not found in the St Dominic Missal:',len(bad))
json.dump([list(b) for b in bad],open('/home/claude/build/orat/not_in_dm.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(b[0][:1] for b in bad))
for b in bad[:40]: print(b)
