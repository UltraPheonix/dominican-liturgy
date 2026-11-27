import sys, numpy as np
from PIL import Image
pnm = sys.argv[1]
im = np.array(Image.open(pnm).convert('L')).astype(float) < 100
W = im.shape[1]
for name,(a,b) in {'L':(int(W*0.12),int(W*0.20)),'R':(int(W*0.60),int(W*0.68))}.items():
    prof = im[:, a:b].mean(1)
    cand = [i for i in range(len(prof)) if prof[i] > 0.5]
    groups = []
    for i in cand:
        if groups and i - groups[-1][-1] <= 3: groups[-1].append(i)
        else: groups.append([i])
    ys = [round(sum(g)/len(g)) for g in groups]
    out=[]; cur=[]
    for y in ys:
        if cur and y - cur[-1] > 70: out.append(cur); cur=[]
        cur.append(y)
    out.append(cur)
    print(name, [s for s in out if len(s)>=3])
