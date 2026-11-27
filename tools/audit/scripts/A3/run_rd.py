import json,sys,re,os
from load import *
from cmp import *
R=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
keys=sys.argv[1:] or G
for key in keys:
    m=M.get(key,{}); rr=R.get(key)
    print('=====',key,'|',m.get('title'),'| site readings:',[ (x.get('type'),x.get('ref')) for x in m.get('readings',[])])
    if not rr: print('  NO READINGS33'); continue
    for n,x in enumerate(rr):
        t=(x.get('title') or '')+' '+(x.get('la') or '')
        r=compare(t, extra=80)
        if not r or not r[1]: print('  [%d] %s NOT FOUND: %s'%(n,x.get('ref'),t[:80])); continue
        S,best=r
        print('  [%d] %s %s %.3f %s | words %d | before: %s | missal next: %s'%(n,x.get('type'),x.get('ref'),best[0],where(best[3]),len(S),before(best[3],6),after(best[1],8)))
        print('      keys:',sorted(x.keys()), 'en-end:', (x.get('en') or '')[-60:])
        for l in show(S,best): print(l)
