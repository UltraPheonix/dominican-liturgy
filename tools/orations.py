"""Collect, Secret and Postcommunion of each Mass, from Divinum Officium (Latin with accents, English),
found by the Introit: the DO Mass whose Introit begins as the Mass's Introit does (date file first for saints).
-> site/data/orations.js  {key: {or: [la, en], se: [la, en], pc: [la, en], src}}"""
import json, re, os, glob, unicodedata, sys
DO='/home/claude/src/do/web/www/missa'
SITE='/home/claude/build/site'
D=json.loads(open(SITE+'/data/masses.js',encoding='utf8').read().split('var DOMINICAN = ',1)[1].rstrip().rstrip(';'))
def key(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub('[^a-z]','',s.replace('æ','ae').replace('œ','oe').replace('j','i').replace('y','i'))
cache={}
def sections(lang,path):
    f='%s/%s/%s.txt'%(DO,lang,path)
    if not os.path.exists(f) and path.startswith('Commune/'):
        f='%s/../horas/%s/%s.txt'%(DO,lang,path)
    if f in cache: return cache[f]
    S={}; cur=None
    if os.path.exists(f):
        for l in open(f,encoding='utf8',errors='replace'):
            l=l.rstrip('\n')
            m=re.match(r'^\[([^\]]+)\]\s*(.*)$',l)
            if m: cur=m.group(1)+(' '+m.group(2) if m.group(2) else ''); S[cur]=[]; continue
            if cur: S[cur].append(l)
    cache[f]=S; return S
PR={}
def prayer(lang,name):
    S=sections(lang,'Ordo/Prayers')
    t=[l for l in S.get(name,[]) if l.strip()]
    return ' '.join(re.sub(r'^[rRvV]\.\s*','',l) for l in t[:1])
def get(lang,path,sec,depth=0):
    S=sections(lang,path)
    lines=S.get(sec)
    if lines is None:
        # whole-file inheritance
        for l in S.get('Rule',[])+[x for v in S.values() for x in v][:0]: pass
        return None
    out=[]
    for l in lines:
        l=l.strip()
        if not l or l.startswith('!') or l.startswith('#'): continue
        if l.startswith('@'):
            m=re.match(r'@([^:]*)(?::(.*))?',l)
            if m and depth<5:
                if not m.group(1): continue
                r=get(lang,m.group(1),m.group(2) or sec,depth+1)
                if r: out.append(r)
            continue
        if l.startswith('$'):
            p=prayer(lang,l[1:].strip())
            if p: out.append(p)
            continue
        if l.startswith('&') or l.startswith('('): continue
        out.append(re.sub(r'^v\.\s*','',l))
    return ' '.join(out).strip() or None
def rule_vide(lang,path):
    S=sections(lang,path)
    for l in S.get('Rule',[])+S.get('Rank',[]):
        m=re.search(r'(?:vide|ex)\s+(C[\w-]+)',l)
        if m: return 'Commune/'+m.group(1)
    return None
_get=get
def get(lang,path,sec,depth=0):
    r=_get(lang,path,sec,depth)
    if r is None and depth<4:
        v=rule_vide(lang,path)
        if v: return get(lang,v,sec,depth+1)
    return r
def tempfile(k):
    W={'m':1,'t':2,'w':3,'h':4,'f':5,'s':6}
    fixed={'Adv3w':'Tempora/Adv3-3','Adv3f':'Tempora/Adv3-5','Adv3s':'Tempora/Adv3-6','Nat1':'Tempora/Nat1-0','Nat2':'Tempora/Nat2-0',
      'Dec24':'Sancti/12-24','Dec25_1':'Sancti/12-25m1','Dec25_2':'Sancti/12-25m2','Dec25_3':'Sancti/12-25m3','Jan1':'Sancti/01-01','Jan5a':'Sancti/01-05',
      'Epi':'Sancti/01-06','7a':'Tempora/Quadp1-0','6a':'Tempora/Quadp2-0','5a':'Tempora/Quadp3-0','5aw':'Tempora/Quadp3-3','5ah':'Tempora/Quadp3-4',
      '5af':'Tempora/Quadp3-5','5as':'Tempora/Quadp3-6','Asc':'Tempora/Pasc5-4','AscVig':'Tempora/Pasc5-3','Litaniis':'Tempora/Pasc5-1r',
      'Pasc6':'Tempora/Pasc6-0','Pasc6s':'Tempora/Pasc6-6','Pent0':'Tempora/Pasc7-0','CorpusChristi':'Tempora/Pent01-4','SCJ':'Tempora/Pent02-5',
      'EmbWedSept':'Tempora/093-3','EmbFriSept':'Tempora/093-5','EmbSatSept':'Tempora/093-6','EmbSatSeptS':'Tempora/093-6','Dedicatio':'Commune/C8',
      'ChristusRex':'Sancti/10-DU','C1s':'Commune/C1','S0202':'Sancti/02-02','S0211':'Sancti/02-11','S0701':'Sancti/07-01','S0822':'Sancti/08-22','S0825':'Sancti/08-25','S0914':'Sancti/09-14','S1125':'Sancti/11-25','C7s':'Commune/C2a-1','C11s':'Commune/C2-1','C15s':'Commune/C2p','C18s':'Commune/C2a','C21s':'Commune/C3a-1','C25s':'Commune/C3','C28s':'Commune/C3p','C30s':'Commune/C4-1','C32s':'Commune/C4','C35s':'Commune/C4a','C39s':'Commune/C5-1','C42s':'Commune/C5','C45s':'Commune/C6','C48s':'Commune/C6-1','C51s':'Commune/C7a','C55s':'Commune/C6a','C79s':'Commune/C11','C114s':'Sancti/11-02','C62s':'Tempora/Pent01-4','C75s':'Tempora/Pasc7-0','Pent1':'Tempora/Pent01-0','Quad6f':'Tempora/Quad6-5','Quad6s':'Tempora/Quad6-6','Quad6h':'Tempora/Quad6-4'}
    if k in fixed: return fixed[k]
    m=re.fullmatch(r'(Adv|Epi|Quad|Pasc)(\d)([mtwhfs]?)',k)
    if m: return 'Tempora/%s%s-%d'%(m.group(1),m.group(2),W.get(m.group(3),0))
    m=re.fullmatch(r'Pent0([mtwhfs])',k)
    if m: return 'Tempora/Pasc7-%d'%W[m.group(1)]
    m=re.fullmatch(r'Pent(\d+)',k)
    if m: return 'Tempora/Pent%02d-0'%int(m.group(1))
    return None
def introit(path):
    t=get('Latin',path,'Introitus')
    return key(t)[:22] if t else ''
files=[os.path.relpath(f,DO+'/Latin')[:-4] for f in glob.glob(DO+'/Latin/Tempora/*.txt')+glob.glob(DO+'/Latin/Sancti/*.txt')+glob.glob(DO+'/Latin/Commune/*.txt')]+['Commune/'+os.path.basename(f)[:-4] for f in glob.glob(DO+'/../horas/Latin/Commune/*.txt')]
INTR={}
for f in files:
    i=introit(f)
    if i: INTR.setdefault(i,[]).append(f)
out={}; miss=[]
for k,m in D['masses'].items():
    tf=tempfile(k)
    if tf and sections('Latin',tf):
        r={'src':tf}
        for sec,code in (('Oratio','or'),('Secreta','se'),('Postcommunio','pc')):
            la=get('Latin',tf,sec); en=get('English',tf,sec)
            if la: r[code]=[la.replace('J','I').replace('j','i'),en or '']
        if 'or' in r: out[k]=r; continue
    ids=[c['id'] for c in m['parts'].get('in',[]) if c.get('id')]
    if not ids: miss.append((k,'no introit')); continue
    inc=key(re.sub(r'\(.*?\)','',D['chants'][str(ids[0])]['i']))[:22]
    n=min(12,len(inc)); cand=[f for i,fs in INTR.items() if len(i)>=n and i[:n]==inc[:n] and n>=6 for f in fs]
    if not cand: miss.append((k,'no DO introit '+inc)); continue
    if k.startswith('S'):
        mm=k[1:3]+'-'+k[3:5]
        dated=[f for f in cand if f.startswith('Sancti/'+mm)]
        if not dated: miss.append((k,'saint not on its date in DO')); continue
        STOP={'sancti','sanctae','sanctorum','confessoris','martyris','virginis','episcopi','ecclesiae','doctoris','abbatis','pontificis','apostoli','apostolorum','martyrum','viduae','mariae','beatae','beati','regis','ordinis','praedicatorum'}
        tt=unicodedata.normalize('NFD',m['title'].lower().replace('æ','ae').replace('œ','oe').replace('j','i')).encode('ascii','ignore').decode()
        mine={w for w in re.findall(r'[a-z]{5,}',tt) if w not in STOP}
        ok=[]
        for f in dated:
            t=' '.join(sections('Latin',f).get('Officium',[])+sections('Latin',f).get('Rank',[]))
            tk=unicodedata.normalize('NFD',t.lower().replace('æ','ae').replace('œ','oe').replace('j','i')).encode('ascii','ignore').decode()
            words={w for w in re.findall(r'[a-z]{5,}',tk) if w not in STOP}
            if any(a[:5]==b[:5] for a in mine for b in words): ok.append(f)
        if not ok: miss.append((k,'saint on its date in DO is another saint')); continue
        cand=ok
    elif k.startswith('C'):
        t=[f for f in cand if f.startswith('Commune/')] or cand
        cand=sorted(t,key=len)
    else:
        t=[f for f in cand if f.startswith('Tempora/')] or cand
        cand=sorted(t,key=len)
    f=cand[0]; r={'src':f}
    for sec,code in (('Oratio','or'),('Secreta','se'),('Postcommunio','pc')):
        la=get('Latin',f,sec); en=get('English',f,sec)
        if la: r[code]=[la.replace('J','I').replace('j','i'),en or '']
    if 'or' in r: out[k]=r
    else: miss.append((k,'no oratio in '+f))
open(SITE+'/data/orations.js','w').write('window.ORATIONS = '+json.dumps(out,ensure_ascii=False,separators=(',',':'))+';\n')
print(len(out),'masses;',len(miss),'without:')
for k,w in miss: print(' ',k,D['masses'][k]['title'][:50],'-',w)
