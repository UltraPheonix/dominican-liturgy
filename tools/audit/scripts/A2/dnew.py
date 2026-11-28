# show word diffs of fix entries after index N
import json,sys,difflib,re
cur=json.load(open('/home/claude/dominican-liturgy/tools/audit/fixes/A2.json'))
for e in cur[int(sys.argv[1]):]:
    o,n=e['old'],e['new']
    print('==',e['path'],e['src'], e.get('op',''))
    if not isinstance(o,str) or not isinstance(n,str): print('   NEW:',json.dumps(n,ensure_ascii=False)[:1500]); continue
    a=re.findall(r'\S+',o); b=re.findall(r'\S+',n); out=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if op!='equal': out.append('[-'+' '.join(a[i1:i2])+'-|+'+' '.join(b[j1:j2])+'+]')
    print('  ',' '.join(out))
