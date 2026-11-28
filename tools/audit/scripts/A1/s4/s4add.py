# s4add.py SPEC.json : append session-4 fix entries to tools/audit/fixes/A1.json
# spec items: {"file","path","subs":[[old,new],...]} or {"file","path","new"} (+ "op":"add"), each with "src","why"
import json,re,sys,copy
ROOT='/home/claude/dominican-liturgy/'
FX=ROOT+'tools/audit/fixes/A1.json'
def load(fn):
    s=open(ROOT+fn,encoding='utf8').read()
    i=re.search(r'(?:var\s+\w+|window\.\w+)\s*=\s*',s).end(); j=max(s.rfind('}'),s.rfind(']'))+1
    return json.loads(s[i:j])
D={}
def get(fn,path):
    if fn not in D: D[fn]=load(fn)
    cur=D[fn]
    for k in path: cur=cur[k]
    return cur
F=json.load(open(FX,encoding='utf8'))
spec=json.load(open(sys.argv[1],encoding='utf8'))
JUNK=re.compile(r'¿|\.,|,\.|\s[,;:.]\S|  |Præd|\bpag\.|\s-\s|[A-Za-zǽ]\s+-|\bF\s|­')
bad=0; added=0
for it in spec:
    fn,path=it['file'],it['path']
    prior=[e for e in F if e['file']==fn and e['path']==path and e.get('s4')]
    if it.get('op')=='add':
        base=None
        try: base=get(fn,path)
        except (KeyError,IndexError): pass
        if base is not None and not prior: print('EXISTS',path); bad+=1; continue
        old=None; new=it['new']
    else:
        base=prior[-1]['new'] if prior else get(fn,path)
        old=copy.deepcopy(base)
        if 'subs' in it:
            new=base
            for a,b in it['subs']:
                n=new.count(a)
                if n!=1: print('SUB COUNT %d in %s: %r'%(n,path,a)); bad+=1; new=None; break
                new=new.replace(a,b)
            if new is None: continue
        else: new=it['new']
    if new==old: print('NOCHANGE',path); continue
    if isinstance(new,str):
        for m in JUNK.finditer(new): print('JUNK? %s: ...%s...'%(path,new[max(0,m.start()-25):m.end()+25]))
    e={'file':fn,'path':path,'old':old,'new':new,'src':it['src'],'why':it['why'],'s4':True}
    if it.get('op')=='add': e={'file':fn,'op':'add','path':path,'old':None,'new':new,'src':it['src'],'why':it['why'],'s4':True}
    if any(x['file']==fn and x['path']==path and x['new']==new for x in F): print('DUP',path); continue
    F.append(e); added+=1
if bad: print('ERRORS',bad,'- nothing written'); sys.exit(1)
json.dump(F,open(FX,'w',encoding='utf8'),ensure_ascii=False,indent=1)
print('added',added,'total',len(F))
