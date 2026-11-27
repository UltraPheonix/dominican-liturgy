import json,re,sys
from align import *
from pmap import *
from load import *
O=load('data/orations.js'); RD=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']; CH=D['chants']
G=json.load(open('/home/claude/dominican-liturgy/tools/audit/groups.json'))['A4']
DIE=re.compile(r'^(Die \d+|Dominica|Feria|In Vigilia|Festa \w+$)')
def norm_concl(s):
    w=[fold(t) for t,_ in toks(s) if t not in ',;:.?!']
    return w
def concl_after(r):
    i=r['endi']; return [t[1] for t in MS[i:i+12]]
NOISE={'arnen':'amen'}
RWIN=json.load(open('/tmp/A4/rwin.json')) if __import__('os').path.exists('/tmp/A4/rwin.json') else {}
OCR=[('se','ae'),('rn','m'),('fesu','iesu'),('ii','u'),('cte','cte')]
def ocr_eq(a,b):
    B=b
    if not any(c.isalpha() for c in a) or not any(c.isalpha() for c in b): return False
    if [x for x in a.split() if x in ',;:.?!']!=[x for x in b.split() if x in ',;:.?!']: return False
    a=''.join(fold(x) for x in a.split()); b=''.join(fold(x) for x in b.split())
    a=''.join(c for c in a if c.isalpha()); b=''.join(c for c in b if c.isalpha())
    if a==b: return True
    for x,y in OCR:
        if b.replace(x,y)==a: return True
    # heading words before the first word: Missal side ends with the site word
    if len(a)>2 and len(B.split())>=3 and b.endswith(a): return True
    return False
HDR=set('festa maii iunii iulii augusti septembris octobris novembris proed proprium sanctorum de'.split())
CROPS=[]
def keep(d):
    t,a,b,c,ln,j1,j2=d[:7]
    fb=[fold(x) for x in b.split()]; fa=[fold(x) for x in a.split()]
    if t=='insert' and all(x in HDR or len(x)<=3 for x in fb): return False
    if t=='replace' and [NOISE.get(x,x) for x in fb]==fa: return False
    if t=='replace' and ocr_eq(a,b): return False
    return True
def fmt(k,lab,r):
    out=[]
    for n,d in enumerate([d for d in r['diffs'] if keep(d)]):
        t,a,b,c,ln,j1,j2=d[:7]
        ctx=' '.join(x[1] for x in MS[max(0,j1-3):j2+3] if x[1] not in ',;:.?!')
        pg=pageof(MS[j1][2])[1]
        CROPS.append([pg,ctx,f"{k} {lab} #{n}: site[{a}] M[{b}]".replace("[","(").replace("]",")")])
        out.append(f"#{n} {t}[{a}|{b}]<{c}>")
    return '; '.join(out)
def section(line):
    a=line
    while a>0 and not DIE.match(L[a].strip()): a-=1
    return a
def endsec(line):
    b=line+1
    while b<len(L) and not re.match(r'^Die \d+',L[b].strip()): b+=1
    return b
def run(k,out):
    o=O.get(k,{}); m=M.get(k,{})
    pg=pages_from(o.get('src','')) or pages_from('p. '+str(m.get('page','')))
    win=None
    if pg and pg[0] in P2L:
        l0=P2L[pg[0]]; l1=P2L.get(pg[1],l0)
        win=(l0-30,l1+420)
    out.append(f"===== {k} | site title: {m.get('title')} | src: {o.get('src','')[:90]} | win {win}")
    first=None
    for p in ('or','se','pc'):
        if not o.get(p): out.append(f"  {p}: MISSING"); continue
        la=o[p][0]; mm=CONCL.search(la); body=la[:mm.start()] if mm else la
        r=compare(body,win[0] if win else None,win=win)
        if not r: out.append(f"  {p}: NOT FOUND {la[:70]}"); continue
        if first is None or r['line']<first: first=r['line']
        ca=concl_after(r)
        dd=fmt(k,p,r)
        sc=[fold(x) for x,_ in toks(mm.group(0))][:2] if mm else []
        mc=[fold(x) for x in ca if x not in ',;:.?!'][:2]
        flag='' if sc[:1]==mc[:1] and (len(sc)<2 or sc[1].replace('eundem','eumdem')==mc[1].replace('eundem','eumdem')) else ' **CONCL?**'
        ej=('eiusdem' in [fold(x) for x,_ in toks(mm.group(0))]) if mm else False
        mej='eiusdem' in [fold(x) for x in ca]
        if ej!=mej: flag+=' **EIUSDEM?**'
        out.append(f"  {p}{flag} {r['score']:.2f} p{r['page'][0]}(pdf{r['page'][1]}) L{r['line']} concl site:{(mm.group(0)[:40] if mm else 'NONE')!r} M:{' '.join(ca)[-110:]}")
        if dd: out.append(f"     DIFF {dd}")
        en=o[p][1] if len(o[p])>1 else ''
        out.append(f"     EN: {en[:70]} ... {en[-50:]}")
    if first:
        a=section(first); b=endsec(first)
        out.append(f"  SECTION L{a}-{b}: "+' '.join(x.strip() for x in L[a:min(b,a+400)] if x.strip() and not x.startswith('@@'))[:6000])
    # readings
    rw=win
    if k in RWIN: l0=P2L[RWIN[k]]; rw=(l0-200,l0+600)
    for r in (RD.get(k) or []):
        res=compare(r['la'],rw[0] if rw else None,win=rw)
        if res and res['score']<0.3: res=compare(r['la'],rw[0] if rw else None)
        if not res: out.append(f"  READ {r['type']} {r['ref']}: NOT FOUND"); continue
        h=' '.join(L[x].strip() for x in range(res['line']-4,res['line']))
        dd=fmt(k,r['type'][:3],res)
        ca=concl_after(res)
        out.append(f"  READ {r['type']} ref={r['ref']} title={r.get('title')} {res['score']:.2f} p{res['page'][0]}(pdf{res['page'][1]}) L{res['line']}\n     HEAD: {h[-160:]}\n     AFTER: {' '.join(ca)[-120:]}")
        if dd: out.append(f"     DIFF {dd}")
        out.append(f"     LA: {r['la'][:60]} ... {r['la'][-60:]}\n     EN: {r.get('en','')[:60]} ... {r.get('en','')[-60:]}")
    if not RD.get(k): out.append(f"  READINGS33: none; masses.js readings {m.get('readings')}")
    # chants
    def ci(lst): return ', '.join(f"{x['id']}:{CH.get(str(x['id']),{}).get('i','?')}" for x in lst)
    out.append("  CHANTS: "+' | '.join(f"{p}={ci(v)}" for p,v in (m.get('parts') or {}).items()))
    for s,v in (m.get('season') or {}).items():
        out.append(f"   season {s}: "+' | '.join(f"{p}={ci(x)}" for p,x in v.items()))
    out.append(f"  NOTE: {m.get('note','')}")
if __name__=='__main__':
    keys=sys.argv[1:] or G
    out=[]
    for k in keys: run(k,out)
    print('\n'.join(out))
    json.dump(CROPS,open('/tmp/A4/crops.json','w'),ensure_ascii=False)
