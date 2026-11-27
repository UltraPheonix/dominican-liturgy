import sys; sys.path.insert(0,'/tmp/A2')
from lib import *
O=load('data/orations.js'); R=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A2']
# printed page map
pp={}; cur=None
for l in lines:
    if l.startswith('@@PAGE'): cur=int(l.split()[1]); pp.setdefault(cur,[]); continue
    m=re.match(r'^ *(\d{1,3}) *$',l) or re.match(r'^\[?(\d{1,3})\]? [A-Z]',l)
    if m and cur is not None: pp[cur].append(int(m.group(1)))
def printed(n):
    v=pp.get(n) or []
    return v[0] if v else None
HEAD=re.compile(r'^(DOMINICA|FERIA [A-Z]|SABBAT|IN [A-Z]{3,}|AD MISSAM|MISSA)')
heads=[ln for ln,l in enumerate(lines,1) if HEAD.match(l)]
SEC=re.compile(r'^\s*(Officium|Oratio|Alia Oratio|Secreta|Postcommunio|Super populum|Oratio super populum|Humiliate.*|Lectio.*|Sequentia sancti.*|Initium sancti.*|Passio.*|Graduale|Offertorium|Communio|Alleluia|Tractus|Sequentia|Graduale.*|Communio.*|Offertorium.*|Officium.*|Tractus.*|Prophetia.*)\s*$')
CONC=re.compile(r'(Per (?:D[óo]minum|e[úu][nm]dem|eúmdem)|Qui (?:vivis|tecum|vivit))(?!.*(Per (?:D[óo]minum|e[úu][nm]dem)|Qui (?:vivis|tecum|vivit)))',re.S)
def cands(sw):
    ws=[fold(w) for w in sw if w[0].isalpha()]
    out=set()
    for a,b in [(0,4),(1,5),(2,6),(3,7),(5,9),(8,12),(10,14)]:
        if b<=len(ws):
            for x in findw(ws[a:b]):
                # back up a words
                y=x; n=0
                while n<a and y>0:
                    y-=1
                    if MF[y][0].isalpha(): n+=1
                out.add(y)
    return sorted(out)
def score(t,s):
    sf=[fold(w) for w in t[:40] if w[0].isalpha()]
    wf=[w for w in MF[max(0,s-5):s+80] if w[0].isalpha()][:len(sf)+10]
    return difflib.SequenceMatcher(None,sf,wf,autojunk=False).ratio()
def align(site, s, extra=None):
    extra=extra or 40+len(site)//6
    sf=[fold(w) for w in site]
    W=len(site)+extra
    win=MT[s:s+W]; wf=MF[s:s+W]
    sm=difflib.SequenceMatcher(None,sf,wf,autojunk=False)
    bl=[b for b in sm.get_matching_blocks() if b.size]
    end=bl[-1].b+bl[-1].size if bl else 0
    st=bl[0].b if bl else 0
    # include trailing punctuation in missal
    if st+0<end and end<len(wf) and not wf[end][0].isalpha() and (not sf or sf[-1][0].isalpha()): end+=1
    sm=difflib.SequenceMatcher(None,sf,wf[st:end],autojunk=False)
    diffs=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal':
            diffs.append((op,' '.join(site[max(0,i1-3):i2+3]),' '.join(site[i1:i2]),' '.join(win[st+j1:st+j2]),i1))
    return diffs, s+st, s+end, sm.ratio()
def run(keys, out=sys.stdout, tail=14):
    for k in keys:
        items=[]
        o=O.get(k,{})
        for f in ['or','se','pc','sp']:
            if f in o and isinstance(o[f],list): items.append(('or.'+f,o[f][0]))
        for n,r in enumerate(R.get(k,[])):
            items.append(('rd.%d %s %s'%(n,r['type'],r['ref']),r['la']))
        cs=[]
        for key,txt in items:
            conc=''
            if key.startswith('or'):
                m=CONC.search(txt)
                if m: conc=txt[m.start():]; txt=txt[:m.start()]
            t=toks(txt); cs.append((key,t,cands(t),conc))
        allc=[x for _,_,c,_ in cs for x in c]
        print('\n########',k,'|',M.get(k,{}).get('title'),file=out)
        if not allc: print('  NOT FOUND',file=out); continue
        best=min(range(30,460),key=lambda p:sum(min([abs(MP[x]-p) for x in c] or [0]) for _,_,c,_ in cs))
        # segment: heading before the earliest chosen item
        chosen=[]
        for key,t,c,conc in cs:
            near=[x for x in c if abs(MP[x]-best)<=8]
            s=max(near,key=lambda x:(round(score(t,x),2),-abs(MP[x]-best))) if near else (min(c,key=lambda x:abs(MP[x]-best)) if c else None)
            chosen.append(s)
        first=chosen[0] if chosen and chosen[0] is not None else min(x for x in chosen if x is not None)
        l0=max([h for h in heads if h<=ML[first]] or [1])
        l1=min([h for h in heads if h>ML[first]+5] or [len(lines)])
        print('  segment lines %d-%d  @@PAGE %d (printed %s) .. '%(l0,l1,MP[first],printed(MP[first])),file=out)
        print('  title:',' / '.join(x.strip() for x in lines[l0-1:l0+3]),file=out)
        secs=[(ln,lines[ln-1].strip()) for ln in range(l0,l1) if SEC.match(lines[ln-1])]
        print('  sections:',', '.join('%s@%d'%(s,ln) for ln,s in secs),file=out)
        for (key,t,c,conc),s in zip(cs,chosen):
            if s is None: print('  --',key,'NOT LOCATED',file=out); continue
            d,a,b,r=align(t,max(0,s-4))
            flag='' if l0<=ML[a]<l1 else '  !!! OUTSIDE SEGMENT'
            print('  ==',key,'@@PAGE %d-%d (p.%s) line %d ratio %.3f%s'%(MP[a],MP[b-1],printed(MP[a]),ML[a],r,flag),file=out)
            print('     before:',' '.join(MT[a-10:a]),file=out)
            if r<0.6: print('     !!! LOW RATIO, %d diffs, skipped'%len(d),file=out); d=[]
            for x in d: print('     %-7s site[%s] missal[%s]   ctx: %s'%(x[0],x[2],x[3],x[1]),file=out)
            print('     after :',' '.join(MT[b:b+tail]),file=out)
            if conc: print('     site concl:',conc[:40],file=out)
if __name__=='__main__':
    run(sys.argv[1:] or G)
