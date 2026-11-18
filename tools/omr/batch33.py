"""Find and read the Roman-fallback antiphons in the 1933 scan. -> cand33.json {key: {page, gabc, ratio}} and crops in /tmp/om/c_<key>.png"""
import json, re, glob, sys, io, contextlib, shutil, difflib
REDO=sys.argv[1:]
sys.argv=['x','0','x']
import read33
T={}
for e in json.load(open('/home/claude/build/gb/office_texts.json')):
    k=('hy' if e['kind']=='hy' else 'rb' if e['kind']=='rb' else 're' if e['kind']=='re' else '')+read33.key(e['t'].replace('*',''))
    T.setdefault(k,e['t'])
m=json.load(open('/home/claude/build/site/data/chant/office.json'))
R=[k for k,v in m.items() if len(v)>5 and v[5]=='R' and not k.startswith(('re','rb','hy'))]
pages={int(f[-8:-4]):read33.key(open(f).read()) for f in glob.glob('/home/claude/dl/op1933/ocr/*.txt')}
import os
out=json.load(open('cand33.json')) if os.path.exists('cand33.json') else {}
out={k:v for k,v in out.items() if v.get('q',0)>=0.85 and k not in REDO}
only=set(sys.argv[3:]) if False else None
for k in R:
    if k in out or (REDO and k not in REDO): continue
    t=T.get(k)
    if not t: print('no text',k); continue
    t=t.replace('* ','').replace('*','')
    # pages whose OCR holds a long stretch of the text
    sc=[]
    for p,P in pages.items():
        kk=k[:30]; r=difflib.SequenceMatcher(None,kk,P,autojunk=False).find_longest_match(0,len(kk),0,len(P)).size
        if r>=min(14,len(kk)-2): sc.append((r,p))
    sc.sort(reverse=True)
    best=None
    for r,p in sc[:4]:
        for pi in (p-1,p):
            buf=io.StringIO()
            sys.argv=['read33.py',str(pi),t]
            try:
                with contextlib.redirect_stdout(buf): read33.main()
            except Exception as e: continue
            g=buf.getvalue().strip()
            words=read33.key(re.sub(r'\([^)]*\)','',g))
            empty=len(re.findall(r'\(\)',g))
            q=difflib.SequenceMatcher(None,words,k).ratio()-0.05*empty
            if not best or q>best[0]:
                best=(q,pi,g); shutil.copy('/tmp/om/crop.png','/tmp/om/c_%s.png'%k[:40])
    if best and best[0]>=0.85:
        out[k]={'page':best[1],'gabc':best[2],'q':round(best[0],2),'t':t}
        print(k[:40],best[1],round(best[0],2),best[2][:150],flush=True)
    else: print('NOT FOUND',k,flush=True)
    json.dump(out,open('cand33.json','w'),ensure_ascii=False,indent=0)
