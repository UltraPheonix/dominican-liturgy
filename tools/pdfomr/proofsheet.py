"""proof sheets: each staff of a piece, with the notes the OMR gave each syllable boxed (alternating colours) and the syllable above"""
import sys, pickle, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0]] + sys.argv[1:]
from PIL import Image, ImageDraw, ImageFont
from m39app import main
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'm39pref.py')).read().split('# ---------------------------------------------------------------- the right text')[0]
__file__ = 'm39pref.py'; exec(src.split("pieces = []; cur = None")[0])
P = pickle.load(open('/tmp/m39pieces.pkl', 'rb'))
want = sys.argv[1]
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
cache = {}
for p in P:
    if want not in p['title']: continue
    rows = []
    for x in p['staves']:
        key = (x['page'], x['side'])
        if key not in cache: cache[key] = main('/home/claude/dl_m39/M39.pdf', *key)[1]
        g = cache[key]; L = x['L']; s = x['s']
        toks, items, s = staff_syllables(x)
        res = assign(toks, items, s)
        im = Image.fromarray(g.astype('uint8')).convert('RGB'); dr = ImageDraw.Draw(im)
        y0 = int(L[0] - 2.6 * s); y1 = int(L[3] + 2.4 * s)
        for i, (sy, ns, bar) in enumerate(res):
            col = (220, 0, 0) if i % 2 == 0 else (0, 90, 255)
            for nx, pos in ns:
                yy = L[3] - pos * s / 2
                dr.rectangle([nx - 3, yy - 13, nx + 26, yy + 13], outline=col, width=4)
            if ns: dr.text((min(n[0] for n in ns), y0 + 4), sy + (' ' + bar if bar else ''), fill=col, font=font)
        rows.append(im.crop((x['x'][0] - 40, y0, x['x'][1] + 60, y1)))
    W = max(r.width for r in rows); half = (len(rows) + 1) // 2
    for part, rr in enumerate((rows[:half], rows[half:])):
        H = sum(r.height for r in rr); out = Image.new('RGB', (W, H), 'white'); y = 0
        for r in rr: out.paste(r, (0, y)); y += r.height
        out.resize((W * 2 // 5, H * 2 // 5)).save('/tmp/cp/proof_%s_%d.png' % (want.replace(' ', '_'), part))
    print(p['title'], len(rows))
    break
