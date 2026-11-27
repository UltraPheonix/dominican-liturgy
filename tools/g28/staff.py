# staff crop with pitch grid and the text layer's words marked; split in N parts, zoomed
import sys, subprocess, re
from PIL import Image, ImageDraw, ImageFont
import numpy as np
djvu, page, x0, y0, x1, y1, out = sys.argv[1], int(sys.argv[2]), *map(int, sys.argv[3:7]), sys.argv[7]
n = int(sys.argv[8]) if len(sys.argv) > 8 else 3
pnm = '/tmp/_p%d.pnm' % page
import os
if not os.path.exists(pnm): subprocess.run(['ddjvu', '-format=pnm', '-page=%d' % page, djvu, pnm], check=True)
full = Image.open(pnm).convert('L'); H = full.height
im = full.crop((x0, y0, x1, y1))
a = np.array(im) < 110
prof = a.sum(1) / a.shape[1]
cand = [i for i in range(len(prof)) if prof[i] > 0.3]
lines = []
for i in cand:
    if lines and i - lines[-1][-1] <= 4: lines[-1].append(i)
    else: lines.append([i])
ls = [sum(g) / len(g) for g in lines]
ls = [float(v) - y0 for v in os.environ['LINES'].split(',')] if os.environ.get('LINES') else ls[-4:]; gap = (ls[-1] - ls[0]) / 3
print('lines', [round(l) for l in ls], 'gap', round(gap))
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
rgb = im.convert('RGB'); dr = ImageDraw.Draw(rgb)
for k in range(-3, 10):
    y = ls[-1] - k * gap / 2
    L = 'abcdefghijklmn'[3 + k]
    col = (230, 0, 0) if k % 2 == 0 else (0, 120, 255)
    for x in range(0, rgb.width, 30): dr.line([(x, y), (x + 8, y)], fill=col, width=1)
    for x in range(5, rgb.width, 200): dr.text((x, y - 10), L, fill=col, font=font)
# words of the text layer under this staff (djvu y from the bottom)
txt = subprocess.run(['djvused', djvu, '-e', 'select %d; print-txt' % page], capture_output=True, text=True).stdout
for m in re.finditer(r'\(word (\d+) (\d+) (\d+) (\d+) "([^"]*)"\)', txt):
    wx0, wy0, wx1, wy1, w = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), m.group(5)
    ty = H - wy1
    if x0 <= wx0 <= x1 and y1 - 10 <= ty <= y1 + 160:
        dr.line([(wx0 - x0, rgb.height - 30), (wx0 - x0, rgb.height)], fill=(0, 150, 0), width=3)
        dr.text((wx0 - x0 + 3, rgb.height - 26), w.encode('latin1', 'ignore').decode('utf8', 'ignore') if False else w, fill=(0, 130, 0), font=font)
W = rgb.width; step = W // n
for i in range(n):
    c = rgb.crop((max(0, i * step - 30), 0, min(W, (i + 1) * step + 30), rgb.height))
    c = c.resize((int(c.width * 1.25), int(c.height * 1.25)))
    c.save('%s_%d.png' % (out, i))
