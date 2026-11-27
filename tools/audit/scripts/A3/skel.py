import json,sys
from load import *
import region as R
D=load('data/masses.js'); M=D['masses']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
keys=sys.argv[1:] or G
for key in keys:
    m=M[key]; print('#####',key,m.get('title'),'| month',m.get('month'),'day',m.get('day'))
    for a,b in R.region(m['month'],m['day']):
        print('\n'.join(R.skeleton(a,b)))
