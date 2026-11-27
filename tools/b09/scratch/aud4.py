import json,glob,re,sys,unicodedata
root=sys.argv[1]; C=json.load(open(root+'/data/office1909/common.json'))
def n(s): s=unicodedata.normalize('NFD',s.lower()); return ''.join(c for c in s if unicodedata.category(c)!='Mn').replace('j','i')
STOP=set('sancti sanctae sancte beati beatae conf virg mart abb ep pont doct eccl et ss vid regis reg pp papae ord praed in de apostoli evang ii iii'.split())
tot=0;miss=[]
for f in sorted(glob.glob(root+'/data/office1909/2026/*.json'))+sorted(glob.glob(root+'/data/office1909/2027/*.json')):
    day=f[-15:-5]; d=json.load(open(f)); seen=set()
    for r in d['h'].get('Laudes',[]):
        t=C.get(r[0],r[0])
        if not isinstance(t,str) or not t.startswith('<h>Oratio de Sancto'): continue
        m=re.search(r'<n>(.*?)</n>',t); title=m.group(1) if m else ''
        body=n(re.sub(r'<[^>]+>','',t.split('</n>',1)[-1]))
        keys=[w[:5] for w in re.findall(r'\w+',n(title)) if len(w)>3 and w not in STOP]
        tot+=1
        if keys and not any(k in body for k in keys) and ' n.' not in body: miss.append((day,title,body[10:90]))
print('saint prayers',tot,'name not in prayer',len(miss))
for x in miss[:200]: print(x)
