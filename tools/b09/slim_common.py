import sys, re; import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matins as M, commune as C
END=r'(?=Lectio [ivxj]+\.|In I+\. Nocturno|In Ii+\. Nocturno|In Iii\. Nocturno|Te Deum|Ad Benedíctus|Ad Laudes|Ante Laudes|Cánticum Te)'
def cut(m):
    seg=m.group(2); i=seg.find('*')
    if i<0: return m.group(1)+' […] '
    j=max(0,i-260); 
    k=max(seg.rfind(x,j,i) for x in ['1$.','ty.','l^.','R.','K ','I$.',']^','1$','R?.','F^.','It.'])
    if k>=0: j=k
    return m.group(1)+' […] '+seg[j:]
def slim(t):
    t=re.sub(r'(Psalmus [^.]{1,6}\.)(.{150,}?)(?=\s(?:\bA(?:na|ha|fia|tia|iia|ña)\.|Ad Benedíctus|Ad Magníficat|y\.|f\.|V\.|£\.|In I+\. Nocturno|Capitulum|Hymnus|Oratio))', r'\1 […]', t, flags=re.S)
    t=re.sub(r'(Lectio [ivxj]+\.)(.+?)'+END, cut, t, flags=re.S)
    return t
for name,a,b in C.COMMONS:
    if name in sys.argv[1:]:
        t=slim(M.text_range(a,b)); print('=====',name,len(t)); print(t)
