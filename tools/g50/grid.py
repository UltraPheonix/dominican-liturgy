"""A staff of the Graduale O.P. (1950) scan, enlarged, with every line and space labelled by its gabc letter (for a C clef
on line N or an F clef the letters are positions: d = bottom line ... k = above the top line) -- for reading by eye.
usage: grid.py PDFPAGE STAFF [x0 x1]  -> /tmp/gt/grid_<page>_<staff>.png   (STAFF counted from the top, 0-based)"""
import sys, subprocess, glob, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, '/home/claude/dominican-liturgy/tools/pdfomr')
from m39app import staves, deskew
pg, si = int(sys.argv[1]), int(sys.argv[2])
subprocess.run(['pdfimages', '-f', str(pg), '-l', str(pg), '-png', '/tmp/dl/g/g.pdf', '/tmp/gt/nat'], check=True)
f = max(glob.glob('/tmp/gt/nat-*.png'), key=lambda x: Image.open(x).size[0])
g0 = np.array(Image.open(f).convert('L')).astype(float)
for x in glob.glob('/tmp/gt/nat-*.png'): __import__('os').remove(x)
# staves() expects ~400 dpi: scale 2x
im = Image.fromarray(g0.astype(np.uint8)).resize((g0.shape[1] * 2, g0.shape[0] * 2), Image.LANCZOS)
g = np.array(im).astype(float); g, ang = deskew(g)
st = staves(g); L = st[si]; s = (L[3] - L[0]) / 3
x0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0; x1 = int(sys.argv[4]) if len(sys.argv) > 4 else g.shape[1]
y0 = max(0, int(L[0] - 3 * s)); y1 = int(L[3] + 2.6 * s)
c = Image.fromarray(g[y0:y1, x0:x1].astype(np.uint8)).convert('RGB')
Z = float(__import__("os").environ.get("Z", 2)); c = c.resize((int(c.width * Z), int(c.height * Z)), Image.LANCZOS)
d = ImageDraw.Draw(c); font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
for k in range(-3, 11):   # positions: 0 = bottom line
    y = (L[3] - k * s / 2 - y0) * Z
    col = (0, 150, 0) if k % 2 == 0 else (230, 120, 0)
    for xx in range(0, c.width, 160):
        d.text((xx, y - 12), chr(ord('d') + k), fill=col, font=font)
    if k % 2 == 1: d.line([(0, y), (c.width, y)], fill=(255, 200, 120), width=1)
c.save('/tmp/gt/grid_%d_%d.png' % (pg, si)); print(len(st), 'staves; size', c.size)
