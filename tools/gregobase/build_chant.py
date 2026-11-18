# Office chant: find, for every antiphon, hymn and short responsory of the generated Office, the Dominican
# melody (GregoBase first, then the supplement), and write site/data/chant/.
import json, re, os, glob, unicodedata, difflib, collections, sys
SITE='/home/claude/build/site'; B=SITE+'/data/office/'
GB=json.load(open('gb_op.json'))
SUP=json.load(open('supplement.json')) if os.path.exists('supplement.json') else {}
# chants transcribed by hand from the Regulae Cantus O.P. (1965) and other scans: preferred over everything
MAN=json.load(open('manual.json')) if os.path.exists('manual.json') else {}
for k,v in MAN.items():
    v.setdefault('ver','Dominican'); v.setdefault('comm',None)
    v['text']=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',re.sub(r'\([^)]*\)','',v['gabc']))).strip()
SUP.update(MAN)
common=json.load(open(B+'common.json')); shards={}
def expand(t):
    out=[]
    for l in t.split('\n'):
        if l.startswith('§'):
            k=l[1:]; s=k[:2]
            if s not in shards: shards[s]=json.load(open(B+'psalter/'+s+'.json'))
            out.append(shards[s].get(k,''))
        else: out.append(l)
    return '\n'.join(out).split('\n')
def strip(l): return re.sub(r'<[^>]+>','',l)
def key(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    s=s.replace('æ','ae').replace('œ','oe').replace('j','i')
    return re.sub(r'[^a-z]','',s)
def words(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    s=s.replace('æ','ae').replace('œ','oe').replace('j','i')
    s=re.sub(r'\be u o u a e\b.*$','',s)
    return re.sub(r'[^a-z ]',' ',s).split()
# segments of a Latin cell: (kind, text used for matching, key)
def segments(lines):
    segs=[]; i=0; n=len(lines)
    while i<n:
        l=lines[i]
        if l.startswith('<r>Ant.</r>'):
            t=strip(l)[4:].strip(); segs.append(('an',t,key(t),t))
        elif re.match(r'^<[rh]>Hymnus</[rh]>$',l.strip()) or (l.startswith('<h>') and 'Hymnus' in l and l.strip().endswith('Hymnus</h>')):
            j=i+1
            while j<n and not lines[j].strip(): j+=1
            if j<n:
                e=j
                while e<n and not re.match(r'^Amen\.?$',strip(lines[e]).strip()) and not lines[e].startswith('<r>℣.</r>'): e+=1
                full=' '.join(strip(x) for x in lines[j:e+1])
                t=' '.join(strip(x) for x in lines[j:j+4]); segs.append(('hy',t,'hy'+key(strip(lines[j])),full))
        elif l.startswith('<r>℟.br.</r>'):
            t=strip(l)[5:].strip(); segs.append(('rb',t,'rb'+key(t),t))
        i+=1
    return segs
want={}
for f in sorted(glob.glob(B+'20??/*.json')):
    day=json.load(open(f))
    for h,rows in day['h'].items():
        for r in rows:
            for kind,t,k,full in segments(expand(day['b'].get(r[0]) or common.get(r[0],''))):
                w=want.setdefault(k,{'kind':kind,'t':t,'full':full,'n':0,'hours':collections.Counter()}); w['n']+=1; w['hours'][h]+=1
PRI={'AR1912':20,'LU1961':21,'RC1965':-1,'THOMPSON-a1':6,'THOMPSON-a2a':6,'THOMPSON-a2b':6,'THOMPSON-a3':6,'THOMPSON-a4':6,'AOP1933':0,'COP1949':0,'MOP1936':1,'POP1913':2,'HSOP1965':2,'GOP1950':3,'AOP1862a':4,'AOP1862b':4}
PART={'an':{'an'},'hy':{'hy'},'rb':{'rb','re'}}
cands=collections.defaultdict(list)
for cid,e in list(GB.items())+[(k,v) for k,v in SUP.items()]:
    w=words(e['text'])
    if len(w)>=2: cands[tuple(w[:2])].append((cid,w))
def best(kind,t):
    w=words(t); b=None
    for cid,gw in cands.get(tuple(w[:2]),[]):
        e=GB.get(cid) or SUP.get(cid)
        if e['part'] not in PART[kind]: continue
        if e.get('roman') and kind=='hy': continue
        if kind=='hy': r=difflib.SequenceMatcher(None,w[:12],gw[:12]).ratio()
        else:
            gw2=gw[:len(w)+2]
            r=difflib.SequenceMatcher(None,w,gw2).ratio()
        pri=min(PRI.get(s[0],5) for s in e['src']) if 'src' in e else 6
        tier=0 if pri>=20 else (1 if pri==6 else 2)
        score=(tier, r, -pri)
        if r>=0.8 and (not b or score>b[0]): b=(score,cid)
    return b and b[1]
out={}; used=set(); stat=collections.Counter(); miss=[]
for k,w in want.items():
    cid=best(w['kind'],w['t'])
    day=sum(v for h,v in w['hours'].items() if h!='Matutinum')
    stat[w['kind'],'ok' if cid else 'miss']+=w['n']; stat[w['kind'],'day-'+('ok' if cid else 'miss')]+=day
    if cid:
        e=GB.get(cid) or SUP.get(cid)
        tp=1 if re.search(r'allel[uú]+[ij]a\W*$',w['t'],re.I) else 0
        whole=1 if w['kind']!='hy' or len(words(e['text']))>=0.8*len(words(w['full'])) else 0
        out[k]=[cid,e.get('mode') or '',tp,whole,e.get('mvar') or '']+(['R'] if e.get('roman') else []); used.add(cid)
    elif day: miss.append((day,w['kind'],w['t'][:80],sorted(w['hours'])))
os.makedirs(SITE+'/data/chant/op',exist_ok=True)
used.update(['4206','4227','7984','7985','7986','7993','7994'])   # Benedicamus Domino I-VII (js/tones.js)
for cid in used:
    e=GB.get(cid) or SUP.get(cid)
    g=e['gabc']
    if '%%' in g: g=g.split('%%',1)[1]
    open(SITE+f'/data/chant/op/{cid}.gabc','w').write(g.strip()+'\n')
json.dump(out,open(SITE+'/data/chant/office.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(sorted(miss,reverse=True),open('missing.json','w'),ensure_ascii=False,indent=0)
print(stat); print(len(out),'keys',len(used),'chants')
for m in sorted(miss,reverse=True)[:15]: print(m)
