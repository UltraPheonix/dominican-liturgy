#!/bin/bash
# usage: r.sh PDFPAGE [L|R|LT|LB|RT|RB]
N=$1; P=${2:-}
f=/tmp/A2/pg-$N.png
[ -f $f ] || { pdftoppm -r 150 -f $N -l $N -png /home/claude/dl/missal/M39.pdf /tmp/A2/pgx; mv /tmp/A2/pgx-*$N.png $f; }
python3 - "$f" "$P" "$N" <<'PY'
import sys
from PIL import Image
f,P,N=sys.argv[1:4]
im=Image.open(f); W,H=im.size
# crop away black border approx
box={'L':(int(W*0.08),int(H*0.03),int(W*0.5),int(H*0.97)),'R':(int(W*0.49),int(H*0.03),int(W*0.9),int(H*0.97))}
side=P[0] if P else 'L'
x0,y0,x1,y1=box[side]
if len(P)>1:
    h=(y1-y0)
    if P[1]=='T': y1=y0+int(h*0.55)
    else: y0=y0+int(h*0.45)
im.crop((x0,y0,x1,y1)).save('/tmp/A2/v-%s%s.png'%(N,P))
print('/tmp/A2/v-%s%s.png'%(N,P), im.size)
PY
