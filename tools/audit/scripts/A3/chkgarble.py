# list auto-skipped (garble) changes whose Missal side has punctuation absent from the site side
import sys,warnings,re; warnings.filterwarnings('ignore')
import batch
for key in sys.argv[1:]:
    for d in batch.analyse(key):
        if d.get('notfound'): continue
        for i,c in enumerate(d['ch']):
            if batch.garble(c):
                pm=re.findall(r'[:;,.!?]',c[2]); ps=re.findall(r'[:;,.!?]',c[1])
                if pm!=ps: print(d['fid'],i,c[:3])
