import sys;sys.path.insert(0,'/tmp/A2')
from lib import load
R=load('data/readings33.js')
for k in sys.argv[1:]:
    for r in R.get(k,[]):
        print(k,r['ref'],'\n LA:',r['la'][:110],'…',r['la'][-70:],'\n EN:',r['en'][:110],'…',r['en'][-70:])
