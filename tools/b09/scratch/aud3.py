import json,glob,re,sys,collections
root=sys.argv[1]; C=json.load(open(root+'/data/office1909/common.json'))
bad=collections.defaultdict(set); lens=[]
for f in sorted(glob.glob(root+'/data/office1909/20*/*.json')):
    day=f[-15:-5]; d=json.load(open(f))
    for h,rows in d['h'].items():
        for r in rows:
            t=C.get(r[0],r[0]); 
            if not isinstance(t,str): continue
            if t.startswith('<h>Oratio') or t.startswith('<h>Commemoratio'):
                body=re.sub(r'<[^>]+>','',t)
                if re.search(r'Ad Matutinum|Lectio [ivx]|Invitatorium|Ad Laudes|Hymnus|Super Psalmos|pag\.',body) or len(body)>900:
                    bad[day].add(h)
print('days with a run-on saint prayer/commemoration:',len(bad))
print(sorted(bad)[:40])
