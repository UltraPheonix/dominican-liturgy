"""Rough raster reading of a staff in the Antiphonarium O.P. 1933 scan.
usage: omr.py PAGE(0-based) Y0 Y1  (fractions of page height bounding one staff + its lyrics)
prints staff line rows, then each note head: x, pitch (gabc letter for a c-clef on the line given by --clef)"""
import sys, numpy as np, pymupdf
from PIL import Image
from scipy import ndimage as ndi
SRC='/home/claude/dl/op1933/antiphonarium-1933-gillet.pdf'
def page(i):
    d=pymupdf.open(SRC); x=d[i].get_images()[0]; pix=pymupdf.Pixmap(d,x[0])
    a=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width)
    return a
def staff(a,y0,y1):
    h=a.shape[0]; A=a[int(y0*h):int(y1*h)]; B=A<150
    rows=B.sum(1); W=B.shape[1]
    cand=[i for i,v in enumerate(rows) if v>0.35*W]
    # merge adjacent rows
    lines=[]
    for i in cand:
        if lines and i-lines[-1][-1]<=2: lines[-1].append(i)
        else: lines.append([i])
    L=[sum(l)/len(l) for l in lines]
    return A,B,L
def heads(B,L):
    s=(L[-1]-L[0])/(len(L)-1)
    C=B.copy()
    # erase staff lines: pixels on a line row whose vertical run is short
    for y in L:
        for yy in range(int(y)-2,int(y)+3):
            if 0<=yy<C.shape[0]:
                up=B[max(0,yy-3):yy].any(0) if yy>2 else np.zeros(C.shape[1],bool)
                dn=B[yy+1:yy+4].any(0)
                C[yy]&=(B[max(0,yy-3)]&B[min(C.shape[0]-1,yy+3)])
    C=ndi.binary_opening(C,structure=np.ones((int(s*0.45),int(s*0.45))))
    lab,n=ndi.label(C); out=[]
    for sl in ndi.find_objects(lab):
        ys,xs=sl; hgt=ys.stop-ys.start; wid=xs.stop-xs.start
        if wid<s*0.5 or wid>s*2.5: continue
        k=max(1,round(hgt/(s*0.95)))
        for j in range(k):
            cy=ys.start+(j+0.5)*hgt/k
            out.append((xs.start,xs.stop,cy))
    out.sort()
    return out,s
if __name__=='__main__':
    p=int(sys.argv[1]); y0=float(sys.argv[2]); y1=float(sys.argv[3]); clef=sys.argv[4] if len(sys.argv)>4 else 'c3'
    a=page(p); A,B,L=staff(a,y0,y1)
    top=[l for l in L][:4]
    if len(L)<4: print('lines',L); sys.exit()
    L=L[:4]; hs,s=heads(B,L)
    # position: 0 = bottom line, 1 = space above, ... ; gabc: line1 bottom = 'd' for c4? use clef
    ln=int(clef[1]); base='abcdefghijklm'
    # c clef on line ln: that line is 'c'... gabc letter for bottom line with c-clef on line ln: positions from 'd'(bottom line, pos 0 in gabc) 
    out=[]
    for x0,x1,cy in hs:
        pos=round((L[3]-cy)/(s/2))  # 0 = bottom line
        out.append((x0,pos))
    print('s=%.1f lines=%s'%(s,[round(v) for v in L]))
    # gabc: bottom line is always 'd' in gabc letter space; clef just names the line
    print(' '.join('%d:%s'%(x,'defghijklm'[pos] if 0<=pos<10 else ('c' if pos==-1 else '?')) for x,pos in out))
