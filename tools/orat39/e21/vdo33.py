import json,re,unicodedata,difflib,sys
sys.path.insert(0,'/home/claude/dominican-liturgy/tools/orat39')
def F(s):
    s=s.replace('æ','ae').replace('œ','oe').replace('Æ','ae').replace('Œ','oe').replace('ǽ','ae')
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('v','u'))
L=json.load(open('lines.json')); MP=json.load(open('map.json'))
o=open('/home/claude/dominican-liturgy/data/orations.js').read(); O=json.loads(o[o.index('{'):].rstrip().rstrip(';'))
CONC=re.compile(r'(Per (eúndem |eúmdem )?Dóminum|Qui vivis|Qui tecum|qui tecum|Qui vivit|Per eúndem|Qui cum Patre)')
def body(t):
    m=CONC.search(t); return t[:m.start()] if m else t
res={}
for k,v in O.items():
    if v.get('src','').startswith('Missale'): continue
    m=MP.get(k) or {}; st=m.get('start'); spans=[]
    if st is not None: spans.append((st,st+700))
    for r in m.get('readings') or []:
        if r.get('line'): spans.append((max(0,r['line']-90),r['line']+250))
    if m.get('common') and isinstance(m['common'][-1],int): spans.append((m['common'][-1],m['common'][-1]+500))
    if not spans: res[k]={'nomap':1}; continue
    seg=''.join(F(l[2][:-1] if l[2].endswith('\xad') else l[2]) for a,b in spans for l in L[a:b])
    res[k]={}
    for kind in ('or','se','pc'):
        if kind not in v: continue
        f=F(body(v[kind][0])); best=0
        for n,sk in ((20,0),(16,8),(16,24),(14,40)):
            q=f[sk:sk+n]; i=seg.find(q)
            while i>=0:
                a=max(0,i-sk); r=difflib.SequenceMatcher(None,seg[a:a+len(f)],f,autojunk=False).ratio(); best=max(best,r); i=seg.find(q,i+1)
        res[k][kind]=round(best,3)
json.dump(res,open('/tmp/vdo33.json','w'))
ok=[k for k,v in res.items() if 'nomap' not in v and v and min(v.values())>=0.93]
bad=[(k,v) for k,v in res.items() if k not in ok]
print(len(ok),'match M33 in their own Mass;',len(bad),'not')
for k,v in sorted(bad): print(k,v)
