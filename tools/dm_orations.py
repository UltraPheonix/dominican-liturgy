"""Find, for each Mass, its Collect/Secret/Postcommunion in the St Dominic Missal (1959) and compare with orations.js."""
import json, re, unicodedata, difflib
def key(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub('[^a-z]','',s.replace('æ','ae').replace('œ','oe').replace('j','i').replace('y','i'))
T=open('/home/claude/dl/txt/dm.txt',encoding='utf8',errors='replace').read()
T=re.sub(r'-\s*\n\s*','',T)
# segments from each Latin Officium to the next
offs=[m.start() for m in re.finditer(r'(?m)^\s*[^\w\n]{0,3}\s*Offici[un]m\.?\s',T)]
segs=[]
for i,a in enumerate(offs):
    b=offs[i+1] if i+1<len(offs) else len(T)
    s=T[a:b]
    intr=key(re.sub(r'^\s*\W*\s*Offici[un]m\.?\s*','',s)[:60])
    def grab(lab):
        m=re.search(r'(?:^|\n)\s*\W{0,3}\s*'+lab+r'\.?\s+(.*?)(?=\n\s*\W{0,3}\s*(?:Oratio|Secreta|Postcommunio|Lectio|Epistola|Evangelium|Offertorium|Communio|Graduale|Responsorium|Alleluia|Tractus|Sequentia|Oremus|Officium|Commemoratio)\b|\Z)',s,re.S)
        return re.sub(r'\s+',' ',m.group(1)).strip() if m else None
    segs.append({'pos':a,'intr':intr,'or':grab('Oratio'),'se':grab('Secreta'),'pc':grab('Post[ce]o[mn]+unio')})
print(len(segs),'Officium segments;', sum(1 for s in segs if s['or']),'with Oratio')
D=json.loads(open('/home/claude/build/site/data/masses.js',encoding='utf8').read().split('var DOMINICAN = ',1)[1].rstrip().rstrip(';'))
O=json.loads(open('/home/claude/build/site/data/orations.js').read()[len('window.ORATIONS = '):-2])
def sim(a,b):
    a,b=key(a)[:160],key(b)[:160]
    return difflib.SequenceMatcher(None,a,b,autojunk=False).ratio() if a and b else 0
out={}
for k,m in D['masses'].items():
    ids=[c['id'] for c in m['parts'].get('in',[]) if c.get('id')]
    if not ids: continue
    inc=key(re.sub(r'\(.*?\)','',D['chants'][str(ids[0])]['i']))[:10]
    cand=[s for s in segs if s['intr'][:10]==inc and s['or']]
    o=O.get(k)
    best=None
    if o:
        for s in cand:
            sc=sim(o['or'][0],s['or'])
            if not best or sc>best[0]: best=(sc,s)
    r={'n':len(cand)}
    if best and best[0]>=0.8:
        r['status']='same'; s=best[1]
        for c in ('se','pc'):
            if c in o and s[c]: r[c]=round(sim(o[c][0],s[c]),2)
    elif len(cand)==1:
        r['status']='dm-only' if not o else 'differs'; r['dm']={c:cand[0][c] for c in ('or','se','pc')}
    else:
        r['status']='unknown' if cand else 'no-dm'
    out[k]=r
import collections
print(collections.Counter(v['status'] for v in out.values()))
print('secret/postcommunion differing among same:', [(k,v) for k,v in out.items() if v['status']=='same' and (v.get('se',1)<0.8 or v.get('pc',1)<0.8)][:20])
json.dump(out,open('/home/claude/build/orat/dm_check.json','w'),ensure_ascii=False,indent=0)
