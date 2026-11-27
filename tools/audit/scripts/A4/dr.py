import re
B='/home/claude/dominican-liturgy/bible/en/'
def v(book,ch,a,b=None):
    b=b or a; out=[]
    for l in open(B+book+'.txt',encoding='utf8'):
        x=l.rstrip('\n').split('\t')
        if len(x)>=3 and int(x[0])==ch and a<=int(x[1])<=b: out.append(' '.join(x[2:]))
    return ' '.join(out)
