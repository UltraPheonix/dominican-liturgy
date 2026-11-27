"""tools/m39/kalendar39.txt -> data/kalendar39.js (window.KAL39 = {MMDD: [[title, rank, massKey|null, note], ...]}).
Mass keys from k_map.py's matching, corrected by FIX below (checked by hand 2026-11-26); MISSING_MASSES.md lists the gaps."""
import json,subprocess
subprocess.run(['python3','tools/m39/k_map.py'],check=True,stdout=subprocess.DEVNULL)
rows=json.load(open('/tmp/x/krows.json')); S=json.load(open('/tmp/x/sitem.json'))
FIX={('0217','Reginaldi'):None,('0317','Patricii'):None,('0423','Georgii'):None,('0811','Octava S. P. N.'):None,
     ('0822','Octava Assumptionis'):None,('0901','Ægidii Abbatis'):None,('1125','Catharinæ Virg. et Mart.'):'S1125',
     ('1225','Nativitas'):'Dec25_1',('1229','Thomæ Ep.'):None,('0628','Vigilia SS. Petri'):'G502_3',('0106','Epiphania'):'Epi',
     ('0428','Pauli a Cruce'):'S0428',('0321','Benedicti Abbatis'):None,('0302','Henrici Susonis'):'S0215',('1119','Elisabeth'):'S1119',('1110','Anniversarium Omnium Fratrum'):'S1113',('1113','Patrocinium S. Thom'):'S0307',('0104','Octava SS. Innocentium'):'S1228',('0401','Stigmatum S. Catharin'):'S0430',('1022','Dedicatio propri'):'Dedicatio',('1029','Octava Dedicationis'):'Dedicatio',('0204','Anniversarium Patrum'):'S1113',('0712','Anniversarium sepultorum'):'S1113',('0905','Anniversarium Familiarum'):'S1113'}
import os
if os.path.exists('tools/m39/new/kfix.json'):   # feasts added from the Missal by tools/m39/new/add_masses.py
    FIX.update({tuple(k.split('|',1)):v for k,v in json.load(open('tools/m39/new/kfix.json')).items()})
SUPERSEDED={('0126','Margaritæ de Hungaria')}   # replaced by the 1943 supplement (S. Margarita, 19 Jan)
K={};miss=[]
for d,t,r,note,key in rows:
    if any(d==a and b in t for a,b in SUPERSEDED): continue
    for (a,b),v in FIX.items():
        if d==a and b in t: key=v
    K.setdefault(d,[]).append([t,r,key,note])
    if key is None and r not in ('Memoria','Vigilia') and not r.startswith('Octava'): miss.append((d,t,r))
open('data/kalendar39.js','w').write('// Missale O.P. 1939, Kalendarium perpetuum (pp. 14-22) + supplements approved before 1955. Built by tools/m39/k_build.py.\n'
  '// MMDD: [[title, rank as printed, site Mass key or null, note]]\nwindow.KAL39 = '+json.dumps(K,ensure_ascii=False,separators=(',',':'))+';\n')
used={e[2] for v in K.values() for e in v if e[2]}
with open('tools/m39/MISSING_MASSES.md','w') as f:
    f.write('# 1939 calendar vs site Masses (tools/m39/k_build.py, %s entries)\n\n## Feasts of the 1939 calendar with no site Mass (%d)\n'%(sum(map(len,K.values())),len(miss)))
    f.write('These need their Mass from the Missale O.P. 1939 (own Mass or Common + proper orations).\n\n')
    for d,t,r in miss: f.write('- %s %s — %s\n'%(d,t,r))
    extra=[(k,m) for k,m in sorted(S.items()) if m.get('mo') is not None and m.get('d') and k not in used and not k.startswith('G')]
    f.write('\n## Site Masses with a date that are not in the 1939 calendar (%d)\n\n'%len(extra))
    for k,m in extra: f.write('- %s %s\n'%(k,m['t']))
print(len(K),'days;',len(miss),'missing Masses;',len(extra),'site Masses not in 1939')
