import pickle, re, json, difflib, collections, sys
sys.argv=['x']; exec(open('/tmp/dmv/seg.py').read().split("if __name__")[0])
E,L=streams(); SE,SL=segments(E),segments(L)
def join(lines):
    t=''
    for l in lines:
        l=l.strip()
        if not l: continue
        if t.endswith('-') and re.match(r'[a-z]', l): t=t[:-1]+l
        else: t=(t+' '+l) if t else l
    return re.sub(r'\s+',' ',t).strip()
byE=collections.defaultdict(list); byL=collections.defaultdict(list)
for s in SE:
    if s['typ']!='h': byE[s['p']].append(s)
for s in SL:
    if s['typ']!='h': byL[s['p']].append(s)
pairs=[]; unE=[]; unL=[]
for p in sorted(set(byE)|set(byL)):
    a=[s['typ'] for s in byE[p]]; b=[s['typ'] for s in byL[p]]
    sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
    ue=set(range(len(a))); ul=set(range(len(b)))
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal':
            for k in range(i2-i1):
                ue.discard(i1+k); ul.discard(j1+k)
                if a[i1+k]!='x': pairs.append({'typ':a[i1+k],'p':p,'en':join(byE[p][i1+k]['lines']),'la':join(byL[p][j1+k]['lines'])})
    unE+=[(p,byE[p][i]) for i in sorted(ue) if a[i]!='x']; unL+=[(p,byL[p][j]) for j in sorted(ul) if b[j]!='x']
print(len(pairs), collections.Counter(x['typ'] for x in pairs), 'unpaired E',len(unE),'L',len(unL))
pickle.dump((pairs,unE,unL),open('/tmp/dmv/pairs.pkl','wb'))
for p,s in unE[:10]: print('E',p,s['typ'],join(s['lines'])[:100])
for p,s in unL[:10]: print('L',p,s['typ'],join(s['lines'])[:100])
# second pass: unpaired prayers of the same kind on the same or the next page, in order
usedL=set(); extra=0
for i,(p,s) in enumerate(unE):
    for j,(q,t) in enumerate(unL):
        if j in usedL or t['typ']!=s['typ'] or abs(q-p)>1: continue
        usedL.add(j); extra+=1
        pairs.append({'typ':s['typ'],'p':p,'en':join(s['lines']),'la':join(t['lines']),'pass2':1}); break
print('pass2', extra, len(pairs))
pickle.dump((pairs,unE,unL),open('/tmp/dmv/pairs.pkl','wb'))
