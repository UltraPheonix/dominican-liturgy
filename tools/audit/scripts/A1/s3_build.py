# Build audit entries for one Mass from items_s3.json (P items), case file, and manual edits.
import sys, json, re, os
sys.path.insert(0,'/tmp/A1')
exec(open('/tmp/A1/cmp.py').read().split('S=json.load')[0])   # toks_site, fold, load
from importlib.machinery import SourceFileLoader
LOC=json.load(open('/tmp/A1/loc_s3.json')); SS=None
def ppage(si):
    global SS
    if SS is None: SS=json.load(open('/tmp/A1/stream.json'))
    w=SS[si]; i=w[0]; return 2*(i-33)+(1 if w[1]>427 else 0), i+1
def srcof(k,lab):
    l=LOC.get(k,{}).get(lab)
    if not l: return 'M39'
    a,pa=ppage(l[0]); b,pb=ppage(l[1])
    return 'M39 p. %d (pdf %d)'%(a,pa) if a==b else 'M39 pp. %d-%d (pdf %d%s)'%(a,b,pa,'' if pa==pb else '-%d'%pb)
def field(k,lab):
    if lab.startswith('or.'): f=lab[3:5]; return ('data/orations.js',[k,f,0])
    if lab.startswith('rd.'): n=int(lab[3:].split()[0]); return ('data/readings33.js',[k,n,'la'])
    if lab.startswith('en.rd.'): n=int(lab[6:].split()[0]); return ('data/readings33.js',[k,n,'en'])
    if lab.startswith('en.or.'): f=lab[6:8]; return ('data/orations.js',[k,f,1])
    if lab.startswith('ref.rd.'): n=int(lab[7:].split()[0]); return ('data/readings33.js',[k,n,'ref'])
    raise Exception(lab)
def build(k, acceptP=None, rejP=(), rejC=(), edits=(), src=None, extra_why=None):
    """acceptP: None = all P items not in rejP. edits: (lab, old, new, why)"""
    O_=load('data/orations.js'); R_=load('data/readings33.js')
    D={'data/orations.js':O_,'data/readings33.js':R_}
    rv=SourceFileLoader('rv','/tmp/A1/review.py').load_module()
    its=rv.items(k)
    news={}
    def get(lab):
        fn,path=field(k,lab); key=(fn,tuple(path))
        if key not in news:
            d=D[fn]
            for p in path: d=d[p]
            news[key]=[fn,path,d,d,{},lab]
        return news[key]
    bylab={}
    for n,it in enumerate(its):
        if it['kind']!='P' or n in rejP or (acceptP is not None and n not in acceptP): continue
        lab=it['lab'].split()[0]
        bylab.setdefault(lab,[]).append(it)
    for lab,lst in bylab.items():
        e=get(lab); s=e[3]
        # orations: P items index into the body without conclusion -> tokens of full string are the same prefix
        st=toks_site(s)
        for it in sorted(lst,key=lambda x:-x['a']):
            t=st[it['a']]; assert t[1]==it['site'] and t[2]==it['word'],(k,lab,t,it)
            s=(s[:t[4]]+it['missal']+s[t[6]:]) if t[1] else (s[:t[4]]+it['missal']+s[t[4]:])
        e[3]=s; e[4]['punct']=e[4].get('punct',0)+len(lst)
    cf='/tmp/A1/case_s3.json'
    if os.path.exists(cf):
        CI=json.load(open(cf)).get(k,[])
        bl={}
        for n,it in enumerate(CI):
            if n in rejC: continue
            bl.setdefault(it['lab'].split()[0],[]).append(it)
        for lab,lst in bl.items():
            e=get(lab); s=e[3]; st=toks_site(s)
            for it in sorted(lst,key=lambda x:-x['a']):
                t=st[it['a']]; assert t[2]==it['site'],(k,t,it)
                w=t[2]; w=(w[0].upper() if it['missal'][0].isupper() else w[0].lower())+w[1:]
                s=s[:t[3]]+w+s[t[4]:]
            e[3]=s; e[4]['case']=e[4].get('case',0)+len(lst)
    for ed in edits:
        lab,old,new=ed[:3]; why=ed[3] if len(ed)>3 else 'words'
        e=get(lab); s=e[3]
        c=s.count(old)
        assert c==1,('EDIT NOT UNIQUE/NOT FOUND',k,lab,c,old)
        e[3]=s.replace(old,new); e[4][why]=e[4].get(why,0)+1
    out=[]
    for (fn,_),(fn,path,old,new,cnt,lab) in news.items():
        if old==new: continue
        s_=(src or {}).get(lab) or srcof(k,lab.split()[0] if lab.startswith('rd') else lab)
        why=', '.join('%s %d'%(a,b) if a in('punct','case') else a for a,b in cnt.items())+' as printed'
        if extra_why and lab in extra_why: why+='; '+extra_why[lab]
        out.append({'file':fn,'path':path,'old':old,'new':new,'src':s_,'why':why,'s3':True,'key':k})
    return out
