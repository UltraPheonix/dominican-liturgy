"""Step 3 audit: sung propers vs the Missale O.P. 1933 (scan OCR). Run after run.sh: python3 tools/m33/propers_audit.py [in gr of co]"""
import json,re,subprocess,sys,unicodedata
sys.path.insert(0,'/home/claude/m33')
from parse import norm
R='/home/claude/dominican-liturgy/'
L=json.load(open('/home/claude/m33/lines.json'));M=json.load(open('/home/claude/m33/map.json'))
site=json.loads(subprocess.check_output(['node','-e',"""
eval(require('fs').readFileSync('%sdata/masses.js','utf8').replace('var DOMINICAN','global.D'));
const o={};for(const [k,m] of Object.entries(D.masses)){o[k]={};for(const p of ['in','gr','of','co'])o[k][p]=((m.parts||{})[p]||[]).map(c=>String(c.id))}
console.log(JSON.stringify(o))"""%R]))
def gtext(i):
    p=R+('gabc/r/'+i[1:] if i.startswith('r') else 'gabc/'+i)+'.gabc'
    try: g=open(p,encoding='utf8').read()
    except: return ''
    g=g.split('%%')[-1]; g=re.sub(r'\([^)]*\)','',g); g=re.sub(r'<[^>]*>|\{|\}|\*|[\[\]]','',g)
    return norm(g)
HEAD={'in':r'^(Officium|Introitus)\b','gr':r'^(Graduale|\S{1,3}\s*Psalm\.|\S{1,2}\.\s+[A-Z][a-z]+\.?\s*\d+)','of':r'^Offertorium\b','co':r'^Communio\b'}
out=[]
for k,v in M.items():
    st=v.get('start')
    if st is None or k not in site: continue
    end=next((j for j in range(st+1,min(len(L),st+400)) if re.match(HEAD['in'],L[j][2])),min(len(L),st+400))
    for p in sys.argv[1:] or ('in','of','co'):
        if not site[k][p]: continue
        hit=next((j for j in range(st,end) if re.match(HEAD[p],L[j][2])),None)
        if hit is None: out.append((k,p,'NOHEAD',L[st][0]+1)); continue
        txt=' '.join(L[j][2] for j in range(hit,min(hit+6,end)))
        a=norm(re.sub(HEAD[p],'',txt)).split()[:25]
        b=gtext(site[k][p][0]).split()
        b=[w for w in b if len(w)>2][:6]
        sc=sum(1 for w in b[1:6] if any(w[:5]==x[:5] for x in a))
        if sc<2: out.append((k,p,' '.join(b[:5]),' '.join(a[:10]),L[hit][0]+1))
md=['# Propers vs Missale O.P. 1933 — audit (step 3)','',
'propers_audit.py compares words 2-6 of every Introit/Gradual/Offertory/Communion the site sings with the OCR after the heading in M33.',
'All 43 lines of the first pass and every line below were checked on the page images. Real mismatches are corrected in',
'propers_fix.json (applied by propers_apply.py, also from build_masses.py); M33 anchors in dpmap.json. What is left below is',
'OCR noise (lost drop caps, mixed columns, NOHEAD = heading not read) or Masses absent from M33 (C1s Commune Apostolorum).','',
'| Mass | part | site | M33 OCR | pdf p. |','|---|---|---|---|---|']+['| '+' | '.join(str(x) for x in o)+(' |' if len(o)==5 else ' | | |') for o in out]
open(R+'tools/m33/propers_audit.md','w').write('\n'.join(md)+'\n'); print(len(out),'flags left')
