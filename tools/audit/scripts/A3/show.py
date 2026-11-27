# print site texts + proposed Missal-based text for key(s)
import sys,warnings; warnings.filterwarnings('ignore')
import batch
from batch import analyse, build, garble, O, R, M
for key in sys.argv[1:]:
    m=M[key]; print('=====',key,m.get('title'),'|',m.get('page'),'| parts',{p:[ (e.get('id') if isinstance(e,dict) else e) for e in v] for p,v in m.get('parts',{}).items()})
    print('refs', [ (x.get('ref'),x.get('kind') or x.get('t')) for x in (R.get(key) or [])])
    for d in analyse(key):
        if d.get('notfound'): print(d['fid'],'NOTFOUND'); continue
        print('--',d['fid'],'%.3f'%d['score'],'IN' if d['inr'] else 'OUT',d['at'])
        print('SITE:',d['old'])
        nw=build(d)
        if nw!=d['old']:
            import difflib
            a=d['old'].split(); b=nw.split()
            print('DIFF:',' '.join(x for x in difflib.ndiff(a,b) if x[0] in '+-'))
