import json,glob,re,sys,collections,unicodedata
root=sys.argv[1]
C=json.load(open(root+'/data/office1909/common.json'))
D=json.load(open('/tmp/b09/latdict2.json'))
def norm(w):
    w=unicodedata.normalize('NFD',w.lower()); w=''.join(c for c in w if unicodedata.category(c)!='Mn')
    return w.replace('j','i').replace('æ','ae').replace('œ','oe').replace('ë','e')
known=set(norm(k) for k in D)|set(norm(v) for v in D.values() if isinstance(v,str))
def txt(r):
    if isinstance(r,str): r=C.get(r,r)
    if isinstance(r,list): return r[0] if r else ''
    return str(r)
stats=collections.Counter(); bad=collections.Counter(); ex=collections.defaultdict(list)
prep=[];nn=[];empty=[]
for f in sorted(glob.glob(root+'/data/office1909/20*/*.json')):
    day=f[-15:-5]; d=json.load(open(f))
    for h,rows in d['h'].items():
        if not rows: empty.append((day,h))
        for r in rows:
            t=r[0] if isinstance(r,list) else r
            t=C.get(t,t) if isinstance(t,str) else t
            if isinstance(t,list): t=t[0]
            t=str(t); t=re.sub(r'</?c>','',t); t=re.sub(r'<n>.*?</n>',' ',t,flags=re.S); t=re.sub(r'<h>.*?</h>',' ',t,flags=re.S); t=re.sub(r'<[^>]+>',' ',t)
            if 'preparation' in t or 'praeparatione' in t: prep.append((day,h))
            m=re.search(r'.{0,40}\bN\.\s.{0,30}',t)
            if m and 'S. P. N.' not in m.group(0): nn.append((day,h,m.group(0).replace(chr(10),' ')))
            for w in re.findall(r"[A-Za-zÀ-ÿǽǼæœÆŒ]+",t):
                if len(w)<3: continue
                stats['w']+=1
                if norm(w) not in known:
                    bad[w]+=1
                    if len(ex[w])<2: ex[w].append(day+' '+h)
print('days',len(glob.glob(root+'/data/office1909/20*/*.json')),'words',stats['w'])
print('in-preparation rows',len(prep),'days',len(set(x[0] for x in prep)))
print('N. rows',len(nn),'days',len(set(x[0] for x in nn)), collections.Counter(x[2][-45:] for x in nn).most_common(8))
print('empty hours',len(empty),empty[:5])
print('unknown word types',len(bad),'tokens',sum(bad.values()))
for w,c in bad.most_common(int(sys.argv[2])): print(c,w,ex[w])
