"""OMR of a Graduale O.P. (1950) page with a proof image: each note head read by tools/pdfomr/m39app.py is marked on the
scan with its gabc letter (position: d = bottom line), bars in blue.  usage: omrproof.py PDFPAGE [STAFF,...] -> /tmp/gt/op_<page>_<staff>.png
and a text line per staff: x:letter ... (for writing the gabc by hand, checked against the image)"""
import sys, json, numpy as np
sys.path.insert(0, '/home/claude/dominican-liturgy/tools/pdfomr')
from m39app import main
from PIL import Image, ImageDraw, ImageFont
pg = int(sys.argv[1]); want = [int(v) for v in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
res, g = main('/tmp/dl/g/g.pdf', pg - 1, 'F')
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
for d in res:
    if want is not None and d['staff'] not in want: continue
    L = d['L']; s = d['s']; y0 = int(L[0] - 3.5 * s); y1 = int(L[3] + 3.6 * s)
    im = Image.fromarray(g[y0:y1].astype(np.uint8)).convert('RGB'); dr = ImageDraw.Draw(im)
    seq = []
    for it in d['items']:
        if it[1] == 'note':
            if not (-3 <= it[2] <= 10) or it[0] < d['x'][0] + 1.2 * s: continue
            ch = chr(ord('d') + it[2]); seq.append((it[0], ch))
            dr.text((it[0], 2 + (len(seq) % 2) * 26), ch, fill=(220, 0, 0), font=font)
        else:
            seq.append((it[0], '|')); dr.line([(it[0], 0), (it[0], 12)], fill=(0, 0, 255), width=4)
    im.save('/tmp/gt/op_%d_%d.png' % (pg, d['staff']))
    print('staff', d['staff'], 'x', d['x'], ' '.join('%d:%s' % (x, c) for x, c in seq))
    print('   words', [w[2] for w in d['words']])
