import fitz, json, statistics, collections
d=fitz.open('/home/claude/dl/missal/M39.pdf')
out=[]
for i in range(len(d)):
    pg=d[i]; W=pg.rect.width
    D=pg.get_text('dict')
    lines=[]
    for b in D['blocks']:
        if b['type']!=0: continue
        for l in b['lines']:
            ws=[]
            lines.append(l)
    if not lines: continue
    words=pg.get_text('words')
    # line keys
    byline=collections.defaultdict(list)
    for w in words: byline[(w[5],w[6])].append(w)
    L=list(byline.values())
    x0s=[min(w[0] for w in l) for l in L]
    rngs=[(0,.2),(.2,.45),(.45,.68),(.68,1.01)]
    starts=[]
    for a,b in rngs:
        xs=[round(x) for x in x0s if a*W<=x<b*W]
        if xs:
            c=collections.Counter(x//4 for x in xs).most_common(1)[0][0]*4
            starts.append(c)
        else: starts.append(a*W)
    def col(x):
        k=0
        for j,s in enumerate(starts):
            if x>=s-12: k=j
        return k
    hs=[w[3]-w[1] for w in words]; med=statistics.median(hs)
    cols=collections.defaultdict(list)
    for l in L:
        # split a line into columns by word x0 too (a pdf "line" may span columns)
        for w in l: cols[col(w[0]) if (w[3]-w[1])<1.6*med else col(w[0])].append(w)
    for k in sorted(cols):
        items=cols[k]
        def yk(w): return (w[1]+w[3])/2 if (w[3]-w[1])<1.6*med else w[1]+med*0.5
        items.sort(key=lambda w:(round(yk(w)/(med*0.8)), w[0]))
        for w in items:
            out.append([i,round(w[0],1),round(w[1],1),round(w[2],1),round(w[3],1),w[4],round((w[3]-w[1])/med,2)])
json.dump(out,open('/tmp/A1/stream.json','w'))
print(len(out))
