"""proof images for staves: scan crop with the transcription of its syllables underneath (index:syllable(notes))
usage: proofstaff.py TITLEPART [all]  -> /tmp/cp/ps_<n>.png"""
import sys, pickle, textwrap, numpy as np
sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFont
from m39app import main
S = pickle.load(open('/tmp/m39pref_spans.pkl', 'rb'))
want = sys.argv[1]; allst = len(sys.argv) > 2
only = [int(v) for v in sys.argv[2].split(',')] if allst and sys.argv[2] != 'all' else None
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 34)
cache = {}; imgs = []
for p in S:
    if want not in p['title'] or not p['_spans']: continue
    for (pg, sd, L, X, lo, hi, how) in p['_spans']:
        if how == '1:1' and not allst: continue
        if only and not any(lo <= v <= hi for v in only): continue
        if (pg, sd) not in cache: cache[(pg, sd)] = main('/home/claude/dl_m39/M39.pdf', pg, sd)[1]
        g = cache[(pg, sd)]; s = (L[3] - L[0]) / 3
        im0 = Image.fromarray(g.astype('uint8')).convert('RGB'); d0 = ImageDraw.Draw(im0)
        f2 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
        for i in range(lo, hi + 1):
            col = [(220, 0, 0), (0, 90, 255), (0, 150, 0)][i % 3]
            for nx, pos in p['_nx'][i]:
                yy = L[3] - pos * s / 2
                d0.rectangle([nx - 3, yy - 12, nx + 25, yy + 12], outline=col, width=3)
                d0.text((nx, L[0] - 2.2 * s + (i % 2) * 34), '%d%s' % (i, chr(100 + pos)), fill=col, font=f2)
        crop = im0.crop((max(0, X[0] - 40), int(L[0] - 2.4 * s), X[1] + 60, int(L[3] + 2.6 * s)))
        txt = '  '.join('%d:%s(%s)%s' % (i, p['_notes'][i][0], p['_notes'][i][1], (' ' + p['_notes'][i][2]) if p['_notes'][i][2] else '') for i in range(lo, hi + 1))
        lines = textwrap.wrap(txt, width=crop.width // 21)
        im = Image.new('RGB', (crop.width, crop.height + 44 * len(lines) + 10), 'white'); im.paste(crop, (0, 0))
        dr = ImageDraw.Draw(im)
        for k, l in enumerate(lines): dr.text((10, crop.height + 4 + 44 * k), l, fill=(180, 0, 0), font=font)
        imgs.append(im)
n = 0
for k in range(0, len(imgs), 2):
    grp = imgs[k:k + 2]; W = max(i.width for i in grp); H = sum(i.height for i in grp)
    out = Image.new('RGB', (W, H), 'white'); y = 0
    for i in grp: out.paste(i, (0, y)); y += i.height
    out.resize((W * 3 // 5, H * 3 // 5)).save('/tmp/cp/ps_%d.png' % n); n += 1
print(n, 'sheets,', len(imgs), 'staves')
