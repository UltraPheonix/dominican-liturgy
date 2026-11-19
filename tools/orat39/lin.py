"""Linear reading text of the Missale O.P. 1939 PDF: blocks ordered by column, drop caps joined.
Output m39lin.txt with '@@PAGE n' markers (pdf page index)."""
import fitz, re, sys
d=fitz.open('/home/claude/dl/missal/Missale OP 1939.pdf')
out=[]
for i in range(len(d)):
    pg=d[i]; W=pg.rect.width
    bl=[b for b in pg.get_text('blocks') if b[6]==0]
    # columns: x0 of blocks cluster; two printed pages per pdf page, two columns each
    cols={}
    for b in bl:
        x=b[0]
        k=min(range(4), key=lambda c: abs(x-[42,212,455,623][c]*W/800))
        cols.setdefault(k,[]).append(b)
    out.append('@@PAGE %d'%i)
    for k in sorted(cols):
        cb=sorted(cols[k], key=lambda b:(round(b[1]),b[0]))
        j=0
        while j<len(cb):
            t=cb[j][4]
            # a drop cap: a block ending in a single capital letter, followed by the block with the rest of the word
            m=re.search(r'\n([A-Z])\n?$', t)
            if m and j+1<len(cb):
                nxt=cb[j+1][4]
                t=t[:m.start()]+'\n'+m.group(1)+nxt.lstrip(); j+=1
            out.append(t.rstrip('\n'))
            j+=1
open('m39lin.txt','w').write('\n'.join(out))
