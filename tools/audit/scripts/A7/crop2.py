#!/usr/bin/env python3
"""crop2.py PDFPAGE WORD NLINES OUT.png [OCC] [DPI]: like C0/crop.py, but the OCC-th match (1-based) and a DPI; crop = the column of the match (half-page width)."""
import sys, subprocess, re, html
pg, word, n, out = int(sys.argv[1]), sys.argv[2].lower(), int(sys.argv[3]), sys.argv[4]
occ = int(sys.argv[5]) if len(sys.argv) > 5 else 1; r = int(sys.argv[6]) if len(sys.argv) > 6 else 220
pdf = '/home/claude/dl/missal/M39.pdf'
x = subprocess.run(['pdftotext', '-bbox', '-f', str(pg), '-l', str(pg), pdf, '-'], capture_output=True, text=True).stdout
pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).groups())
c = 0
for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x):
    if word in html.unescape(m.group(5)).lower():
        c += 1
        if c == occ: x0, y0 = float(m.group(1)), float(m.group(2)); break
else: sys.exit('not found')
s = r / 72; X0 = int(max(0, x0 - 175) * s); W = int(360 * s); import os; pre = int(os.environ.get("PRE", "0")); Y0 = int(max(0, y0 - 14 - 13 * pre) * s); H = int(n * 13 * s)
subprocess.run(['pdftoppm', '-r', str(r), '-f', str(pg), '-l', str(pg), '-x', str(X0), '-y', str(Y0), '-W', str(W), '-H', str(H), '-png', '-singlefile', pdf, out[:-4]])
print(out)
