import fitz, re, json, sys, statistics, difflib, warnings
warnings.filterwarnings('ignore')
PDF='/tmp/en_sources/dl/musicasacra/dm.pdf'
doc=fitz.open(PDF)
def rows_of(page):
    d=page.get_text('dict'); objs=[]
    for b in d['blocks']:
        if b['type']!=0: continue
        for l in b['lines']:
            sp=l['spans']; txt=''.join(s['text'] for s in sp)
            if not re.search(r'[A-Za-z]', txt): continue
            it=sum(len(s['text']) for s in sp if 'Italic' in s['font'] or 'Oblique' in s['font'])
            objs.append({'y':l['bbox'][1],'y1':l['bbox'][3],'x':l['bbox'][0],'x1':l['bbox'][2],'t':txt,'it':it/max(1,len(txt))})
    objs.sort(key=lambda o:(o['y'],o['x']))
    rows=[]
    for o in objs:
        if rows and abs(rows[-1][0]['y']-o['y'])<4: rows[-1].append(o)
        else: rows.append([o])
    for r in rows: r.sort(key=lambda o:o['x'])
    return rows
for pno in map(int,sys.argv[1:]):
    rows=rows_of(doc[pno])
    ys=[r[0]['y'] for r in rows]
    for i,r in enumerate(rows):
        print(round(r[0]['y']), round(ys[i+1]-ys[i],1) if i+1<len(rows) else '-', ' | '.join(f"{round(o['x'])}{'I' if o['it']>.5 else ''}:{o['t']}" for o in r)[:110])
