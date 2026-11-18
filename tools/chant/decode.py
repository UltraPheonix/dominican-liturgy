# Decode Fr Thompson's Antiphonale (PDF typeset with chant fonts) into a reading-order list of items:
#   {'k':'text', 'half', 'y', 'x', 'text', 'font'}  and  {'k':'sys', 'half', 'y', 'els':[...], 'lyr':[chars], 'lab': mode label}
import pymupdf, json, sys, re, collections
GC=json.load(open('gclass.json'))
LETTERS='abcdefghijklm'
def decode_book(book, pages=None):
    d=pymupdf.open(f'/home/claude/dl/antiph/{book}.pdf'); out=[]
    for pno in (pages or range(len(d))):
        p=d[pno]; M=p.rotation_matrix; mid=p.rect.width/2
        chant=collections.defaultdict(list); texts=[]
        for s in p.get_texttrace():
            fn=s['font']; size=s['size']
            for c in s['chars']:
                o=pymupdf.Point(c[2])*M
                k=f'{book}:{fn}:{c[1]}'
                g=GC.get(k)
                if g and g['t']!='symbol' and (g.get('staff') or g['t'] in ('notes','clef','flat','bar','connector','acc')) and size>30:
                    half=0 if o.x<mid else 1
                    chant[(half,round(o.y,0))].append((o.x,size,g))
                else:
                    bb=pymupdf.Rect(c[3])*M
                    texts.append({'x':bb.x0,'x1':bb.x1,'y':o.y,'c':chr(c[0]) if not (g and g['t']=='symbol') else {'+':'℟','=':'℣','„':'✠'}.get(g['ch'],'℣') ,'font':fn,'size':size,'half':0 if bb.x0<mid else 1})
        # merge chant rows whose baselines differ by <=2
        rows={}
        for (h,y),v in sorted(chant.items()):
            key=next((k for k in rows if k[0]==h and abs(k[1]-y)<=2),None)
            if key: rows[key]+=v
            else: rows[(h,y)]=list(v)
        systems=[]
        for (h,y),v in rows.items():
            els=[]
            for x,size,g in sorted(v,key=lambda t:t[0]):
                sc=size/1000
                if g['t']=='notes':
                    for e in g['els']:
                        if e['k']=='n': els.append({'k':'n','x':x+e['x']*sc,'p':e['p'],'s':e['s'],'v':e.get('virga',0)})
                        elif e['k']=='bar': els.append({'k':'bar','x':x+e['x']*sc,'b':e['b']})
                        elif e['k']=='acc': els.append({'k':'acc','x':x+e['x']*sc})
                elif g['t']=='clef': els.append({'k':'clef','x':x,'c':g['clef']})
                elif g['t']=='flat': els.append({'k':'flat','x':x+g['x']*sc,'p':g['p']})
                elif g['t']=='bar': els.append({'k':'bar','x':x+0.05*size,'b':g['b']})
                elif g['t']=='acc': els.append({'k':'acc','x':x+g['x']*sc})
            if not any(e['k']=='n' for e in els): continue
            systems.append({'half':h,'y':y,'size':v[0][1],'els':els,'x0':min(t[0] for t in v),'x1':max(t[0] for t in v)})
        # text lines
        lines=collections.defaultdict(list)
        for t in texts:
            key=next((k for k in lines if k[0]==t['half'] and abs(k[1]-t['y'])<=1.5),None) or (t['half'],round(t['y'],1))
            lines[key].append(t)
        tl=[]
        for (h,y),cs in lines.items():
            cs.sort(key=lambda t:t['x'])
            tl.append({'half':h,'y':y,'chars':cs})
        used=set()
        for s in systems:
            staff_h=0.514*s['size']
            # lyrics: the nearest text line below the staff baseline
            cand=[l for l in tl if l['half']==s['half'] and 0<l['y']-s['y']<staff_h*1.1]
            cand=[l for l in cand if any(s['x0']-5<=c['x']<=s['x1']+30 and c['c'].isalpha() for c in l['chars'])]
            if cand:
                l=min(cand,key=lambda l:l['y']); s['lyr']=[c for c in l['chars'] if c['x']>=s['x0']-8]; used.add(id(l))
                rest=[c for c in l['chars'] if c['x']<s['x0']-8]
            else: s['lyr']=[]
            # mode label: text left of the staff within its height
            lab=[c for l in tl if l['half']==s['half'] and s['y']-staff_h-4<l['y']<s['y']+6 for c in l['chars'] if c['x1']<=s['x0']+2]
            for l in tl:
                if l['half']==s['half'] and s['y']-staff_h-4<l['y']<s['y']+6 and all(c['x1']<=s['x0']+2 for c in l['chars']): used.add(id(l))
            s['lab']=''.join(c['c'] for c in sorted(lab,key=lambda c:c['x'])).strip()
        items=[]
        for l in tl:
            if id(l) in used: continue
            txt=''; last=None
            for c in l['chars']:
                if last is not None and c['x']-last>1.5 and not txt.endswith(' '): txt+=' '
                txt+=c['c']; last=c['x1']
            txt=re.sub(r'\s+',' ',txt).strip()
            if txt: items.append({'k':'text','half':l['half'],'y':l['y'],'x':l['chars'][0]['x'],'text':txt,'bold':'Bold' in l['chars'][0]['font'],'ital':'Italic' in l['chars'][0]['font'],'page':pno})
        for s in systems: s['k']='sys'; s['page']=pno; items.append(s)
        items.sort(key=lambda i:(i['half'],i['y']))
        out+=items
    return out
if __name__=='__main__':
    book=sys.argv[1]; rng=sys.argv[2] if len(sys.argv)>2 else None
    pages=range(*map(int,rng.split('-'))) if rng else None
    items=decode_book(book,pages)
    json.dump(items,open(f'items_{book}.json','w'),ensure_ascii=False)
    for it in items[:60]:
        if it['k']=='text': print('T',it['page'],it['half'],round(it['y']),it['text'][:90])
        else: print('S',it['page'],it['half'],round(it['y']),it['lab'],''.join(e.get('c','') or (LETTERS[e['p']+3] if e['k']=='n' and 0<=e['p']+3<13 else e.get('b','') if e['k']=='bar' else '.') for e in it['els']),'|',''.join(c['c'] for c in it['lyr'])[:80])
