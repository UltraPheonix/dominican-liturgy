import json,sys,importlib
sys.path.insert(0,'/tmp/A3')
from load import *
import batch, decisions
importlib.reload(decisions)
from decisions import D,SUB,EXTRA
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A3']
keys=sys.argv[1:] or G
SRC=lambda d: 'M39 '+d['at'].replace('pdf ','pdf ').split(', line')[0]
fixes=[]
for key in keys:
    for d in batch.analyse(key):
        if d.get('notfound'): continue
        fid=d['fid']
        skip=set(); over={}
        for i,c in enumerate(d['ch']):
            v=D.get('%s#%d'%(fid,i))
            if v is None and batch.garble(c): v='skip'
            if v=='skip': skip.add(i)
            elif isinstance(v,str): over[i]=v
        fp=None
        if d['kind']=='or':
            v=D.get(fid+'#F')
            if v=='skip': fp=d['sitefp']
            elif isinstance(v,str): fp=v
        new=batch.build(d,skip,over,fp)
        for a,b in SUB.get(fid,[]):
            assert a in new, (fid,a); new=new.replace(a,b)
        if new!=d['old']:
            if d['path'][0]=='MEM': path=d['path'][1:]; fn='data/memoriae.js'
            elif d['kind']=='or': path=[key,fid.split('.')[1],0]; fn='data/orations.js'
            else: path=[key,int(fid.split('.r')[1]),'la']; fn='data/readings33.js'
            p=d['at'].split(', line')[0]
            fixes.append({'file':fn,'path':path,'old':d['old'],'new':new,'src':'M39 '+p.replace('pdf ','pdf. ').replace('pdf. ','pdf ') ,'why':'words and punctuation as printed (checked on the scan)'})
json.dump(fixes,open('/tmp/A3/fx_%s.json'%keys[0],'w'),ensure_ascii=False,indent=1)
print(len(fixes),'fixes')
for f in fixes:
    import difflib
    a=f['old'].split(); b=f['new'].split()
    dd=[x for x in difflib.ndiff(a,b) if x[0] in '+-']
    print(f['path'], ' '.join(dd)[:400])
