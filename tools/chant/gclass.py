# Classify every chant glyph (by outline) into notational elements, in font units.
import json, sys
from ganalyze import comps, bb
STAFF={0,168,336,504}
def pos(y): return round((y-5)/84)          # 0 = bottom line (gabc d)
def classify(polys):
    if not polys: return {'t':'space'}
    staff=any(bb(p)[3]-bb(p)[1]<=12 and bb(p)[1] in STAFF for p in polys)
    cs,st,holes=comps(polys)
    big=[c for c in cs if c['x1']-c['x0']>350 or (c['y1']-c['y0']>400 and c['fill']<0.6)]
    if big: return {'t':'symbol','staff':staff}
    els=[]
    # clefs: two (or three) tall parts
    tall=[c for c in cs if c['y1']-c['y0']>=104 and c['x1']-c['x0']<=100 and c['fill']<0.93]
    if len(tall)>=2:
        tall.sort(key=lambda c:(c['x0'],c['y0']))
        right=[c for c in tall if c['x0']==max(t['x0'] for t in tall)]
        right.sort(key=lambda c:c['y0'])
        mid=(right[0]['y1']+right[-1]['y0'])/2
        line=round((mid-5)/168)+1
        kind='f' if len(cs)>=3 or len(tall)>=3 else 'c'
        return {'t':'clef','clef':f'{kind}{line}','staff':staff}
    small=[c for c in cs if c['y1']-c['y0']<56]
    if len(small)==2 and len(cs)==2 and st:
        y=(small[0]['y0']+small[0]['y1']+small[1]['y0']+small[1]['y1'])/4
        return {'t':'flat','p':pos(y),'x':(small[0]['x0']+small[0]['x1'])/2,'staff':staff}
    if not cs:
        if st:
            s=max(st,key=lambda s:s['y1']-s['y0']); h=s['y1']-s['y0']; w=max(x['x1'] for x in st)-min(x['x0'] for x in st) if 'x1' in s else 0
            if h>=480: return {'t':'bar','b':'::' if len(st)>1 or w>=100 else ':','staff':staff}
            if h>=300: return {'t':'bar','b':';','staff':staff}
            return {'t':'connector','staff':staff}
        return {'t':'space','staff':staff}
    for c in cs:
        w=c['x1']-c['x0']; h=c['y1']-c['y0']; cx=(c['x0']+c['x1'])/2
        if h>=400 and w<=110: els.append({'k':'bar','b':'::','x':cx}); continue
        if w>=140:
            els.append({'k':'n','p':pos(c['y1']-48),'x':c['x0']+44,'s':'obl'}); els.append({'k':'n','p':pos(c['y0']+48),'x':c['x1']-44,'s':'obl'}); continue
        if h<56:
            if c['y0']>600: els.append({'k':'acc','x':cx})
            continue
        cy=(c['y0']+c['y1'])/2
        if w<=62: s='small'
        elif w<=76 and c['fill']<0.82: s='rh'
        elif c['fill']<0.9 and not st: s='q'
        else: s='p'
        n={'k':'n','p':pos(cy),'x':cx,'s':s}
        if holes and s=='p': n['s']='hollow'
        for t in st:
            if t['x0']>=60 and t['y1']<=c['y0']+12 and s=='p': n['virga']=1
        els.append(n)
    if not els: return {'t':'space','staff':staff}
    if all(e['k']=='bar' for e in els): return {'t':'bar','b':'::','staff':staff}
    if all(e['k']=='acc' for e in els): return {'t':'acc','x':els[0]['x'],'staff':staff}
    return {'t':'notes','els':els,'staff':staff}
if __name__=='__main__':
    G=json.load(open('glyphs_all.json')); out={}
    for k,v in G.items():
        out[k]=classify(v['polys']); out[k]['ch']=v['ch']
    json.dump(out,open('gclass.json','w'))
    import collections
    print(collections.Counter(v['t'] for v in out.values()))
    for k,v in out.items():
        if k.startswith(sys.argv[1] if len(sys.argv)>1 else 'a1:TTE27BF2F8'):
            print(repr(v['ch']), {a:b for a,b in v.items() if a!='ch'})
