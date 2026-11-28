# chk.py: compare a proposed text with the M39 text layer between two line numbers (folded words + punctuation)
import sys,difflib; sys.path.insert(0,'/tmp/A2')
from lib import MT,MF,ML,fold,toks
def chk(new,lo,hi,label=''):
    idx=[i for i,l in enumerate(ML) if lo<=l<=hi]
    mt=[MT[i] for i in idx]; mf=[MF[i] for i in idx]; ln=[ML[i] for i in idx]
    st=toks(new); sf=[fold(w) for w in st]
    sm=difflib.SequenceMatcher(None,sf,mf,autojunk=False)
    bl=[b for b in sm.get_matching_blocks() if b.size]
    a=bl[0].b; b=bl[-1].b+bl[-1].size
    sm=difflib.SequenceMatcher(None,sf,mf[a:b],autojunk=False)
    print('==',label,'ratio %.3f'%sm.ratio())
    for op,i1,i2,j1,j2 in sm.get_opcodes():
        if op!='equal':
            ctx=' '.join(st[max(0,i1-3):i1])
            print('  %-7s ...%s [%s] -> layer [%s] (line %s)'%(op,ctx,' '.join(st[i1:i2]),' '.join(mt[a+j1:a+j2]),ln[min(a+j1,len(ln)-1)]))
