import json,glob,re,sys,os
P=json.load(open('/tmp/A2/props.json'))
OV={}
for f in sorted(glob.glob('/tmp/A2/ov/*.py')):
    d={}; exec(open(f).read(),d); OV.update(d['OV'])
SRCPAGE=json.load(open('/tmp/A2/srcpage.json')) if os.path.exists('/tmp/A2/srcpage.json') else {}
def pagecite(pdfs):
    a,b=pdfs
    import sys; sys.path.insert(0,'/tmp/A2')
    return a,b
fixes=[]; problems=[]
for k,v in P.items():
    o=OV.get(k,[])
    if o=='skip': continue
    new=v['new']
    if isinstance(o,dict): new=o['new']; o=o.get('subs',[])
    for t in o:
        a,b=t[0],t[1]
        if a not in new:
            if len(t)<3: problems.append((k,'override not found',a))
            continue
        new=new.replace(a,b)
    new=re.sub(r' {2,}',' ',new)
    if '¿' in new: problems.append((k,'unresolved ¿',re.findall(r'\S*¿\S*',new)))
    if new!=v['old']:
        fixes.append({'k':k,'file':v['file'],'path':v['path'],'old':v['old'],'new':new,'pdf':v['pages']})
json.dump(fixes,open('/tmp/A2/fixes_raw.json','w'),ensure_ascii=False,indent=0)
for p in problems: print('PROBLEM',*p)
print(len(fixes),'fixes')
