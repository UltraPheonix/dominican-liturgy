import sys,os
B='/home/claude/dominican-liturgy/bible/'
def verses(book,ch,v1,v2,lang='en'):
    out=[]
    for l in open(B+lang+'/'+book+'.txt',encoding='utf8'):
        p=l.rstrip('\n').split('\t')
        if len(p)<3: continue
        c,v=int(p[0]),int(p[1])
        if c==ch and v1<=v<=v2: out.append((v,p[2]))
    return out
if __name__=='__main__':
    b,ch,a,z=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])
    lang=sys.argv[5] if len(sys.argv)>5 else 'en'
    for v,t in verses(b,ch,a,z,lang): print(v,t)
