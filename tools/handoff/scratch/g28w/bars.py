# bars.py PNM X0 X1 L1,L2,L3,L4 : vertical thin strokes (bars and stems) with extent in pitch positions
import sys, numpy as np
from PIL import Image
pnm,x0,x1=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); L=[float(v) for v in sys.argv[4].split(',')]
gap=(L[3]-L[0])/3; half=gap/2
y0=int(L[0]-2*gap); y1=int(L[3]+2*gap)
b=np.array(Image.open(pnm).convert('L').crop((x0,y0,x1,y1)))<100
H,W=b.shape
res=[]
for c in range(W):
    col=b[:,c]; best=(0,0,0); r=0
    for i in range(H):
        r=r+1 if col[i] else 0
        if r>best[0]: best=(r,i-r+1,i)
    if best[0]>gap*0.9:
        # thin: left and right neighbors at mid-run mostly white
        res.append((c,best[1],best[2]))
# cluster
out=[];cur=[]
for t in res:
    if cur and t[0]-cur[-1][0]>2: out.append(cur);cur=[]
    cur.append(t)
if cur: out.append(cur)
def pos(y): return 'abcdefghijklmn'[max(0,min(13,3+round((L[3]-(y+y0))/half)))]
for g in out:
    w=len(g); 
    if w>gap*0.35: continue
    top=min(t[1] for t in g); bot=max(t[2] for t in g)
    print('%d w%d %s-%s len%.1f'%(g[0][0]+x0,w,pos(top),pos(bot),(bot-top)/gap))
