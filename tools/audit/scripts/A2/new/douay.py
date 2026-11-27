def verses(lang,book,ch,a,b):
    out=[]
    for l in open(f'/home/claude/dominican-liturgy/bible/{lang}/{book}.txt',encoding='utf8'):
        p=l.rstrip('\n').split('\t')
        if int(p[0])==ch and a<=int(p[1])<=b: out.append(p[2])
    return out
def dr(book,ch,a,b,subs=()):
    s=' '.join(verses('en',book,ch,a,b))
    for x,y in subs:
        assert s.count(x)==1,(x,s.count(x)); s=s.replace(x,y)
    return s
