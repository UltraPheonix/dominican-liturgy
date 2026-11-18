# Draw every glyph of the chant fonts used in a book, labelled by its keyboard character.
import sys, pymupdf, collections
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from PIL import Image, ImageDraw
book=sys.argv[1]; out=sys.argv[2]
d=pymupdf.open(book)
fonts={}; use=collections.Counter()
for p in d:
    for s in p.get_texttrace():
        if 'TTE' not in s['font']: continue
        fn=s['font']
        if fn not in fonts:
            # find xref
            for f in p.get_fonts(full=True):
                if f[3].endswith(fn): fonts[fn]={'xref':f[0],'g':{}}
        for c in s['chars']: fonts[fn]['g'][c[1]]=chr(c[0]); use[(fn,c[1])]+=1
def contours(t, gname):
    gl=t['glyf']; g=gl[gname]
    if g.numberOfContours==0: return []
    coords,ends,flags=g.getCoordinates(gl)
    polys=[]; st=0
    for e in ends:
        polys.append([tuple(map(int,c)) for c in coords[st:e+1]]); st=e+1
    return polys
import json
info={}
for fn,f in fonts.items():
    name,ext,typ,buf=d.extract_font(f['xref']); path=f'{fn}.ttf'; open(path,'wb').write(buf)
    t=TTFont(path); order=t.getGlyphOrder()
    items=sorted(f['g'].items(), key=lambda x:x[1])
    cols=12; W,H=150,300; img=Image.new('L',(cols*W,((len(items)+cols-1)//cols)*H),255); dr=ImageDraw.Draw(img)
    for i,(gid,ch) in enumerate(items):
        ox,oy=(i%cols)*W+40,(i//cols)*H+220
        polys=contours(t,order[gid])
        for poly in polys:
            if len(poly)>2: dr.polygon([(ox+x*0.12,oy-y*0.12) for x,y in poly],fill=0)
        dr.line([(ox-30,oy),(ox+100,oy)],fill=180)
        dr.text(((i%cols)*W+5,(i//cols)*H+5),f'{ch!r} {ord(ch)} n={use[(fn,gid)]}',fill=0)
        info[f'{fn}:{gid}']={'ch':ch,'polys':polys}
    img.save(f'{out}_{fn}.png'); print(fn,len(items))
json.dump(info,open(out+'_glyphs.json','w'))
