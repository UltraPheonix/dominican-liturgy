import json,sys,re
o=json.load(open('new_or.json')); r=json.load(open('report.json'))
R={(x['k'],x['p']):x for x in r}
for k in sys.argv[1:]:
    print('##',k)
    for kind in ('or','se','pc'):
        la=re.sub(r'(Per Dóminum|Per eúndem|Qui vivis|Qui tecum).*$', r'\1…', o[k][kind][0])
        en=re.sub(r'(?i)[;:,.]? *(through (our|the same) Lord Jesus Christ|who lives? and reigns?).*$','',R[(k,kind)]['en'])
        print(kind,la); print('  =',R[(k,kind)]['r'],en[:400])
