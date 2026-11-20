import json, re
from anchor import SITE
import readings as R
H = {int(k): v for k, v in json.load(open('headers.json')).items()}
MON = dict(zip('01 02 03 04 05 06 07 08 09 10 11 12'.split(), 'Januarii Februarii Martii Aprilis Maji Junii Julii Augusti Septembris Octobris Novembris Decembris'.split()))
ANCH = json.load(open('anchors.json'))
OUT = {}; bad = []
for k, a in ANCH.items():
    pg = R.L[a['line']][0]
    hd = H.get(pg, '') + ' / ' + H.get(pg + 1, '')
    if k.startswith('S') and len(k) >= 5:
        mm, dd = k[1:3], str(int(k[3:5]))
        if not (MON[mm][:4] in hd and ('(%s)' % dd in hd or '(%s ' % dd in hd)):
            bad.append((k, 'date', hd)); 
    rs = []
    for r in R.readings_of(k):
        al = R.align(R.join(r['body']))
        rs.append({'kind': r['kind'], 'head': r['head'], 'page': r['page'], 'al': al})
    OUT[k] = {'page': pg, 'hdr': hd, 'readings': rs}
json.dump(OUT, open('readings_raw.json', 'w'), ensure_ascii=False, default=list)
for b in bad: print(b)
print(len(bad))
