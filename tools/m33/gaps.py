import json, re
import dpmap as D, mapall as M
d = json.load(open('dpmap.json'))
for sec in ('tempore','commune','votivae'):
    keys=[k for k in D.SEC[sec] if not k.startswith('Quad6')]
    for i,k in enumerate(keys):
        if d.get(k) is not None: continue
        prev=next((d[keys[j]] for j in range(i-1,-1,-1) if d.get(keys[j])),None)
        nxt=next((d[keys[j]] for j in range(i+1,len(keys)) if d.get(keys[j])),None)
        print('==',k,repr(M.INTR.get(k,'')),prev,nxt)
        if prev is None or nxt is None: continue
        for li in range(prev+1,nxt):
            l=M.L[li][2]
            if M.kind(l)=='introit' or re.match(r'^\W{0,2}(Offi|Intr|0ffi|Ofï)',l):
                print('  ',li,M.L[li][0],M.kind(l),l[:50],'|',M.L[li+1][2][:40])
