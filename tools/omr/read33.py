"""Read one antiphon from the Antiphonarium O.P. 1933 scan into GABC.
usage: read33.py PAGE_INDEX(0-based) "full antiphon text with accents" [--staff N] [--clef c4]
Prints the GABC and saves /tmp/om/crop.png with the staves used, for checking by eye."""
import sys, re, os, json, subprocess, unicodedata, difflib, numpy as np
from PIL import Image
from scipy import ndimage as ndi
import omr, staves
TESS={'TESSDATA_PREFIX':'/home/claude/tess'}
def key(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub('[^a-z]','',s.replace('æ','ae').replace('œ','oe').replace('j','i'))
def hocr(pi,a):
    f='/tmp/om/h%04d'%pi
    if not os.path.exists(f+'.hocr'):
        Image.fromarray(a).save(f+'.png')
        subprocess.run(['tesseract',f+'.png',f,'-l','lat','--psm','3','-c','hocr_char_boxes=1','-c','tessedit_create_hocr=1'],env={**os.environ,**TESS},capture_output=True)
    h=open(f+'.hocr').read(); lines=[]
    for lm in re.finditer(r"class='ocr_line'[^>]*title=\"bbox (\d+) (\d+) (\d+) (\d+)[^\"]*\"(.*?)</span>\s*</span>\s*(?=<span class='ocr_line'|</p>)",h,re.S):
        x0,y0,x1,y1=map(int,lm.groups()[:4])
        ch=[(int(c.group(1)),int(c.group(3)),c.group(5)) for c in re.finditer(r"x_bboxes (\d+) (\d+) (\d+) (\d+)[^>]*>([^<]*)<",lm.group(5))]
        lines.append((x0,y0,x1,y1,ch))
    return lines
def bars(a,L):
    s=(L[3]-L[0])/3; y0=int(L[0]-s*0.2); y1=int(L[3]+s*0.2)
    B=a[y0:y1]<140; col=B.sum(0); out=[]
    x=0; W=B.shape[1]
    while x<W:
        if col[x]>=1.3*s:
            x1=x
            while x1+1<W and col[x1+1]>=1.3*s: x1+=1
            if x1-x<=5:
                # extent of the vertical stroke
                R=staves.vrun(B[:,x:x1+1]); out.append([x,R.max()/s])
            x=x1+1
        else: x+=1
    # merge double bars
    m=[]
    for b in out:
        if m and b[0]-m[-1][0]<16: m[-1][2]=2; continue
        m.append([b[0],b[1],1])
    return m
def syllabify(text):
    r=subprocess.run(['node','-e','const P=require("/home/claude/build/site/js/psalm.js");process.stdout.write(JSON.stringify(P.syllabify(process.argv[1])))',text],capture_output=True,text=True)
    return json.loads(r.stdout)
G='abcdefghijklm'
def main():
    pi=int(sys.argv[1]); text=sys.argv[2]; args=sys.argv[3:]
    a=omr.page(pi); S=staves.find(a)
    want=key(text)
    # lyric line under each staff: OCR the band beneath it as one line
    lyr=[]
    for k,L in enumerate(S):
        s=(L[3]-L[0])/3; y0=int(L[3]+0.25*s); y1=int(L[3]+2.4*s)
        f='/tmp/om/l%04d_%d'%(pi,k)
        if not os.path.exists(f+'.hocr'):
            Image.fromarray(a[y0:y1]).save(f+'.png')
            subprocess.run(['tesseract',f+'.png',f,'-l','lat','--psm','7','-c','hocr_char_boxes=1','-c','tessedit_create_hocr=1'],env={**os.environ,**TESS},capture_output=True)
        h=open(f+'.hocr').read()
        lyr.append([(int(c.group(1)),int(c.group(3)),c.group(5)) for c in re.finditer(r"x_bboxes (\d+) (\d+) (\d+) (\d+)[^>]*>([^<]*)<",h)])
    # choose the staves: start where the lyric (minus 'Ant.') begins the antiphon
    st=None
    if '--staff' in args: st=int(args[args.index('--staff')+1])
    else:
        best=0
        for i,ch in enumerate(lyr):
            t0=key(''.join(c[2] for c in ch)); t=re.sub('^ant','',t0)
            if 'euouae' in t0 or 'euoua' in t0: continue
            r=difflib.SequenceMatcher(None,t[:12],want[:12]).ratio()+(0.3 if t0.startswith('ant') else 0)
            if r>best: best,st=r,i
    use=[st]; tot=len(re.sub('^ant','',key(''.join(c[2] for c in lyr[st]))))
    while tot<len(want)*0.85 and use[-1]+1<len(S):
        use.append(use[-1]+1); tot+=len(key(''.join(c[2] for c in lyr[use[-1]])))
    syl=syllabify(text)
    # target letters with syllable index
    tl=[]; 
    for si,sy in enumerate(syl):
        for c in key(sy): tl.append((c,si))
    # OCR letters across the staves used, with x and staff
    ol=[]
    for k in use:
        for x0,x1,c in lyr[k]:
            for ch in key(c): ol.append((ch,x0,k))
    if ol and ''.join(c for c,_,_ in ol[:3])=='ant': ol=ol[3:]
    sm=difflib.SequenceMatcher(None,''.join(c for c,_ in tl),''.join(c for c,_,_ in ol),autojunk=False)
    pos={}
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag=='equal':
            for d in range(i2-i1): pos[i1+d]=ol[j1+d][1:]
    sx=[]  # syllable start (staff, x)
    for si in range(len(syl)):
        idx=[i for i,(c,s2) in enumerate(tl) if s2==si]
        p=next((pos[i] for i in idx if i in pos),None)
        sx.append(p)
    # fill gaps by interpolation within the same staff
    for i in range(len(sx)):
        if sx[i] is None:
            prev=next((sx[j] for j in range(i-1,-1,-1) if sx[j]),None); nxt=next((sx[j] for j in range(i+1,len(sx)) if sx[j]),None)
            if prev and nxt and prev[1]==nxt[1]: sx[i]=((prev[0]+nxt[0])//2,prev[1])
            elif prev: sx[i]=(prev[0]+25,prev[1])
            else: sx[i]=(nxt[0]-25,nxt[1])
    out=[]; clefs=[]
    for k in use:
        L=S[k]; s=(L[3]-L[0])/3
        notes=staves.read(a,L)
        bs=bars(a,L)
        row=(a[int(L[0])-1:int(L[0])+2]<170).any(0); sl=int(np.argmax(row))
        left=sl+int(1.3*s)
        cl=[n for n in notes if n[0]<left and -1<=n[2]<=8]
        notes=[n for n in notes if n[0]>=left and -1<=n[2]<=8]
        right0=len(row)-int(np.argmax(row[::-1]))
        if k!=use[-1] and notes and notes[-1][1]<=s*0.32: notes=notes[:-1]   # the custos
        right=len(row)-int(np.argmax(row[::-1]))
        bs=[b for b in bs if (b[0]<right-18 or b[2]==2) and b[0]>left and all(abs(b[0]-n[0])>14 and abs(b[0]-(n[0]+n[1]))>6 for n in notes)]
        # clef: c clef = two heads straddling a line
        clef='c4'
        if len(cl)>=2:
            ps=sorted(set(p for _,_,p in cl),reverse=True)
            mid=(ps[0]+ps[1])/2 if len(ps)>1 else ps[0]
            line=int(round(mid/2))+1
            clef=('f' if len(ps)>2 else 'c')+str(line)
        if '--clef' in args: clef=args[args.index('--clef')+1]
        clefs.append(clef)
        base={'c4':3,'c3':5,'c2':7,'c1':9,'f4':0,'f3':2,'f2':4}[clef]
        mine=[(i,x) for i,(x,st2) in enumerate(sx) if st2==k]
        def owner(x):
            o=None
            for i,sxx in mine:
                if sxx<=x+10: o=i
            return o if o is not None else (mine[0][0] if mine else None)
        ev=[('n',x,G[base+p] if 0<=base+p<13 else '?',owner(x),w) for x,w,p in notes]
        def bowner(x):
            pre=[e for e in ev if e[1]<x]
            return pre[-1][3] if pre else owner(x)
        ev+=[('b',x,(h,d),bowner(x)) for x,h,d in bs if x>left]
        ev.sort(key=lambda e:e[1])
        while ev and ev[0][0]=='b': ev.pop(0)
        if k==use[-1] and mine:
            lastx=mine[-1][1]
            dbl=[e for e in ev if e[0]=='b' and e[2][1]==2 and e[1]>lastx]
            if dbl: ev=[e for e in ev if e[1]<=dbl[0][1]]
        if k!=use[-1]:
            while ev and ev[-1][0]=='b' and ev[-1][2][1]!=2: ev.pop()
        out.append((clef,ev,mine))
    # assemble gabc
    g='('+clefs[0]+') '; done=set(); lastclef=clefs[0]
    for (clef,ev,mine) in out:
        if clef!=lastclef: g+='('+clef+') '; lastclef=clef
        bysyl={}
        for e in ev: bysyl.setdefault(e[3],[]).append(e)
        for i,_ in mine:
            if i in done: continue
            done.add(i)
            evs=bysyl.get(i,[])
            nn=[e for e in evs if e[0]=='n']; ns=''
            for j,e in enumerate(nn):
                # small descending heads after a higher note: inclinata (diamonds)
                if j and e[4]<s*0.38 and e[2]<nn[j-1][2] and (ns[-1:].isupper() or nn[j-1][4]>=s*0.38): ns+=e[2].upper()
                else: ns+=e[2]
            g+=(' ' if syl[i].startswith(' ') else '')+syl[i].strip()+'('+ns+')'+(' ' if syl[i].endswith(' ') or i==len(syl)-1 else '')
            for e in evs:
                if e[0]=='b':
                    h,d=e[2]; g+=' ('+('::' if d==2 else ':' if h>2.6 else ';')+') '
    g=re.sub(r'\s+',' ',g).strip()
    rank={';':1,':':2,'::':3}
    def coll(m):
        bs=re.findall(r'\((::|:|;)\)',m.group(0)); return '('+max(bs,key=lambda b:rank[b])+')'
    g=re.sub(r'(?:\((?:::|:|;)\)\s*){2,}',lambda m:coll(m)+' ',g).strip()
    g=re.sub(r'\((?:::|:|;)\)$','(::)',g)
    if not g.endswith('(::)'): g+=' (::)'
    print(g)
    y0=int(S[use[0]][0]-3.5*32); y1=int(S[use[-1]][3]+2.8*32)
    Image.fromarray(a[y0:y1]).save('/tmp/om/crop.png')
if __name__=="__main__": main()
