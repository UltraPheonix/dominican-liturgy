"""crop.py BP COL Y [H] -> /tmp/crop.png : a strip of the Missal column around y (300 dpi coords)"""
import sys; sys.path.insert(0, '/home/claude/build/m39hw')
from ocr39 import spread, render, columns
from PIL import Image
bp, c, y = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); h = int(sys.argv[4]) if len(sys.argv) > 4 else 500
pdfp, side = spread(bp); img = render(pdfp); H, W, _ = img.shape
half = img[:, :W // 2] if side == 0 else img[:, W // 2:]
cols = columns(half); x0, x1 = cols[c]
im = Image.fromarray(half[max(0, y - 120):y + h, max(0, x0 - 10):x1 + 10])
im.save(sys.argv[5] if len(sys.argv) > 5 else '/tmp/crop.png')
