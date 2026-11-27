import json,re,sys
sys.argv=[sys.argv[0]]
exec(open('/tmp/A1/cmp.py').read().split('S=json.load')[0])
from importlib.machinery import SourceFileLoader
rv=SourceFileLoader('rv','/tmp/A1/review.py').load_module()
O=load('data/orations.js'); R=load('data/readings33.js'); MS=load('data/masses.js')
DEC=json.load(open('/tmp/A1/dec.json'))
CONCL=re.compile(r'\s((?:Per (?:eúndem |eúmdem |eumdem |eundem )?(?:Dóminum|Dominum|Christum)|Per (?:eúndem|eúmdem|eumdem|eundem)(?=\.)|Qui (?:tecum|vivis|cum Patre|vivit|venturus|cum Deo))\b.*)$')
fixes=[]; log=[]
LOC=json.load(open('/tmp/A1/loc_all.json')); SS=json.load(open('/tmp/A1/stream.json'))
def ppage(si):
    w=SS[si]; i=w[0]; return 2*(i-33)+(1 if w[1]>427 else 0), i+1
def src(k,lab):
    l=LOC.get(k,{}).get(lab.replace('en.','').replace('ref.',''))
    if not l: return 'M39'
    a,pa=ppage(l[0]); b,pb=ppage(l[1])
    return 'M39 p. %d (pdf %d)'%(a,pa) if a==b else 'M39 pp. %d-%d (pdf %d%s)'%(a,b,pa,'' if pa==pb else '-%d'%pb)
def field(k,lab):
    if lab.startswith('or.'):
        f=lab[3:5]; return ('data/orations.js',[k,f,0],O[k][f][0])
    if lab.startswith('rd.'):
        n=int(lab[3:].split()[0]); return ('data/readings33.js',[k,n,'la'],R[k][n]['la'])
    if lab.startswith('en.or.'):
        f=lab[6:8]; return ('data/orations.js',[k,f,1],O[k][f][1])
    if lab.startswith('en.rd.'):
        n=int(lab[6:].split()[0]); return ('data/readings33.js',[k,n,'en'],R[k][n]['en'])
    if lab.startswith('ref.rd.'):
        n=int(lab[7:].split()[0]); return ('data/readings33.js',[k,n,'ref'],R[k][n]['ref'])
    if lab=='title': return ('data/masses.js',['masses',k,'title'],MS['masses'][k]['title'])
    raise Exception(lab)
for k,dec in DEC.items():
    its=rv.items(k) if k in rv.D else []
    rej=set(dec.get('rejP',[]))
    news={}  # (file,path tuple) -> [file,path,old,new,count]
    def get(lab):
        fn,path,val=field(k,lab); key=(fn,tuple(path))
        if key not in news: news[key]=[fn,path,val,val,{},lab]
        return news[key]
    # punctuation changes grouped by lab
    bylab={}
    for n,it in enumerate(its):
        if it['kind']!='P' or n in rej: continue
        bylab.setdefault(it['lab'].split()[0] if it['lab'].startswith('rd') else it['lab'],[]).append(it)
    for lab,lst in bylab.items():
        e=get(lab); s=e[3]
        st=toks_site(s)
        for it in sorted(lst,key=lambda x:-x['a']):
            t=st[it['a']]
            assert t[1]==it['site'], (k,lab,t,it)
            s=(s[:t[4]]+it['missal']+s[t[6]:]) if t[1] else (s[:t[4]]+it['missal']+s[t[4]:])
        e[3]=s; e[4]['punct']=e[4].get('punct',0)+len(lst)
    for ed in dec.get('edits',[]):
        lab,old,new=ed[:3]; why=ed[3] if len(ed)>3 else 'words'
        e=get(lab); s=e[3]
        c=s.count(old)
        if c!=1: print('EDIT NOT UNIQUE/NOT FOUND',k,lab,c,old[:60]); continue
        e[3]=s.replace(old,new); e[4][why]=e[4].get(why,0)+1
    for (fn,_),(fn,path,old,new,cnt,lab) in news.items():
        if old==new: continue
        fixes.append({'file':fn,'path':path,'old':old,'new':new,'src':dec.get('src',{}).get(lab) or src(k,lab),'why':', '.join('%s %d'%(a,b) for a,b in cnt.items())+' as printed'})
json.dump(fixes,open('/home/claude/dominican-liturgy/tools/audit/fixes/A1.json','w'),ensure_ascii=False,indent=1)
print(len(fixes),'fixes')
