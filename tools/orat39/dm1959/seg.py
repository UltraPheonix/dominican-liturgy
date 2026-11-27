import pickle, re, json, difflib, sys
ROWS=pickle.load(open('/tmp/dmv/rows.pkl','rb'))
EN=set('the and of to you we that your our may us who which be by with for his her is are lord god through this those they he she them all have has from as on'.split())
LA=set('et ut nos qui quae quod tua tuam tuae tui nobis quaesumus domine deus per est ad cum sunt eius ejus te tibi atque ac dominum nostri nostrae nostra sicut non quia'.split())
def score(row):
    ws=re.findall(r'[a-z]+', ' '.join(o['t'] for o in row).lower())
    return sum(w in EN for w in ws)-sum(w in LA for w in ws)
def split(rows):
    body=[r for r in rows if r[0]['y']>24]
    s=[score(r) for r in body]
    best=(-1e9,len(body))
    for k in range(0,len(body)+1):
        if 0<k<len(body) and body[k][0]['y']-body[k-1][0]['y']<14: continue
        v=sum(s[:k])-sum(s[k:])
        if v>best[0]: best=(v,k)
    k=best[1]
    return body[:k], body[k:]
RUB=re.compile(r'\bp\.\s*\d|^\s*(Creed|Kyrie|Gloria|Preface|Offertory Prayers|Omit|Mass:|Memory of the|Commemoration of the Feria)', re.I)
def keep(o, rowfirst):
    t=o['t']
    if not re.search(r'[A-Za-z]{2}', t): return False
    if o['x']>110 and (o['it']>.5 or RUB.search(t)): return False
    if o['it']>.6 and RUB.search(t): return False
    return True
LAB_EN={'collect':'or','secret':'se','postcommunion':'pc','office':'x','introit':'x','epistle':'x','lesson':'x','gospel':'x','gradual':'x','responsory':'x','tract':'x','sequence':'x','offertory':'x','communion':'x','alleluia':'x','prayer':'?','preface':'x','prophecy':'x'}
LAB_LA={'oratio':'or','secreta':'se','postcommunio':'pc','officium':'x','introitus':'x','lectio':'x','epistola':'x','evangelium':'x','graduale':'x','responsorium':'x','tractus':'x','sequentia':'x','offertorium':'x','communio':'x','alleluia':'x','praefatio':'x','prophetia':'x'}
def label(t, lang):
    m=re.match(r'^[\W\d_]{0,6}([A-Za-z]{4,14})\b\s?([.,~:;]?)', t)
    if not m: return None
    w=m.group(1).lower(); V=LAB_EN if lang=='en' else LAB_LA
    best=max(V, key=lambda v: difflib.SequenceMatcher(None,w,v).ratio())
    r=difflib.SequenceMatcher(None,w,best).ratio()
    if r<0.8: return None
    typ=V[best]
    rest=t[m.end():]
    if lang=='en' and typ=='?':
        if re.match(r'\s*over\s+the\s+people', rest, re.I): return ('sp', re.sub(r'^\s*over\s+the\s+people\W*','',rest,flags=re.I))
        if m.group(2)=='.': return ('or', rest)
        return None
    if lang=='la' and typ=='or' and re.match(r'\s*super\s+popul\w*\W*', rest, re.I): return ('sp', re.sub(r'^\s*super\s+popul\w*\W*','',rest,flags=re.I))
    # a prayer label must be followed by punctuation or a capital
    if typ!='x' and not (m.group(2) or re.match(r'\s+[A-Z]', rest)): return None
    if typ=='x' and not m.group(2): return None
    return (typ, rest)
CAPS=re.compile(r'^[^a-z]*$')
def streams():
    E=[];L=[]
    for pno,rows in enumerate(ROWS):
        if pno<20: continue
        e,l=split(rows)
        for half,out,lang in ((e,E,'en'),(l,L,'la')):
            for r in half:
                objs=[o for o in r if keep(o, r[0])]
                if not objs: continue
                t=' '.join(o['t'].strip() for o in objs)
                letters=re.sub(r'[^A-Za-z]','',t)
                caps= len(letters)>=6 and sum(c.isupper() for c in letters)/len(letters)>.8
                out.append({'p':pno,'t':t,'caps':caps,'lab':label(t,lang)})
    return E,L
def segments(S):
    segs=[]; cur=None
    for i,r in enumerate(S):
        if r['lab']:
            cur={'typ':r['lab'][0],'p':r['p'],'lines':[r['lab'][1]]}; segs.append(cur); continue
        if r['caps'] or re.match(r'^\W*(Memory of|Commemoration of|Commemoratio|Memoria)\b', r['t']):
            cur=None; segs.append({'typ':'h','p':r['p'],'lines':[r['t']]}); continue
        if cur is not None: cur['lines'].append(r['t'])
    return segs
if __name__=='__main__':
    E,L=streams()
    SE,SL=segments(E),segments(L)
    pickle.dump((SE,SL),open('/tmp/dmv/segs.pkl','wb'))
    import collections
    print(collections.Counter(s['typ'] for s in SE)); print(collections.Counter(s['typ'] for s in SL))
