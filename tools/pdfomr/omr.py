"""Read the Gregorio chant engraved in the All Saints priest missal back into GABC.
usage: omr.py PAGE(1-based) X0 X1 (pt, column range)  -> prints gabc per staff"""
import sys, pymupdf, numpy as np, re
sys.path.insert(0,'/home/claude/build/pdfomr'); from syl import syllables
from scipy import ndimage as ndi
PDF='/mnt/user-data/uploads/e44c8a9f-2_Priest_Missal_-_All_Saints_OP_2026-11-12.pdf'
pn=int(sys.argv[1])-1; X0=float(sys.argv[2]); X1=float(sys.argv[3])
d=pymupdf.open(PDF); p=d[pn]; Z=300/72
pix=p.get_pixmap(dpi=300); A=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].astype(int)
x0,x1=int(X0*Z),int(X1*Z)
A=A[:,x0:x1]
R,G,B=A[...,0],A[...,1],A[...,2]
gold=(abs(R-189)<45)&(abs(G-158)<45)&(abs(B-94)<50)&(R-B>50)
black=(R+G+B)<230
row=gold.mean(1)
ys=[y for y in range(len(row)) if row[y]>0.12]
g=[]
for y in ys:
    if g and y-g[-1][-1]<=2: g[-1].append(y)
    else: g.append([y])
lines=[sum(a)/len(a) for a in g]
staves=[]; i=0
while i+3<len(lines):
    q=lines[i:i+4]; dd=np.diff(q)
    if dd.max()-dd.min()<4 and 10<dd.min()<60: staves.append(q); i+=4
    else: i+=1
# text chars (lyrics) in the column
raw=p.get_text('rawdict')
chars=[]
for b in raw['blocks']:
    for l in b.get('lines',[]):
        for s in l['spans']:
            if 'Garamond' not in s['font']: continue
            for ch in s['chars']:
                bx=ch['bbox']
                if X0-2<=bx[0]<=X1: chars.append((bx[0]*Z-x0,bx[1]*Z,bx[2]*Z-x0,bx[3]*Z,ch['c'],s['size'],s['color']))
for L in staves:
    sp=(L[3]-L[0])/3; top=int(L[0]-3*sp); bot=int(L[3]+3*sp)
    M=black[top:bot].copy()
    for c in chars:
        a0,b0,a1,b1=int(c[0])-2,int(c[1])-top-2,int(c[2])+2,int(c[3])-top+2
        if b1>0 and b0<M.shape[0]: M[max(0,b0):max(0,b1),max(0,a0):a1]=False
    lab,n=ndi.label(M); objs=ndi.find_objects(lab)
    notes=[]; bars=[]
    for k,sl in enumerate(objs):
        yy,xx=sl; h=yy.stop-yy.start; w=xx.stop-xx.start
        if h>2.2*sp and w<0.35*sp: bars.append((xx.start, h/sp)); continue
        if w<0.35*sp or h<0.35*sp: continue
        sub=(lab[sl]==k+1)
        # keep the thick parts only (note heads), dropping stems and thin joins
        run=np.zeros(sub.shape,int)
        for r in range(sub.shape[0]):
            c=0
            for q in range(sub.shape[1]):
                c=c+1 if sub[r,q] else 0; run[r,q]=c
        thick=np.zeros_like(sub)
        for r in range(sub.shape[0]):
            q=sub.shape[1]-1
            while q>=0:
                if run[r,q]>=0.38*sp: thick[r,q-run[r,q]+1:q+1]=True; q-=run[r,q]
                else: q-=1
        tl,tn=ndi.label(thick)
        for tsl in ndi.find_objects(tl):
            ty,tx=tsl; th=ty.stop-ty.start; tw=tx.stop-tx.start
            if th<0.3*sp: continue
            parts=[(tx.start,tx.stop)]
            if tw>0.85*sp:
                k2=max(2,round(tw/(sp*0.56))); parts=[(tx.start+int(i*tw/k2),tx.start+int((i+1)*tw/k2)) for i in range(k2)]
            for pa,pb in parts:
                m=thick[ty,pa:pb]; rows=np.where(m.any(1))[0]
                if not len(rows): continue
                segs=[]
                for r in rows:
                    if segs and r-segs[-1][-1]<=1: segs[-1].append(r)
                    else: segs.append([r])
                for sg in segs:
                    hh=len(sg); nh=max(1,round(hh/(sp*0.5)))
                    if hh<0.3*sp: continue
                    for j in range(nh):
                        cy=top+yy.start+ty.start+sg[0]+(j+0.5)*hh/nh
                        notes.append((xx.start+(pa+pb)/2, round((L[3]-cy)/(sp/2))))
    ly=[c for c in chars if L[3]+0.5*sp < c[1] < L[3]+4.5*sp]
    ly.sort()
    notes=[t for t in notes if -4<t[1]<12]
    notes.sort()
    print('  notes:',' '.join('%s@%d'%(chr(ord('d')+pp),x) for x,pp in notes))
    # syllables: runs of characters split at spaces and hyphens
    syl=[]; cur=None
    for c in ly:
        ch=c[4]
        if ch in ' -':
            if cur: syl.append(cur); cur=None
            continue
        if cur and c[0]-cur['x1']>sp*0.22: syl.append(cur); cur=None
        if not cur: cur={'x0':c[0],'x1':c[2],'t':ch,'sep':' '}
        else: cur['x1']=c[2]; cur['t']+=ch
    if cur: syl.append(cur)
    # split words into syllables, keeping each syllable's x
    words=[]; cur=[]
    for c in ly:
        if c[4] in ' -':
            if cur: words.append((cur,c[4]=='-')); cur=[]
            continue
        if cur and c[0]-cur[-1][2]>sp*0.22: words.append((cur,False)); cur=[]
        cur.append(c)
    if cur: words.append((cur,False))
    syl=[]
    for ws,hy in words:
        w=''.join(c[4] for c in ws)
        core=re.sub(r'[^\wæœǽÆŒ]','',w)
        st=syllables(w) if core else [0]
        for k,a in enumerate(st):
            b=st[k+1] if k+1<len(st) else len(w)
            vi=[q for q in range(a,b) if ws[q][4].lower() in 'aeiouyáéíóúýæœǽ']
            vx=ws[vi[0]][0] if vi else ws[a][0]
            syl.append({'x0':vx,'x1':ws[b-1][2],'t':w[a:b],'end': k==len(st)-1 and not hy})
    # a hyphen after a syllable: mark continuation
    txt=''.join(c[4] for c in ly)
    # assign notes: each note to the last syllable starting before it (+ tolerance)
    for sy in syl: sy['n']=[]
    gl=np.where(gold[int(L[0])])[0]; sx=gl.min() if len(gl) else 0
    clef=[t for t in notes if t[0]<sx+sp*1.1]
    body=[t for t in notes if t[0]>=sx+sp*1.1]
    for x,pp in body:
        best=None
        for sy in syl:
            if sy['x0']-sp*0.25<=x: best=sy
        if best is None and syl: best=syl[0]
        if best is not None: best['n'].append((x,pp))
    def letters(ns):
        ns=sorted(ns, key=lambda t:(round(t[0]/(sp*0.35)), t[1]))
        return ''.join(chr(ord('d')+p) for x,p in ns)
    # bars: pairs close together = double bar
    bars.sort(); bl=[]
    for x,h in bars:
        if bl and x-bl[-1][0]<sp*0.8: bl[-1]=(bl[-1][0],'::')
        else: bl.append((x,':' if h>2.6 else (';' if h>1.6 else ',')))
    out=''
    for k,sy in enumerate(syl):
        t=sy['t']
        if re.fullmatch(r'[RV]\.',t): out+='<sp>%s/</sp>.() '%t[0]; continue
        out+='%s(%s)%s'%(t,letters(sy['n']),' ' if sy['end'] else '')
        last=max([x for x,p in sy['n']] or [sy['x0']]); nxt=syl[k+1]['x0'] if k+1<len(syl) else 1e9
        for bx,bt in bl:
            if last<bx<nxt+sp*0.3 and not (k+1<len(syl) and bx>max([x for x,p in syl[k+1]['n']] or [nxt])): out+='(%s) '%bt
    print('GABC|'+out.strip())
    words=''.join(c[4] for c in ly)
    print('STAFF y=%d sp=%.1f'%(L[0],sp))
    print('  notes:',' '.join('%s@%d'%(chr(ord('d')+pp),x) for x,pp in notes if -4<pp<12))
    print('  bars:',' '.join('%d(%.1f)'%(x,h) for x,h in bars))
    out=[]; cur=None
    for c in ly:
        out.append('%s@%d'%(c[4],c[0]))
    print('  text:', ' '.join(out))
