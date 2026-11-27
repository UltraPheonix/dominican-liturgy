import sys
from PIL import Image
import numpy as np
f=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2].split(','))
im=np.array(Image.open(f).convert('L').crop((x0,y0,x1,y1)))<120
cols=im.sum(0)>0
segs=[];s=None;gap=0
for x,c in enumerate(cols):
    if c:
        if s is None: s=x
        last=x
    elif s is not None and x-last>int(sys.argv[3] if len(sys.argv)>3 else 6):
        segs.append((s,last));s=None
if s is not None: segs.append((s,last))
print(' '.join('%d-%d'%(a+x0-int(sys.argv[4] if len(sys.argv)>4 else x0),b+x0-int(sys.argv[4] if len(sys.argv)>4 else x0)) for a,b in segs))
