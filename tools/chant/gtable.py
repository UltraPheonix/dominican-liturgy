# Glyph semantics for Fr Thompson's Antiphonale (Meinrad-style chant fonts).
# Every glyph of every chant font in the five volumes is described by its outline; the meaning of each
# outline comes from the keyboard character it has in volumes 1-2, so volumes 3-4 (re-encoded fonts) are
# mapped by identical outlines.
import pymupdf, json, sys, hashlib, collections
from fontTools.ttLib import TTFont
BOOKS=['a1','a2a','a2b','a3','a4']
def contours(t, gname):
    gl=t['glyf']; g=gl[gname]
    if g.numberOfContours==0: return []
    coords,ends,flags=g.getCoordinates(gl); polys=[]; st=0
    for e in ends: polys.append([tuple(map(int,c)) for c in coords[st:e+1]]); st=e+1
    return polys
def sig(polys): return hashlib.md5(json.dumps(sorted(polys)).encode()).hexdigest()[:12]
glyphs={}   # "book:font:gid" -> {sig, ch, polys}
for b in BOOKS:
    d=pymupdf.open(f'/home/claude/dl/antiph/{b}.pdf'); fonts={}
    for pno,p in enumerate(d):
        for s in p.get_texttrace():
            fn=s['font']
            if fn.startswith('Times') or 'Times' in fn: continue
            if fn not in fonts:
                fonts[fn]=None
                for f in p.get_fonts(full=True):
                    if f[3].split('+')[-1]==fn and f[1]=='ttf':
                        name,ext,typ,buf=d.extract_font(f[0]); path=f'/tmp/{b}_{fn}.ttf'; open(path,'wb').write(buf)
                        try: fonts[fn]=TTFont(path)
                        except Exception as e: print('font fail',b,fn,e)
            t=fonts[fn]
            if t is None: continue
            order=t.getGlyphOrder()
            for c in s['chars']:
                k=f'{b}:{fn}:{c[1]}'
                if k in glyphs: glyphs[k]['n']+=1; continue
                try: polys=contours(t,order[c[1]])
                except Exception: polys=[]
                glyphs[k]={'sig':sig(polys),'ch':chr(c[0]),'polys':polys,'n':1}
    print(b,len(glyphs),file=sys.stderr)
json.dump(glyphs,open('glyphs_all.json','w'))
