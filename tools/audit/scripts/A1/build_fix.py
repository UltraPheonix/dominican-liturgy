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
import os
OLDF=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A1.json'))
def curval(f):
    d={'data/orations.js':O,'data/readings33.js':R,'data/masses.js':MS}[f['file']]
    try:
        for p in f['path']: d=d[p]
        return d
    except Exception: return None
APPLIED={f['path'][1] if f['file']=='data/masses.js' else f['path'][0] for f in OLDF if curval(f)==f['new']}
for k,dec in DEC.items():
    if k in ('Adv1','Adv3') or k in APPLIED: continue
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
    cf='/tmp/A1/case_%s.json'%k
    if os.path.exists(cf):
        CI=json.load(open(cf)).get(k,[]); rejC=set(dec.get('rejC',[]))
        bl={}
        for n,it in enumerate(CI):
            if n in rejC: continue
            bl.setdefault(it['lab'].split()[0] if it['lab'].startswith('rd') else it['lab'],[]).append(it)
        for lab,lst in bl.items():
            e=get(lab); s=e[3]; st=toks_site(s)
            for it in sorted(lst,key=lambda x:-x['a']):
                t=st[it['a']]; assert t[2]==it['site'],(k,t,it)
                w=t[2]; w=(w[0].upper() if it['missal'][0].isupper() else w[0].lower())+w[1:]
                s=s[:t[3]]+w+s[t[4]:]
            e[3]=s; e[4]['case']=e[4].get('case',0)+len(lst)
    for ed in dec.get('edits',[]):
        lab,old,new=ed[:3]; why=ed[3] if len(ed)>3 else 'words'
        e=get(lab); s=e[3]
        c=s.count(old)
        if c!=1: print('EDIT NOT UNIQUE/NOT FOUND',k,lab,c,old[:60]); continue
        e[3]=s.replace(old,new); e[4][why]=e[4].get(why,0)+1
    for (fn,_),(fn,path,old,new,cnt,lab) in news.items():
        if old==new: continue
        fixes.append({'file':fn,'path':path,'old':old,'new':new,'src':dec.get('src',{}).get(lab) or src(k,lab),'why':', '.join('%s %d'%(a,b) for a,b in cnt.items())+' as printed'})
FN='/home/claude/dominican-liturgy/tools/audit/fixes/A1.json'
old=json.load(open(FN)); newk={(f['file'],tuple(f['path'])) for f in fixes}
extra=json.load(open('/tmp/A1/manual.json')) if __import__('os').path.exists('/tmp/A1/manual.json') else []
exk={(f['file'],tuple(f['path'])) for f in extra}
fixes=[f for f in old if (f['file'],tuple(f['path'])) not in newk|exk]+[f for f in fixes if (f['file'],tuple(f['path'])) not in exk]+extra
for k,dec in DEC.items():
    for lab,o,n,why in dec.get('amend',[]):
        fn,path,cur=field(k,lab)
        e=[f for f in fixes if f['file']==fn and f['path']==path]
        if e:
            e=e[0]; base=e['new']
            if o not in base:
                if n not in base: print('AMEND NOT FOUND',k,lab,o)
                continue
            if cur==base: e['old']=cur
            e['new']=base.replace(o,n,1); e['why']+='; %s (amended)'%why
        else:
            if cur.count(o)!=1: print('AMEND NOT FOUND',k,lab,o); continue
            fixes.append({'file':fn,'path':path,'old':cur,'new':cur.replace(o,n),'src':dec.get('src',{}).get(lab) or src(k,lab),'why':why+' as printed'})
json.dump(fixes,open(FN,'w'),ensure_ascii=False,indent=1)
print(len(fixes),'fixes')
