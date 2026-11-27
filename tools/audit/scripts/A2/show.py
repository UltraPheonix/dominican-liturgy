import json,sys,difflib,re
P=json.load(open('/tmp/A2/props.json'))
for k,v in P.items():
    if k.split('|')[0] not in sys.argv[1:]: continue
    o,n=v['old'],v['new']
    print('==',k,'pdf',v['pages'], 'SAME' if o==n else '')
    if o==n: continue
    a=re.findall(r'\S+',o); b=re.findall(r'\S+',n)
    out=[]
    for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if op=='equal':
            seg=a[i1:i2]
            out.append(' '.join(seg) if len(seg)<=8 else ' '.join(seg[:3])+' … '+' '.join(seg[-3:]))
        else: out.append('[-'+' '.join(a[i1:i2])+'-|+'+' '.join(b[j1:j2])+'+]')
    print('  ',' '.join(out))
