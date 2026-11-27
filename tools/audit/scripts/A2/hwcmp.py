# compare current proposals (fixes_raw new, else data) with HW_TEXT 1939 blocks
import json,re,sys,difflib
sys.path.insert(0,'/tmp/A2')
from lib import load
s=open('/home/claude/dominican-liturgy/data/holyweek_text.js',encoding='utf8').read()
HT=json.loads(s[s.index('=')+1:].rstrip().rstrip(';'))['1939']
F={f['k']:f for f in json.load(open('/tmp/A2/fixes_raw.json'))}
O=load('data/orations.js'); R=load('data/readings33.js')
def norm(t):
    t=re.sub(r'\{[^}]*\}','',t); t=t.replace('^','').replace('*','')
    t=re.sub(r'\s+([:;?!])',r'\1',t); t=t.replace('j','i').replace('J','I')
    return t
def alltext(blocks):
    out=[]
    for b in blocks:
        if b.get('t')=='F': out+=alltext(b['blocks'])
        elif b.get('la'): out.append(norm(b['la']))
    return out
k=sys.argv[1]
H=' '.join(alltext([b for sec in HT[k] for b in sec['blocks']]))
items=[]
for f in ['or','se','pc','sp']:
    if f in O.get(k,{}): items.append(('%s|%s.%s.0'%(k,k,f),O[k][f][0]))
for n,r in enumerate(R.get(k,[])): items.append(('%s|%s.%d.la'%(k,k,n),r['la']))
for key,cur in items:
    t=F[key]['new'] if key in F else cur
    t=re.sub(r'(Per (D|e)|Qui (tecum|vivis)).*$','',t).strip() if '.%s.'%'' or True else t
    tn=norm(t)
    w=tn.split()
    # locate in H by first 4 words
    hw=H.split(); st=None
    for i in range(len(hw)):
        if hw[i:i+3]==w[:3]: st=i; break
    if st is None:
        for i in range(len(hw)):
            if hw[i:i+3]==w[3:6]: st=max(0,i-3); break
    if st is None: print('##',key,'NOT FOUND in HW'); continue
    seg=hw[st:st+len(w)+5]
    sm=difflib.SequenceMatcher(None,w,seg,autojunk=False)
    print('##',key)
    for op,a,b,c,d in sm.get_opcodes():
        if op!='equal' and not (op=='insert' and b==len(w)): print('   ',op,' '.join(w[max(0,a-2):b+1]),' ||| ',' '.join(seg[max(0,c-2):d+1]))
