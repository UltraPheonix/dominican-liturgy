import sys
from load import load
O=load('data/orations.js'); R=load('data/readings33.js')
for key in sys.argv[1:]:
    for p in ('or','se','pc'):
        if p in O.get(key,{}): print(key,p,'EN:',O[key][p][1][:400])
    for n,x in enumerate(R.get(key) or []): print(key,'r%d'%n,x['ref'],'|',x['title_en'],'EN:',x['en'])
