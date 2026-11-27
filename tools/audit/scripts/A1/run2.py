import sys; sys.path.insert(0,'/tmp/A1')
exec(open('/tmp/A1/cmp.py').read())
import os
M=load('data/masses.js')['masses']; O=load('data/orations.js'); R=load('data/readings33.js')
G=json.load(open(ROOT+'tools/audit/groups.json'))['A1']
CONCL=re.compile(r'\s((?:Per (?:eúndem |eúmdem |eumdem |eundem )?(?:Dóminum|Dominum|Christum)|Per (?:eúndem|eúmdem|eumdem|eundem)(?=\.)|Qui (?:tecum|vivis|cum Patre|vivit|venturus|cum Deo))\b.*)$')
def gabctext(id):
    fn=ROOT+'gabc/%s.gabc'%id
    if not os.path.exists(fn): return None
    s=open(fn,encoding='utf8').read()
    s=s.split('%%',1)[-1]
    s=re.sub(r'\([^)]*\)','',s); s=re.sub(r'<[^>]*>','',s); s=re.sub(r'\{|\}|\[[^\]]*\]','',s)
    s=s.replace('*','').replace('†','').replace('℣','').replace('℟','')
    return re.sub(r'\s+',' ',s).strip()
def texts(k):
    out=[]
    o=O.get(k,{})
    for f in ['or','se','pc','sp']:
        if f in o:
            la=o[f][0]; m=CONCL.search(la)
            body=la[:m.start()] if m else la
            out.append(('or.'+f, body, m.group(1) if m else ''))
    for n,r in enumerate(R.get(k,[])):
        out.append(('rd.%d %s %s'%(n,r['type'],r['ref']), r['la'],''))
    for p,v in M[k]['parts'].items():
        for n,c in enumerate(v):
            t=gabctext(c.get('id'))
            out.append(('ch.%s.%d #%s'%(p,n,c.get('id')), t or '', ''))
    return out
os.makedirs('/tmp/A1/diff2',exist_ok=True)
summ=[]
RNG=tuple(map(int,os.environ['A1RANGE'].split('-'))) if os.environ.get('A1RANGE') else None
ITEMS={}
LOC={}
keys=sys.argv[1:] or G
for k in keys:
    L=[]; T=texts(k); IT=ITEMS.setdefault(k,[])
    cands={}
    for lab,t,c in T:
        st=toks_site(t)
        if len(st)<3: cands[lab]=[]; continue
        v=locate(st,*RNG) if RNG else locate(st)
        cands[lab]=[(p*8,n) for p,n in v.most_common(6) if n>=max(2,v.most_common(1)[0][1]*0.6)]
    # cluster center: median of top cand positions of orations+readings
    tops=[c[0][0] for l,c in cands.items() if c and not l.startswith('ch')]
    tops.sort(); center=tops[len(tops)//2] if tops else 0
    for lab,t,concl in T:
        st=toks_site(t)
        c=cands[lab]
        if not c: L.append('## %s: NOT FOUND (%d words)  %s'%(lab,len(st),t[:80])); continue
        best=max(c,key=lambda x:(x[1]>=c[0][1]*0.6)*1e9 - abs(x[0]-center))
        start=best[0]
        ops,a0=align(st,start)
        # first/last equal
        eqs=[o for o in ops if o[0]=='equal']
        ms=a0+eqs[0][3]; me=a0+eqs[-1][4]
        LOC.setdefault(k,{})[lab.split(' #')[0].split(' ')[0] if lab.startswith('rd') else lab.split(' #')[0]]=[MT[ms][3][0],MT[me-1][3][-1]]
        L.append('## %s  pdf %d-%d  match %d/%d  %s'%(lab,pdf(ms),pdf(me-1),sum(o[2]-o[1] for o in eqs),len(st),('CONCL: '+concl) if concl else ''))
        for tag,i1,i2,j1,j2 in ops:
            J1,J2=a0+j1,a0+j2
            if tag=='equal':
                for a,b in zip(range(i1,i2),range(J1,J2)):
                    if st[a][1]!=MT[b][1]:
                        if lab.startswith('ch'): continue
                        nxt=MT[b+1][2] if b+1<len(MT) else ''
                        if MT[b][1]=='.' and st[a][1]==',' and nxt and nxt[:1].islower(): continue
                        IT.append(dict(lab=lab,kind='P',a=a,site=st[a][1],missal=MT[b][1],si=MT[b][3][-1],word=st[a][2],ctx=' '.join(x[2] for x in st[max(0,a-3):a+3])))
                        L.append('  P %-18s site[%s] missal[%s]  @%d:%s  ctx: %s'%(st[a][2],st[a][1],MT[b][1],pdf(b),MT[b][3][0],' '.join(x[2] for x in st[max(0,a-3):a+3])))
            else:
                if J1<ms or J1>=me:
                    if tag!='insert': L.append('  %s site-only at edge: %s'%(tag,' '.join(x[2]+x[1] for x in st[i1:i2])))
                    else:
                        pass
                    continue
                IT.append(dict(lab=lab,kind='W',tag=tag,i1=i1,i2=i2,site=' '.join(x[2]+x[1] for x in st[i1:i2]),missal=' '.join((x[2] or '')+x[1] for x in MT[J1:J2]),si=MT[J1][3][0] if J1<len(MT) else -1))
                L.append('  W %s site: %s | missal: %s  @%d:%s'%(tag,' '.join(x[2]+x[1] for x in st[i1:i2]),' '.join((x[2] or '')+x[1] for x in MT[J1:J2]),pdf(J1) if J1<len(MT) else -1,MT[J1][3][0] if J1<len(MT) else -1))
        # trailing missal text beyond site end (truncation check for readings)
        if lab.startswith('rd'):
            tail=' '.join((x[2] or '')+x[1] for x in MT[me:me+15])
            L.append('  TAIL after: %s'%tail)
    open('/tmp/A1/diff2/%s.txt'%k,'w').write('\n'.join(L))
    summ.append('%s %d lines'%(k,len(L)))
print('\n'.join(summ))
json.dump(LOC,open('/tmp/A1/x2loc_%s.json'%('_'.join(keys) if len(keys)<4 else 'all'),'w'))
json.dump(ITEMS,open('/tmp/A1/x2items_%s.json'%('_'.join(keys) if len(keys)<4 else 'all'),'w'),ensure_ascii=False,indent=0)
