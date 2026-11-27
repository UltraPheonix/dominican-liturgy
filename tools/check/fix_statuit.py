"""Missale O.P. 1939, Commune unius Confessoris Pontificis (pp. 17*-19*): both Masses, Sacerdotes tui and Statuit, have the
Communio Beatus servus (Matth. 24); the Graduale O.P. 1950 likewise (Beatus servus, pag. 32*). The site's Common Statuit had
Fidelis servus (Luke 12), and the Masses copied from it. Fixed here for the Common and for every Mass that takes the Statuit
Mass whole (Missal or Graduale: "Missa Statuit, de Communi ..."); Masses with Fidelis servus printed as their own (S. Gregorii
Nazianzeni; and those marked m39, checked against the Missal) are left as they are."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = R + '/data/masses.js'
s = open(F, encoding='utf8').read(); h, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
KEYS = ['C32s', 'S0204', 'S0606', 'S0530b', 'S0803b', 'S0317', 'S0610b', 'S0622b', 'S0713b', 'S1001', 'S1117', 'S1023b', 'S0707b',
        'S0111b', 'S0303b', 'S0521b', 'S0907b']
n = 0
for k in KEYS:
    co = D['masses'][k]['parts'].get('co', [])
    if [x['id'] for x in co] == [6516] and not co[0].get('m39'):
        D['masses'][k]['parts']['co'] = [{'id': 5854, 'm39': True}]; n += 1
open(F, 'w', encoding='utf8').write(h + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(n, 'Masses: Communio Beatus servus')
