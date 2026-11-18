"""list the staves of a 1933 page and read their note heads.
usage: staves.py PAGE  -> for each staff: index, line rows, notes x:pos (pos 0 = bottom line, 1 = space above ...)"""
import sys, numpy as np, omr
from scipy import ndimage as ndi
def find(a):
    B=a<170; r=B.sum(1); W=a.shape[1]
    cand=[i for i,v in enumerate(r) if v>0.3*W]
    rows=[]
    for i in cand:
        if rows and i-rows[-1][-1]<=2: rows[-1].append(i)
        else: rows.append([i])
    L=[sum(x)/len(x) for x in rows]
    st=[]; i=0
    while i+3<len(L):
        d=[L[i+k+1]-L[i+k] for k in range(3)]
        if all(20<x<45 for x in d) and max(d)-min(d)<5: st.append(L[i:i+4]); i+=4
        else: i+=1
    return st
def vrun(B):
    # vertical run length through each dark pixel
    H,W=B.shape; up=np.zeros((H,W),int); dn=np.zeros((H,W),int)
    for y in range(H):
        up[y]=np.where(B[y],(up[y-1] if y else 0)+1,0)
    for y in range(H-1,-1,-1):
        dn[y]=np.where(B[y],(dn[y+1] if y<H-1 else 0)+1,0)
    return up+dn-1
def read(a,L,raw=False):
    s=(L[3]-L[0])/3; y0=int(L[0]-3.2*s); y1=int(L[3]+1.6*s)
    B=(a[y0:y1]<160)
    R=vrun(B); C=B.copy()
    for y in L:
        yy=int(round(y))-y0
        C[yy-4:yy+5]&=(R[yy-4:yy+5]>s*0.4)
    C=ndi.binary_closing(C,structure=np.ones((5,5)))
    C=ndi.binary_fill_holes(C)
    C=ndi.binary_opening(C,structure=np.ones((int(s*0.22),int(s*0.22))))
    lab,n=ndi.label(C); out=[]
    for sl in ndi.find_objects(lab):
        ys,xs=sl; hgt=ys.stop-ys.start; wid=xs.stop-xs.start
        if wid<s*0.25 or wid>s*0.85 or hgt<s*0.25: continue
        k=max(1,round(hgt/(s*0.47)))
        for j in range(k):
            cy=ys.start+(j+0.5)*hgt/k+y0
            out.append((xs.start,wid,round((L[3]-cy)/(s/2))))
    out.sort(key=lambda t:(t[0]//8,t[2]))
    return out
G='abcdefghijklm'
def name(pos,clef):
    # gabc letters: with a c-clef on line n, the bottom line (pos 0) is: c4->d, c3->f, c2->h, c1->j ; f3->... 
    base={'c4':3,'c3':5,'c2':7,'c1':9,'f4':0,'f3':2}[clef]
    i=base+pos
    return G[i] if 0<=i<len(G) else '?'
if __name__=='__main__':
    a=omr.page(int(sys.argv[1])); clef=sys.argv[2] if len(sys.argv)>2 else 'c4'
    for i,L in enumerate(find(a)):
        print(i,[round(v) for v in L])
        print('  ',' '.join('%d:%s'%(x,name(p,clef)) for x,w,p in read(a,L)))
