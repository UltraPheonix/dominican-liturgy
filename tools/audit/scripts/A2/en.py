import sys; sys.path.insert(0,'/tmp/A2')
from lib import load
R=load('data/readings33.js')
for k in sys.argv[1:]:
    for n,r in enumerate(R.get(k,[])):
        print(k,n,r['ref']); print('  LA:',r['la'][:110],' … ',r['la'][-90:]); print('  EN:',r['en'][:110],' … ',r['en'][-90:])
