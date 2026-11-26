"""Parse the tesseract output of the M39 Kalendarium (pdf 9-13) into MMDD|title|rank lines for proofreading."""
import re,sys
MONTHS=['JANUARIUS','FEBRUARIUS','MARTIUS','APRILIS','MAJUS','JUNIUS','JULIUS','AUGUSTUS','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
RANK=r'(Totum Duplex(?: I+ classis)?|Duplex(?: majus)?|Semiduplex|Semid\.|Simplex|Memoria|3 Lectiones|9 Lectiones|Solemnissima|Solemnis|Simplex)'
files=sys.argv[1:]
m=0; day=None; out=[]
for f in files:
    started = f.endswith('9L.txt')==False
    for l in open(f):
        l=l.rstrip()
        u=re.sub(r'[^A-Z]','',l)
        if u in MONTHS: m=MONTHS.index(u)+1; started=True; continue
        if not started or m==0: continue
        if 'FESTA' in u: continue
        mm=re.search(r'(?<![\dA-Za-z])(\d{1,2})\s*[|\]}\)]?\s*\|?\s*([A-Z*S][^|]*)?$',l)
        # day numbers: the last integer before the title
        g=re.match(r'^.*?(\d{1,2})\s*[|\]}\)]\s*(.*)$',l) or re.match(r'^.*?\b(\d{1,2})\s*$',l)
        if g and 1<=int(g.group(1))<=31 and not re.search(r'Lectiones',l[:l.find(g.group(1))+3] if False else ''):
            day=int(g.group(1)); rest=g.group(2) if g.lastindex>=2 else ''
        else:
            rest=l.strip(' |:;\'",.’')
            if not rest or day is None: continue
        rest=rest.strip(' |')
        if rest: out.append('%02d%02d|%s'%(m,day,rest))
print('\n'.join(out))
