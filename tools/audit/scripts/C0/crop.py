#!/usr/bin/env python3
"""crop.py PDFPAGE WORD [NLINES] OUT.png : crop the M39 scan around the first word matching WORD (case-insensitive)."""
import sys, subprocess, re, html
pg, word = int(sys.argv[1]), sys.argv[2].lower(); n = int(sys.argv[3]); out = sys.argv[4]
pdf = '/home/claude/dl/missal/M39.pdf'
x = subprocess.run(['pdftotext', '-bbox', '-f', str(pg), '-l', str(pg), pdf, '-'], capture_output=True, text=True).stdout
pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', x).groups())
for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', x):
    if word in html.unescape(m.group(5)).lower():
        x0, y0 = float(m.group(1)), float(m.group(2)); break
else: sys.exit('not found')
half = 0 if x0 < pw / 2 else 1; r = 300; s = r / 72
X0 = int((half * pw / 2) * s); W = int(pw / 2 * s); Y0 = int(max(0, y0 - 14) * s); H = int(n * 13 * s)
subprocess.run(['pdftoppm', '-r', str(r), '-f', str(pg), '-l', str(pg), '-x', str(X0), '-y', str(Y0), '-W', str(W), '-H', str(H), '-png', '-singlefile', pdf, out[:-4]])
print(out)
