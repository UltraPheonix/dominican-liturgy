"""zz.py PAGE S0 S1 [x0 x1 scale] : stack zoomed staves S0..S1 -> /tmp/rt/zz.png"""
import sys, subprocess
from PIL import Image
p, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
x0, x1, sc = (sys.argv[4], sys.argv[5], sys.argv[6]) if len(sys.argv) > 6 else ('240', '1570', '0.95')
ims = []
for s in range(a, b + 1):
    subprocess.run(['python3', '/tmp/rt/zs.py', p, str(s), x0, x1, sc], capture_output=True)
    ims.append(Image.open('/tmp/rt/zs.png').copy())
o = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims)), 'white'); y = 0
for i in ims: o.paste(i, (0, y)); y += i.height
o.convert('L').save('/tmp/rt/zz.png')
