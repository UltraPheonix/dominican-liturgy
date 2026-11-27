import re
from m39 import L
MON=['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
DIE=re.compile(r'^\s*Die\s+(\d\s?\d?)\s+([A-Z][a-z]+)')
dies=[]
for i,l in enumerate(L):
    m=DIE.match(l)
    if m and i>39000:
        d=int(m.group(1).replace(' ','')); mo=m.group(2)
        if mo in MON: dies.append((i,MON.index(mo),d))
def region(month,day):
    out=[]
    for n,(i,mo,d) in enumerate(dies):
        if mo==month and d==day:
            j=dies[n+1][0] if n+1<len(dies) else i+400
            out.append((i,j))
    return out
LAB=re.compile(r'^(Officium|Oratio|Lectio|Léctio|Sequentia|Graduale|Alleluia|Tractus|Offertorium|Secreta|Communio|Postcommunio|Praefatio|Credo|Missa|De |Memoria|Commemoratio|In Missis|Temp|Infra|Si |Et fit|Omnia|Reliqua|Cetera|Ut in|Quando|Extra|Pro |Evangelium|Epistola)|pag\.|Communi|\?P\.|TSt|Gr\.|^.\s*Sequentia|^\S\.\s*Ps')
def skeleton(i,j,full=False):
    out=[]
    for k in range(i,j):
        l=L[k]
        if l.startswith('@@'): out.append('   '+l); continue
        if full or LAB.search(l.strip()) or k<i+6:
            out.append('%6d %s'%(k+1,l.rstrip()))
    return out
