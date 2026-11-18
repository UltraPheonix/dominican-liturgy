# Thompson's decoded pieces -> supplement.json (antiphons, short responsories, hymns) for build_chant.py
import json, re, glob, collections
ROM={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8}
out={}; n=collections.Counter()
for f in sorted(glob.glob('/home/claude/build/chant/pieces_*.json')):
    book=f.split('_')[-1][:-5]
    for i,p in enumerate(json.load(open(f))):
        ctx=' '.join(p['ctx'][-3:]); g=p['gabc']
        part=None
        if re.search(r'RESPONSORIUM BREVE',ctx,re.I): part='rb'
        elif re.search(r'HYMNUS',ctx): part='hy'
        elif re.search(r'\bAnt\b',ctx) or p['lab']: part='an'
        if not part: continue
        # the antiphon alone: up to the psalm intonation or the Euouae
        if part=='an':
            g=re.split(r"<i>(?:Ps\.|C\.)</i>|\s(?=E\(\w*\)\s*u\(\w*\)\s*o\()",g)[0].strip()
            g=re.sub(r"'",'',g)
            if not g.endswith('(::)'): g=g.rstrip()+' (::)'
        m=re.match(r'([IV]+)',p['lab'] or '')
        mode=str(ROM.get(m.group(1),'')) if m else ''
        text=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',re.sub(r'\([^)]*\)','',g))).strip()
        if len(text.split())<2: continue
        cid=f'T{book}-{i}'
        out[cid]={'inc':text[:40],'part':part,'mode':mode,'mvar':None,'ver':'Thompson','comm':None,'src':[['THOMPSON-'+book,str(p['page'])]],'gabc':g,'text':text}
        n[part]+=1
json.dump(out,open('supplement.json','w'),ensure_ascii=False)
print(n)
