# staffs.py PNM XA XB : print staves as (lines at XA ; lines at XB)
import sys, numpy as np
from PIL import Image
im=np.array(Image.open(sys.argv[1]).convert('L'))<100
def lines(a):
    prof=im[:,a:a+200].mean(1)
    ys=[i for i in range(len(prof)) if prof[i]>0.5]
    g=[]
    for y in ys:
        if g and y-g[-1][-1]<=3: g[-1].append(y)
        else: g.append([y])
    c=[round(sum(x)/len(x)) for x in g]
    st=[];cur=[]
    for y in c:
        if cur and not (40<y-cur[-1]<62): 
            if len(cur)==4: st.append(cur)
            cur=[]
        cur.append(y)
    if len(cur)==4: st.append(cur)
    return st
A=lines(int(sys.argv[2])); B=lines(int(sys.argv[3]))
for s in A:
    m=[t for t in B if abs(t[0]-s[0])<60]
    print(','.join(map(str,s)), ','.join(map(str,m[0])) if m else '?')
