"""Holy Week of the Missale O.P. 1939, as printed: OCR lines -> cleaned paragraphs per day -> site/data/holyweek1939.js"""
import json, re, sys
sys.path.insert(0,'/home/claude/build/m39hw')
import accent
DAYS=[('Quad6',137,1,r'DOMINICA IN RAMIS'),('Quad6m',146,1,r'FERIA SECUNDA'),('Quad6t',148,0,r'FERIA TERTIA'),('Quad6w',154,0,r'FERIA QUARTA'),
      ('Quad6h',160,1,r'FERIA QUINTA'),('Quad6f',166,0,r'FERIA SEXTA'),('Quad6s',179,1,r'^SABBATO$')]
END=(192,0)
LABEL=re.compile(r'^(Officium|Oratio|Secreta|Postcommunio|Lectio|Graduale|Responsorium|Tractus|Offertorium|Communio|Evangelium|Alleluia|Aña|Ana|Afia|Atia|Antiphona|Hymnus|Praefatio|Prophetia|Benedictio|Passio|Sequéntia|Oremus|Orémus|Flectamus|Psalmus|Ps\.)\b')
def clean(t):
    t=t.strip()
    t=re.sub(r'^(?:[|;,.:\'"()\-—_~!*]+\s*)+(?=\S)','',t)          # rule-line debris at the start
    t=re.sub(r'(?:\s+[|;,\'"()\-—_~!]{1,3})+\s*$','',t) if not t.endswith(('-',)) else re.sub(r'\s*[|]+\s*-$','-',t)
    t=re.sub(r'\s*\|\s*-?\s*$','',t)
    t=t.replace('»I*','✠').replace('»I«','✠').replace('»«','✠').replace('*I*','✠').replace('»%','✠').replace('»I','✠')
    t=re.sub(r'(?:(?<=\s)|^)(?:JX|X|IX|R)\.\s','℟. ',t)
    t=re.sub(r'(?:(?<=\s)|^)(?:X9|09|\?\?|9|Y|V)\.\s','℣. ',t)
    t=re.sub(r'^(Aña|Ana|Afia|Atia|Aiia|Aüa)\b','Aña',t)
    return t
def header(line, first):
    t=line['t']
    return first and (re.search(r'\b\d{2,3}\b',t) or len(t)<28)
out={}
lines=[]
for p in range(137,193):
    try: L=json.load(open('/home/claude/build/m39hw/p%d.json'%p))
    except: continue
    for c in (0,1):
        cl=[l for l in L if l['c']==c]
        for i,l in enumerate(cl):
            if i==0 and header(l,True): continue
            lines.append((p,c,l['red'],clean(l['t'])))
# drop caps: a lone capital starting the next line belongs to the first word of this line
i=0
while i+1<len(lines):
    p,c,r,t=lines[i]; p2,c2,r2,t2=lines[i+1]
    m=re.match(r'^([A-Z])\s+(\S.*)$',t2)
    if m and re.match(r'^[A-Z]{1,}[A-Z]*\b',t) and not re.match(r'^(Aña|IN|Ps)\b',t2):
        lines[i]=(p,c,r,m.group(1)+t if not t.startswith(m.group(1)) else t); lines[i+1]=(p2,c2,r2,m.group(2))
    i+=1
# split into days
idx={}
for k,(key,pg,col,rx) in enumerate(DAYS):
    for j,(p,c,r,t) in enumerate(lines):
        if p==pg and c==col and re.search(rx,t): idx[key]=j; break
order=[k for k,_,_,_ in DAYS]
for n,key in enumerate(order):
    a=idx[key]; b=idx[order[n+1]] if n+1<len(order) else len(lines)
    blocks=[]; cur=None
    for (p,c,r,t) in lines[a:b]:
        if not t: continue
        head=bool(re.search(r'[A-Z]{4,}',t) and sum(ch.isupper() for ch in t)>len(re.sub(r'\W','',t))*0.7 and len(t)<40)
        newpara = cur is None or head or cur.get('h') or bool(r)!=bool(cur.get('r')) or LABEL.match(t) or re.match(r'^(℣|℟|Aña|✠)',t)
        if cur and cur['t'].endswith('-'):
            cur['t']=cur['t'][:-1]+t; continue
        if newpara:
            cur={'t':t}
            if head: cur['h']=1
            elif r: cur['r']=1
            blocks.append(cur)
        else: cur['t']+=' '+t
    for bl in blocks:
        t=accent.fix(re.sub(r'\s+',' ',bl['t'])).strip()
        t=re.sub(r'^((?:Oratio|Lectio[^.]*?\.|Secreta|Postcommunio|Officium[^A-Z]*|Graduale[^A-Z]*|Tractus[^A-Z]*|Communio[^A-Z]*|Offertorium[^A-Z]*)\s+)(\S+)',lambda m:m.group(1)+accent.dropcap(m.group(2)),t)
        t=re.sub(r'(c\. \d+(?: ét \d+)?)\s*N illo', r'\1 IN illo', t).replace('. N illo',' IN illo')
        if not bl.get('h'): t=accent.dropcap(t.split(' ')[0])+t[len(t.split(' ')[0]):]
        bl['t']=t
    out[key]=blocks
json.dump(out,open('/home/claude/build/m39hw/hw39.json','w'),ensure_ascii=False,indent=0)
for k in order: print(k,len(out[k]),'blocks',sum(1 for b in out[k] if b.get('r')),'rubrics')
