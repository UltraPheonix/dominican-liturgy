import sys,re,json,os
sys.path.insert(0,'/tmp/A2')
from lib import load
ROOT='/home/claude/dominican-liturgy'
M=load('data/masses.js'); CH=M['chants']
O=load('data/orations.js'); R=load('data/readings33.js')
def gtext(i):
    f=ROOT+'/gabc/%s.gabc'%i
    if not os.path.exists(f): return '(no gabc)'
    s=open(f,encoding='utf8').read()
    hdr,_,body=s.partition('%%')
    book=re.search(r'book:(.*?);',hdr); book=book.group(1) if book else '?'
    t=re.sub(r'\([^)]*\)','',body); t=re.sub(r'<[^>]+>','',t); t=re.sub(r'\s+',' ',t).strip()
    return book+' | '+t[:260]
for k in sys.argv[1:]:
    m=M['masses'].get(k)
    if not m: print(k,'NO MASS'); continue
    print('=====',k,'|',m['title'],'|',m.get('en'),'| G page',m.get('page'),'| color',m.get('color'))
    for p,lst in m['parts'].items():
        for x in lst:
            i=str(x.get('id')); c=CH.get(i,{})
            print('  %-3s %-6s G%s %-30s :: %s'%(p,i,c.get('pg'),c.get('i'),gtext(i)))
    if m.get('extras'): print('  extras',json.dumps(m['extras'],ensure_ascii=False)[:300])
    if m.get('note'): print('  note',m['note'])
    o=O.get(k,{})
    for f in o:
        if f=='src': print('  orsrc',o[f]); continue
        if isinstance(o[f],list): print('  %s LA: %s\n     EN: %s'%(f,o[f][0],o[f][1] if len(o[f])>1 else ''))
    for n,r in enumerate(R.get(k,[])):
        print('  R%d %s | %s | %s\n     LA: %s\n     EN: %s'%(n,r.get('type'),r.get('ref'),r.get('title'),r.get('la'),r.get('en')))
