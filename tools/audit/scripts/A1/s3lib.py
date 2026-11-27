import json, re, sys, copy
sys.path.insert(0,'/tmp/A1')
ROOT='/home/claude/dominican-liturgy/'
FN=ROOT+'tools/audit/fixes/A1.json'
def load(fn):
    s=open(ROOT+fn,encoding='utf8').read()
    i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end()
    j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
O=load('data/orations.js'); R=load('data/readings33.js'); MS=load('data/masses.js')
DATA={'data/orations.js':O,'data/readings33.js':R,'data/masses.js':MS}
from douay import verses
def V(book,ch,v):
    r=[t for n,t in verses(book,ch,v,v)]
    assert r,(book,ch,v); return r[0]
def VV(book,ch,a,b): return ' '.join(t for n,t in verses(book,ch,a,b))
def cur(file,path):
    d=DATA[file]
    for p in path: d=d[p]
    return d
ENTRIES=[]
def fix(file,path,new,src,why,old='__cur__'):
    o=cur(file,path) if old=='__cur__' else old
    if o==new: print('SAME',path); return
    ENTRIES.append({'file':file,'path':path,'old':o,'new':new,'src':src,'why':why,'s3':True})
def add(file,path,new,src,why):
    ENTRIES.append({'file':file,'op':'add','path':path,'old':None,'new':new,'src':src,'why':why,'s3':True})
def edit(file,path,pairs,src,why):
    s=cur(file,path)
    for a,b in pairs:
        assert s.count(a)==1,(path,a,s.count(a)); s=s.replace(a,b)
    fix(file,path,s,src,why)
