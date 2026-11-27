# list English text in A3 fixes (readings) that is not verbatim Douay (bible/en), segment by segment
import json,re,sys
sys.path.insert(0,'/tmp/A3')
from load import load
R=load('data/readings33.js')
B='/home/claude/dominican-liturgy/bible/en/'
def norm(s): return re.sub(r'[^a-z]+',' ',s.lower().replace('’',"'")).strip()
cache={}
def book(ref):
    b=re.match(r'(.+?)\s+\d+\s*:',ref).group(1).strip()
    if b not in cache:
        try: cache[b]=norm(' '.join(l.split('\t',2)[2] for l in open(B+b+'.txt',encoding='utf8') if l.count('\t')>=2))
        except FileNotFoundError: cache[b]=None
    return cache[b]
F=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A3.json'))
items=[]
for e in F:
    if e['file']!='data/readings33.js': continue
    p=e['path']
    if p[-1]=='en': items.append((p, R[p[0]][p[1]]['ref'] if p[0] in R else '?', e['new']))
    elif isinstance(e['new'],list):
        for n,x in enumerate(e['new']): items.append((p+[n], x['ref'], x['en']))
    elif isinstance(e['new'],dict): items.append((p, e['new']['ref'], e['new']['en']))
for p,ref,en in items:
    bk=book(ref)
    if bk is None: print(p,'NO BOOK',ref); continue
    segs=[s for s in re.split(r'[.;:?!]\s+|,\s+(?=[A-Z])',en.replace('At that time:','')) if s.strip()]
    bad=[s for s in segs if norm(s) and norm(s) not in bk and not s.strip().endswith('(AI translation)')]
    if bad: print(p, ref, '|', ' || '.join(bad)[:400])
