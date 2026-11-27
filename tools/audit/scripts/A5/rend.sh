#!/bin/bash
# usage: rend.sh PDFPAGE  -> /tmp/A5/img/P-{L,R}{1,2}.png (left/right half, top/bottom)
p=$1; r=${2:-170}
cd /tmp/A5/img
[ -f pg$p.png ] || pdftoppm -f $p -l $p -r $r -png -singlefile /home/claude/dl/missal/M39.pdf pg$p
python3 - <<PY
from PIL import Image
im=Image.open('/tmp/A5/img/pg$p.png'); w,h=im.size
for s,(x0,x1) in (('L',(0,w//2+10)),('R',(w//2-10,w))):
    for t,(y0,y1) in (('1',(0,h//2+40)),('2',(h//2-40,h))):
        im.crop((x0,y0,x1,y1)).save('/tmp/A5/img/%s-%s%s.png'%('$p',s,t))
PY
