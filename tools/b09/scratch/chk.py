import json,glob,re,sys,unicodedata
sys.path.insert(0,'tools/b09')
C=json.load(open('data/office1909/common.json'))
FX={}
for f in ['tools/b09/propers_fix.json']+sorted(glob.glob('tools/b09/fix/*.json')):
    FX.update({k:v for k,v in json.load(open(f)).items() if not k.startswith('_')})
def nb(s):
    s=unicodedata.normalize('NFD',re.sub(r'<[^>]+>','',s).lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-zæœ]+',' ',s).strip()
days={}
for f in sorted(glob.glob('data/office1909/20*/*.json')):
    d=json.load(open(f)); days[f[-15:-5]]=d
def text_of(d,hs):
    return nb(' '.join(C.get(r[0],r[0]) for h in hs for r in d['h'].get(h,[])))
rep=[]
for title,X in FX.items():
    # find the day whose title matches
    hit=[k for k,d in days.items() if nb(title.split(' Conf')[0])[:18] in nb(d['t'][0])]
    if not hit: rep.append((title,'NO DAY FOUND')); continue
    k=hit[0]; d=days[k]; ks=sorted(days); pk=ks[ks.index(k)-1]; allt=text_of(d,d['h'].keys())+' '+text_of(days[pk],['Vespera']); miss=[]
    def chk(name,s):
        if isinstance(s,str) and len(nb(s))>12 and nb(s)[:60] not in allt: miss.append(name)
    for key,v in X.items():
        if key in ('pages','note','sub','ok','not_ok') or key.startswith(('gospel','homily')): continue
        if key=='lessons':
            for n,t in v.items(): chk('L'+n,t)
        elif key=='resp':
            for n,r in v.items(): chk('R'+n,r[0]); chk('R%sb'%n,r[1])
        elif isinstance(v,str): chk(key,v)
        elif isinstance(v,list):
            for i,x in enumerate(v):
                if isinstance(x,str): chk('%s[%d]'%(key,i),x)
                elif isinstance(x,list):
                    for j,y in enumerate(x):
                        if isinstance(y,str): chk('%s[%d][%d]'%(key,i,j),y)
    prep=sum('in preparation' in C.get(r[0],'') or 'in præparatióne' in C.get(r[0],'') for r in d['h'].get('Matutinum',[]))
    rep.append((k,title[:34],'missing: '+' '.join(miss) if miss else 'all placed','| prep rows in Matins',prep))
for r in sorted(rep,key=str): print(*r)
