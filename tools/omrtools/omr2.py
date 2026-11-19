"""omr2.py PAGE yc [yc ...] : staff lines near each yc found locally, then note groups (gabc letters, pes = same x) with x."""
import sys, numpy as np, importlib.util
from PIL import Image
spec = importlib.util.spec_from_file_location('h2', '/tmp/rt/heads2_lib.py'); 
pi = int(sys.argv[1])
a = np.array(Image.open('/tmp/rt/page%d.png' % pi).convert('L')).astype(float)
sys.path.insert(0, '/home/claude/build/omr'); import staves
from scipy import ndimage as ndi
def read(a, L):
    s=(L[3]-L[0])/3; y0=int(L[0]-2.2*s); y1=int(L[3]+2.2*s)
    B=(a[y0:y1]<150); R=staves.vrun(B); C=B.copy()
    for y in L:
        yy=int(round(y))-y0; C[yy-3:yy+4]&=(R[yy-3:yy+4]>s*0.45)
    C=ndi.binary_closing(C,structure=np.ones((5,5))); C=ndi.binary_fill_holes(C)
    C=ndi.binary_opening(C,structure=np.ones((int(s*0.32),int(s*0.32))))
    lab,n=ndi.label(C); out=[]
    for sl in ndi.find_objects(lab):
        ys,xs=sl; h=ys.stop-ys.start; w=xs.stop-xs.start
        if w<s*0.3 or w>s*1.6 or h<s*0.3: continue
        k=max(1,round(h/(s*0.5))); sub=C[sl]
        for j in range(k):
            ya=int(j*h/k); yb=int((j+1)*h/k); cols=np.where(sub[ya:yb].any(0))[0]
            cx=xs.start+(int(cols.mean()) if len(cols) else w//2); cy=ys.start+(j+0.5)*h/k+y0
            out.append((cx,round((L[3]-cy)/(s/2))))
    return sorted(out)
W = a.shape[1]
for yc in map(int, sys.argv[2:]):
    win = a[yc-90:yc+90, int(W*0.15):int(W*0.9)] < 140
    row = win.mean(1)
    idx = [i for i in range(1, len(row)-1) if row[i] > 0.2 and row[i] >= row[i-1] and row[i] >= row[i+1]]
    grp = []
    for i in idx:
        if grp and i - grp[-1][-1] <= 4: grp[-1].append(i)
        else: grp.append([i])
    ys = sorted([(max(row[g]), sum(g)/len(g)) for g in grp], reverse=True)[:4]
    L = sorted(y + yc - 90 for _, y in ys)
    hs = [(x, p) for x, p in read(a, L) if -3 <= p <= 9]
    gs = []
    for x, p in hs:
        if gs and x - gs[-1][-1][0] < 28: gs[-1].append((x, p))
        else: gs.append([(x, p)])
    f = lambda g: ''.join(chr(ord('d')+p) for x, p in sorted(g, key=lambda t: (t[0]//10, t[1])))
    print('y%d lines %s | %s' % (yc, [round(v) for v in L], ' '.join('%s@%d' % (f(g), g[0][0]) for g in gs)))
