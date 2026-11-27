#!/bin/bash
# multi.sh out.png "page|phrase|up|dn" ...
out=$1; shift; n=0; files=()
for a in "$@"; do IFS='|' read p ph up dn xs <<< "$a"; n=$((n+1)); python3 /tmp/A1/look.py $p "$ph" ${up:-40} ${dn:-60} /tmp/A1/m_$n.png ${xs:-0} 2>/dev/null | grep -q NOT && echo "NOT FOUND: $a"; [ -f /tmp/A1/m_$n.png ] && files+=(/tmp/A1/m_$n.png); done
python3 - "$out" "${files[@]}" <<'P'
import sys
from PIL import Image
ims=[Image.open(f) for f in sys.argv[2:]]
W=max(i.width for i in ims); H=sum(i.height+10 for i in ims)
M=Image.new('RGB',(W,H),'gray'); y=0
for i in ims: M.paste(i,(0,y)); y+=i.height+10
M.save(sys.argv[1]); print(sys.argv[1],M.size)
P
rm -f /tmp/A1/m_*.png
