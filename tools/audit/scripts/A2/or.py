import sys,re;sys.path.insert(0,'/tmp/A2')
from lib import load
O=load('data/orations.js')
for k in sys.argv[1:]:
    for f in ['or','se','pc']:
        t=O[k][f][0]; m=re.search(r'(Per D|Per e|Qui )',t)
        print(k,f,'|',t[:m.start()+12] if m else t)
