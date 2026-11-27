import sys; sys.path.insert(0,'/tmp/A2')
from prop import *
CONCW=re.compile(r'\s*(Per (?:D[óo]minum|e[úu][nm]dem)|Qui (?:vivis|tecum|vivit))\b.*$',re.S)
props=json.load(open('/tmp/A2/props.json')) if os.path.exists('/tmp/A2/props.json') else {}
def run(keys,out=sys.stdout):
    for k in keys:
        items=[]
        o=O.get(k,{})
        for f in ['or','se','pc','sp']:
            if f in o and isinstance(o[f],list): items.append((('data/orations.js',[k,f,0]),o[f][0]))
        for n,r in enumerate(R.get(k,[])):
            items.append((('data/readings33.js',[k,n,'la']),r['la']))
        print('\n########',k,'|',M.get(k,{}).get('title'),file=out)
        # collect first
        chosen=[]; seg=None; best=None
        for (fn,path),txt in items:
            conc=''
            if fn.endswith('orations.js'):
                m=CONC.search(txt)
                if m: conc=txt[m.start():]; pre=txt[:m.start()]
                else: pre=txt
            else: pre=txt
            t=toks(pre); c=cands(t)
            if not c: print('  --',path,'NOT LOCATED',file=out); continue
            if best is None:
                # choose by global best match within temporale/supp
                s=max(c,key=lambda x:score(t,x))
                best=MP[s]
                l0=max([h for h in heads if h<=ML[s]] or [1]); l1=min([h for h in heads if h>ML[s]+5] or [len(lines)])
                seg=(l0,l1)
                print('  segment lines %d-%d, @@PAGE %d (pdf %d, printed %s): %s'%(l0,l1,MP[s],MP[s]+1,printed(MP[s]),' / '.join(x.strip() for x in lines[l0-1:l0+3])),file=out)
                secs=[(ln,lines[ln-1].strip()) for ln in range(l0,l1) if SEC.match(lines[ln-1])]
                print('  sections:',', '.join('%s@%d'%(s_,ln) for ln,s_ in secs),file=out)
            else:
                ins=[x for x in c if seg[0]<=ML[x]<seg[1]]
                near=ins or [x for x in c if abs(MP[x]-best)<=8] or c
                s=max(near,key=lambda x:(round(score(t,x),2),-abs(MP[x]-best)))
            new,notes,a,b,r=propose(pre,max(0,s-4))
            mconc=''
            if conc:
                mm=CONCW.search(new)
                if mm: mconc=mm.group(1); new=new[:mm.start()]
                newfull=new.rstrip()+' '+conc
            else: newfull=new
            if fn.endswith('readings33.js'): newfull=new
            flag='' if seg[0]<=ML[a]<seg[1] else ' (outside segment)'
            print('  ==',path,'@@PAGE %d-%d (pdf %d, p.%s) line %d ratio %.3f%s'%(MP[a],MP[b-1],MP[a]+1,printed(MP[a]),ML[a],r,flag),file=out)
            print('     before:',' '.join(MT[a-10:a]),file=out)
            if r<0.6: print('     !!! LOW RATIO — manual',file=out); continue
            for n_ in notes:
                if n_[0]=='WORD' and n_[2].strip().endswith('=> : Per Dóminum') : continue
                print('     %-6s %s  ||  %s'%n_,file=out)
            if conc: print('     concl: site[%s] missal[%s]'%(conc[:22],mconc or ' '.join(MT[b:b+3])),file=out)
            else: print('     after :',' '.join(MT[b:b+14]),file=out)
            key=k+'|'+'.'.join(map(str,path))
            props[key]={'file':fn,'path':path,'old':txt,'new':newfull,'pages':[MP[a]+1,MP[b-1]+1]}
    json.dump(props,open('/tmp/A2/props.json','w'),ensure_ascii=False,indent=0)
if __name__=='__main__':
    run(sys.argv[1:] or G)
