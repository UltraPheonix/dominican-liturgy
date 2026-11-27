"""Add the Latin conclusion the Missale O.P. (1939) prints to the orations that lacked it (each checked in m39lin.txt:
'Per Dominum.' except S0705 pc 'Qui vivis et regnas.'); fixes Pent0w Secreta 'piis affectibus celebremus' (Missal p. 33232).
Idempotent: python3 tools/orat39/conclusions.py"""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = R + '/data/orations.js'
s = open(F, encoding='utf8').read(); i = s.index('{'); j = s.rstrip().rstrip(';').rindex('}') + 1; O = json.loads(s[i:j])
LC = 'Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
EC = 'through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'
QV = 'Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
QE = 'who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.'
ITEMS = [('Pasc0h', 'pc'), ('Pasc1', 'or'), ('Pasc1', 'se'), ('Pasc1', 'pc'), ('Pasc4', 'se'), ('Pasc5', 'or'), ('Litaniis', 'se'), ('Asc', 'pc'),
         ('Pent0m', 'se'), ('Pent0w', 'se'), ('Pent0w', 'pc'), ('Pent0s', 'se'), ('Pent0s', 'pc'), ('Pent2', 'se'), ('Pent4', 'or'),
         ('Pent6', 'se'), ('Pent7', 'or'), ('S0705', 'pc')]
O['Pent0w']['se'][0] = O['Pent0w']['se'][0].replace('piis efféctibus celebrámus', 'piis afféctibus celebrémus')
n = 0
for k, p in ITEMS:
    la, en = O[k][p][0].strip(), O[k][p][1].strip()
    lc, ec = (QV, QE) if k == 'S0705' else (LC, EC)
    if la.endswith(lc): continue
    la = la.rstrip('.:;, ') + ': ' + lc
    if en and not re.search(r'world without end\.?$', en):
        en = en.rstrip('.:;, ') + '; ' + ec
    O[k][p] = [la, en] + O[k][p][2:]; n += 1
e = O['S0705']['pc'][1]
O['S0705']['pc'][1] = e.replace('Through Jesus Christ, thy Son our Lord, Who liveth and reigneth with thee, in the unity of the Holy Ghost, God, world without end.',
                                'Who livest and reignest with God the Father, in the unity of the Holy Ghost, God, world without end.')
open(F, 'w', encoding='utf8').write(s[:i] + json.dumps(O, ensure_ascii=False) + s[j:])
print(n, 'conclusions added')
