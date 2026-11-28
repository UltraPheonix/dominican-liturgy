# auto.py KEY "P-items" "C-items" OUT.json : build full-text fix entries from accepted review items (P = punctuation items of
# review.py numbering, C = case items of rvc.py numbering), grouped per field; prints a word diff for checking.
import json,sys,re,unicodedata,difflib
sys.argv_save=sys.argv[:]; sys.argv=[sys.argv[0]]
exec(open('/tmp/A1/cmp.py').read().split('S=json.load')[0])
sys.path.insert(0,'/tmp/A1'); import review
sys.argv=sys.argv_save
k=sys.argv[1]
P=[int(x) for x in sys.argv[2].split(',') if x.strip()] if len(sys.argv)>2 else []
C=[int(x) for x in sys.argv[3].split(',') if x.strip()] if len(sys.argv)>3 else []
out=sys.argv[4]
its=review.items(k); CI=json.load(open('/tmp/A1/case_s3.json')).get(k,[])
O=load('data/orations.js'); R=load('data/readings33.js')
def target(lab):
    if lab.startswith('or.'): return 'data/orations.js',(k,lab.split()[0][3:],0)
    m=re.match(r'rd\.(\d+)',lab); return 'data/readings33.js',(k,int(m.group(1)),'la')
def get(fn,path):
    d=O if 'orations' in fn else R
    for p in path: d=d[p]
    return d
CAPS=str.maketrans({'Á':'A','É':'E','Í':'I','Ó':'O','Ú':'U','Ý':'Y','Ǽ':'Æ'})
edits={}
for n in P:
    it=its[n]; assert it['kind']=='P',(n,it)
    edits.setdefault(target(it['lab']),[]).append(('P',it['a'],it['site'],it['missal']))
for n in C:
    it=CI[n]; edits.setdefault(target(it['lab']),[]).append(('C',it['a'],it['site'],it['missal']))
spec=[]
for (fn,path),E in edits.items():
    path=list(path); t=get(fn,path); T=toks_site(t)
    ops=[]
    for kind,a,s,m in E:
        tk=T[a]
        if kind=='P':
            assert tk[1]==s,(a,tk,s)
            if s=='': ops.append((tk[4],tk[4],m))
            else: ops.append((tk[5],tk[6],m))
        else:
            w=tk[2]; assert fold(w)==fold(s),(w,s)
            nw=(w[0].upper().translate(CAPS)+w[1:]) if m[0].isupper() else (w[0].lower()+w[1:])
            if w[0] in 'ÁÉÍÓÚǼ' and not m[0].isupper(): nw=w[0].lower()+w[1:]
            ops.append((tk[3],tk[3]+1,nw[0]))
    new=t
    for a,b,r in sorted(ops,reverse=True): new=new[:a]+r+new[b:]
    A=t.split(); B=new.split(); sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal': print(path,' '.join(A[max(0,i1-2):i2]),'=>',' '.join(B[max(0,j1-2):j2]))
    spec.append({"file":fn,"path":path,"new":new,"src":"","why":""})
json.dump(spec,open(out,'w'),ensure_ascii=False,indent=0); print('wrote',out,len(spec))
