import json,re,sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
keys=sys.argv[1:]
exec(open('/tmp/A1/cmp.py').read())
O=load('data/orations.js')
LOC=json.load(open('/tmp/A1/loc_all.json'))
CONCL=re.compile(r'\s((?:Per (?:eúndem |eúmdem |eumdem |eundem )?(?:Dóminum|Dominum|Christum)|Per (?:eúndem|eúmdem|eumdem|eundem)(?=\.)|Qui (?:tecum|vivis|cum Patre|vivit|venturus|cum Deo))\b.*)$')
pos={}
for p,t in enumerate(MT):
    for si in t[3]: pos.setdefault(si,p)
for k in keys:
    for f in ['or','se','pc','sp']:
        if f not in O.get(k,{}): continue
        la=O[k][f][0]; m=CONCL.search(la)
        l=LOC.get(k,{}).get('or.'+f)
        if not l: print(k,f,'NOLOC'); continue
        p=pos.get(l[1])
        nxt=' '.join((x[2] or '')+x[1] for x in MT[p+1:p+9]) if p is not None else '?'
        print('%s %s | site: %s | missal: %s'%(k,f,(m.group(1)[:45] if m else 'NONE'),nxt))
