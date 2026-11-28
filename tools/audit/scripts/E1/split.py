import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import fitz, re, json, sys, warnings
warnings.filterwarnings('ignore')
import importlib.util
exec(open(os.path.join(D,'extract.py')).read().split('for pno in map')[0])
EN=set('the and of to you we that your our may us who which in be by with for his her is are o lord god through this those they he she them all which have has from as on'.split())
LA=set('et ut in nos qui quae quod tua tuam tuae tui nobis quaesumus domine deus per est ad cum sunt eius ejus te tibi atque ac dominum nostri nostrae nostra sicut non quia'.split())
def score(row):
    ws=re.findall(r'[a-z]+', ' '.join(o['t'] for o in row).lower())
    return sum(w in EN for w in ws)-sum(w in LA and w not in EN for w in ws)
def split(rows):
    # drop header rows
    body=[r for r in rows if r[0]['y']>24 or not (len(rows)>1)]
    s=[score(r) for r in body]
    best=(-1e9,len(body))
    for k in range(1,len(body)):
        gap=body[k][0]['y']-body[k-1][0]['y']
        if gap<14: continue
        v=sum(s[:k])-sum(s[k:])
        if v>best[0]: best=(v,k)
    k=best[1]
    return body[:k], body[k:], s, k
if __name__=='__main__':
    bad=0
    for pno in range(int(sys.argv[1]),int(sys.argv[2])):
        rows=rows_of(doc[pno]); e,l,s,k=split(rows)
        neg=sum(1 for x in s[:k] if x<0); pos=sum(1 for x in s[k:] if x>0)
        if neg>1 or pos>1 or not l or not e:
            bad+=1; print(pno, len(e), len(l), 'E-latin',neg,'L-eng',pos)
    print('bad',bad)
