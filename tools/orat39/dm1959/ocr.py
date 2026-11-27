# Tesseract (eng, psm 6, 300 dpi) on the cropped rows of each paired prayer (English and Latin halves).
# usage: python3 ocr.py PART N      -> work/crops/<pair>_<e|l>_<k>.tsv  (+ .json with the crop rectangle)
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import fitz, pickle, subprocess, json, warnings, collections
warnings.filterwarnings('ignore')
from PIL import Image, ImageOps
doc = fitz.open(PDF)
pairs, _, _ = pickle.load(open(W_('pairs.pkl'), 'rb'))
part, n = int(sys.argv[1]), int(sys.argv[2])
import re
# jobs: lines "i side" (from need.py); default: every pair, both halves
jobs = [tuple(l.split()) for l in open(sys.argv[3])] if len(sys.argv) > 3 else [(str(i), s) for i in range(len(pairs)) for s in 'el']
END = re.compile(r'\b(Per\s+D|Per\s+eu|Per\s+Christ|Qui\s+viv|Qui\s+tecum|through\s+(our|the|Christ|Jesus)|[Ww]ho\s+live)')
def rows_to_end(rows, lines):
    # the prayer's rows up to the one with its conclusion (at most 14)
    out = []
    for (p, g, lab), t in zip(rows, lines):
        out.append((p, g, lab))
        if END.search(t) or len(out) >= 14: break
    return out
os.makedirs(W_('crops'), exist_ok=True)
DPI = 300; PAD = 24
for j, (i, side) in enumerate(jobs):
    i = int(i); x = pairs[i]
    if j % n != part: continue
    if True:
        byp = collections.OrderedDict()
        for p, g, lab in rows_to_end(x[side + 'rows'], x[side + 'lines']): byp.setdefault(p, []).extend(g)
        for k, (p, gs) in enumerate(byp.items()):
            out = W_(f'crops/{i:04d}_{side}_{k}')
            if os.path.exists(out + '.tsv'): continue
            r = fitz.Rect(min(g[0] for g in gs) - 3, min(g[1] for g in gs) - 1.5, max(g[2] for g in gs) + 3, max(g[3] for g in gs) + 1.5)
            r = r & doc[p].rect
            png = W_(f'crops/tmp{part}.png')
            pm = doc[p].get_pixmap(dpi=DPI, clip=r)
            pm.save(png)
            im = ImageOps.expand(Image.open(png).convert('L'), border=PAD, fill=255); im.save(png)
            subprocess.run(['tesseract', png, out, '-l', 'eng', '--psm', '6', 'tsv'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            json.dump({'p': p, 'rect': [r.x0, r.y0, r.x1, r.y1], 'dpi': DPI, 'pad': PAD, 'g': gs}, open(out + '.json', 'w'))
