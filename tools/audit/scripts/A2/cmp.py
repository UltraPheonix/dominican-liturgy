import sys; sys.path.insert(0,'/tmp/A2')
from lib import *
O=load('data/orations.js'); R=load('data/readings33.js'); D=load('data/masses.js'); M=D['masses']
G=json.load(open(ROOT+'/tools/audit/groups.json'))['A2']
def cands(sw):
    ws=[fold(w) for w in sw if w[0].isalpha()]
    for a,b in [(0,4),(1,5),(2,6),(0,3),(3,7),(5,9)]:
        c=findw(ws[a:b])
        if c:
            # back off to start: approximate
            return [max(0,x-(a*2)) for x in c], a
    return [],0
def align(site, s, extra=60):
    sf=[fold(w) for w in site]
    win=MT[s:s+len(site)+extra]; wf=MF[s:s+len(site)+extra]
    sm=difflib.SequenceMatcher(None,sf,wf,autojunk=False)
    bl=[b for b in sm.get_matching_blocks() if b.size]
    # trim: missal end = end of last block
    end=bl[-1].b+bl[-1].size if bl else 0
    # start: first block
    st=bl[0].b if bl else 0
    sm=difflib.SequenceMatcher(None,sf,wf[st:end],autojunk=False)
    diffs=[]
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal':
            diffs.append((op,' '.join(site[max(0,i1-2):i2+2]),' '.join(site[i1:i2]),' '.join(win[st+j1:st+j2])))
    # exact-case/spelling diffs within equal blocks ignored (folded)
    return diffs, s+st, s+end, sm.ratio()
def run(keys, out=sys.stdout, showtail=12):
    for k in keys:
        items=[]
        o=O.get(k,{})
        for f in ['or','se','pc','sp']:
            if f in o and isinstance(o[f],list): items.append((('orations',k,f),o[f][0]))
        for n,r in enumerate(R.get(k,[])):
            items.append((('readings',k,n,r['type'],r['ref']),r['la']))
        cs=[]
        for key,txt in items:
            t=toks(txt); c,a=cands(t); cs.append((key,t,c))
        allp=[MP[x] for _,_,c in cs for x in c]
        if not allp: print('##',k,'NOT FOUND',file=out); continue
        best=min(range(30,460),key=lambda p:sum(min([abs(MP[x]-p) for x in c] or [0]) for _,_,c in cs))
        print('\n########',k,M.get(k,{}).get('title'),'anchor @@PAGE',best,file=out)
        for key,t,c in cs:
            if not c: print('  --',key,'NOT LOCATED',file=out); continue
            s=min(c,key=lambda x:abs(MP[x]-best))
            d,a,b,r=align(t,max(0,s-3))
            print('  ==',key,'@@PAGE %d-%d line %d ratio %.3f'%(MP[a],MP[b-1],ML[a],r),file=out)
            print('     before:',' '.join(MT[a-12:a]),file=out)
            for x in d: print('     %-7s site[%s] missal[%s]   ctx: %s'%(x[0],x[2],x[3],x[1]),file=out)
            print('     after :',' '.join(MT[b:b+showtail]),file=out)
if __name__=='__main__':
    run(sys.argv[1:] or G)
