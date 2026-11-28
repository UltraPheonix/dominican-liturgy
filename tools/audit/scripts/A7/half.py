#!/usr/bin/env python3
"""half.py PDFPAGE L|R TOP BOTTOM OUT.png [DPI]: render the left/right half of a pdf page between fractions TOP..BOTTOM of its height."""
import sys, subprocess, re
pg, side, t, b, out = int(sys.argv[1]), sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
r = int(sys.argv[6]) if len(sys.argv) > 6 else 220
pdf = '/home/claude/dl/missal/M39.pdf'
info = subprocess.run(['pdfinfo', '-f', str(pg), '-l', str(pg), pdf], capture_output=True, text=True).stdout
pw, ph = map(float, re.search(r'Page\s+\d+ size:\s+([\d.]+) x ([\d.]+)', info).groups())
s = r / 72; X0 = 0 if side == 'L' else int(pw / 2 * s); W = int(pw / 2 * s)
subprocess.run(['pdftoppm', '-r', str(r), '-f', str(pg), '-l', str(pg), '-x', str(X0), '-y', str(int(ph * t * s)), '-W', str(W), '-H', str(int(ph * (b - t) * s)), '-png', '-singlefile', pdf, out[:-4]])
print(out)
