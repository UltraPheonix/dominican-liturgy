import json,re,sys
exec(open('/tmp/A1/cmp.py').read().split('S=json.load')[0])
O=load('data/orations.js');R=load('data/readings33.js');M=load('data/masses.js')['masses']
for k in sys.argv[1:]:
    m=M[k]; print('==',k,'|',m.get('title'),'|',{a:b for a,b in m.items() if a not in('parts','title')})
    for p,v in m['parts'].items(): print('  ',p,[ (c.get('id'),c.get('inc') or c.get('incipit') or '') for c in v])
    for f,v in O.get(k,{}).items():
        if isinstance(v,list): print(' OR',f,'LA:',v[0][:400]); print('       EN:',(v[1] if len(v)>1 else '')[:400])
        else: print(' OR',f,v)
    for n,r in enumerate(R.get(k,[])):
        print(' RD',n,r.get('type'),r.get('ref'),'|',{a:b for a,b in r.items() if a not in('la','en','type','ref')})
        print('    LA:',r['la']); print('    EN:',r.get('en'))
