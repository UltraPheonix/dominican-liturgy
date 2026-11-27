import json,sys
sys.path.insert(0,'/tmp/A4')
from align import *
from pmap import *
from load import *
import audit as A   # reuses keep()
PUN=set(',;:.?!')
def target(k,field):
    if field in ('or','se','pc'):
        return 'data/orations.js',[k,field,0],A.O[k][field][0]
    i=int(field[1:]) if field[0]=='r' else None
    return 'data/readings33.js',[k,i,'la'],A.RD[k][i]['la']
def win_for(k):
    o=A.O.get(k,{}); m=A.M.get(k,{})
    pg=pages_from(o.get('src','')) or pages_from('p. '+str(m.get('page','')))
    if pg and pg[0] in P2L:
        l0=P2L[pg[0]]; l1=P2L.get(pg[1],l0); return (l0-30,l1+420)
    return None
def kept(k,field):
    fn,path,s=target(k,field); win=win_for(k)
    body=s
    if field in ('or','se','pc'):
        mm=CONCL.search(s); body=s[:mm.start()] if mm else s
    if field[0]=='r' and k in A.RWIN: l0=P2L[A.RWIN[k]]; win=(l0-200,l0+600)
    r=compare(body,win[0] if win else None,win=win)
    if r and r['score']<0.3 and field[0]=='r': r=compare(body,win[0] if win else None)
    return s,body,r,[d for d in r['diffs'] if A.keep(d)]
def make(k,field,accept,manual=None,src='',why=''):
    """accept: list of kept-diff indices (punctuation-only); manual: {idx: replacement text for the site token span} or list of (old,new) substrings"""
    fn,path,s=target(k,field)
    s0,body,r,ds=kept(k,field)
    sp=r['spos']; edits=[]
    for n in accept:
        t,a,b,c,ln,j1,j2,i1,i2=ds[n]
        mp=[MS[j][1] for j in range(j1,j2)]
        if manual and isinstance(manual,dict) and n in manual:
            rep=manual[n]
            if i2>i1: edits.append((sp[i1][0],sp[i2-1][1],rep))
            else: edits.append((sp[i1-1][1],sp[i1-1][1],rep))
            continue
        if t=='case':
            st0=sp[i1][0]; ch=s[st0]; edits.append((st0,st0+1,ch.upper() if b[0].isupper() else ch.lower())); continue
        assert all(x in PUN for x in mp) and all(x in PUN for x in a.split()), (k,field,n,a,b)
        newp=''.join(mp)
        if t=='insert':
            e=sp[i1-1][1]; edits.append((e,e,newp))
        elif t=='delete':
            st,en=sp[i1][0],sp[i2-1][1]
            # remove punctuation; if it was followed by space keep one space
            edits.append((st,en,''))
        else:
            edits.append((sp[i1][0],sp[i2-1][1],newp))
    new=s
    for st,en,rep in sorted(edits,reverse=True): new=new[:st]+rep+new[en:]
    if manual and isinstance(manual,list):
        for o,nw in manual:
            assert new.count(o)==1,(k,field,o,new.count(o)); new=new.replace(o,nw)
    new=new.replace('  ',' ')
    return {"file":fn,"path":path,"old":s,"new":new,"src":src,"why":why}
