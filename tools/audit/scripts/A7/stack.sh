#!/bin/sh
# stack.sh OUT.png IN1.png IN2.png ... : stack crops vertically with their names
python3 - "$@" <<'PY'
import sys
from PIL import Image, ImageDraw
out, fs = sys.argv[1], sys.argv[2:]
ims = [Image.open(f) for f in fs]
w = max(i.width for i in ims); h = sum(i.height + 18 for i in ims)
o = Image.new('RGB', (w, h), 'white'); y = 0; d = ImageDraw.Draw(o)
for f, i in zip(fs, ims): d.text((5, y), f, fill='red'); o.paste(i, (0, y + 16)); y += i.height + 18
o.save(out)
PY
