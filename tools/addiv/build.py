"""Build data/addiv.js: the Orationes ad diversa (nn. 1-38) and the Orationes ad supplendum numerum ternarium of the
Missale O.P. 1939, with English. Run: python3 tools/addiv/fix.py && python3 tools/addiv/tern.py && python3 tools/addiv/build.py"""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H)
from en import EN, TITLE_EN, DM
import fix
LA = json.load(open(H + '/la.json')); TR = json.load(open(H + '/tern_raw.json'))
CON = [(fix.PDS, 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.'),
       (fix.PD, 'Through our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'),
       (fix.PES, 'Through the same Jesus Christ, Your Son, our Lord, who lives and reigns with You in the unity of the same Holy Spirit, God, world without end.'),
       (fix.PE, 'Through the same Jesus Christ, Your Son, our Lord, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.'),
       (fix.QV, 'Who live and reign with God the Father, in the unity of the Holy Spirit, God, world without end.'),
       (fix.QT, 'Who lives and reigns with You in the unity of the Holy Spirit, God, world without end.')]
CON = [(fix.ispell(a), b) for a, b in CON]
NAT_OR = 'Dóminum nostrum Iesum Christum Fílium tuum: Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
def split(la):
    for c, e in CON:
        if la.endswith(c): return la[:-len(c)].rstrip(), c, e
    raise SystemExit('no conclusion: ' + la[-80:])
def prayer(la, en):
    src, en = (en if isinstance(en, tuple) else ('ai', en))
    b, c, e = split(la)
    return {'la': b, 'lc': c, 'en': en.rstrip(' .;:,'), 'ec': e, 's': src}
def title(t):
    t = t.replace('­ ', '').replace('­ ', '').replace(', aha', ', alia').replace('pcenit', 'pœnit')
    for a, b in [('Praelat', 'Prælat'), ('Praedicat', 'Prædicat'), ('Ecclesiae', 'Ecclesiæ'), ('terraemotus', 'terræmotus'), ('reliquiae', 'reliquiæ')]: t = t.replace(a, b)
    return t
S = {}
for x in LA:
    k = 'd%d' % x['n']
    S[k] = {'n': x['n'], 'la': title(x['title']), 'en': TITLE_EN[x['n']]}
    for i, kind in enumerate(('or', 'se', 'pc')): S[k][kind] = prayer(x[kind], EN[k][i])
    if x.get('note'): S[k]['note'] = x['note']
S['d2']['la'] = 'Alia Oratio ut supra (A cunctis)'
# the seasonal prayers that are not among the Orationes ad diversa
T = {'bvmAdv': ('De B. Maria V. (in Adventu)', 'Of Our Lady (Advent)'), 'bvmNat': ('De B. Maria V. (tempore Nativitatis)', 'Of Our Lady (Christmastide)'),
     'cruce': ('De Cruce (tempore Paschali)', 'Of the Cross (Paschaltide)')}
for k, (la, en) in T.items():
    t = dict(TR[k])
    if k == 'bvmNat':
        t['or'] = t['or'].rstrip('.') + ', ' + NAT_OR
        t['se'] = t['se'].replace('Muner ib u s', 'Munéribus') + ' ' + fix.ispell(fix.PD)
        t['pc'] = t['pc'].replace('Hiec', 'Hæc') + ' ' + fix.ispell(fix.PE)
    S[k] = {'la': la, 'en': en}
    for i, kind in enumerate(('or', 'se', 'pc')):
        if k == 'bvmNat' and kind == 'or':
            b = t['or'][:-len(NAT_OR)].rstrip(' ,'); S[k]['or'] = {'la': b + ',', 'lc': NAT_OR, 'en': EN[k][0][1], 'ec': 'our Lord Jesus Christ, Your Son, who lives and reigns with You in the unity of the Holy Spirit, God, world without end.', 's': DM, 'cont': 1}
        else: S[k][kind] = prayer(t[kind], EN[k][i])
# Of Our Lady through the year (Missale O.P. 1939, De sancta Maria in Sabbato III, A Purificatione usque ad Adventum,
# pp. 58*-59*): the commemoration of Our Lady on Saturdays when her Office is impeded (Breviarium 1924, Rubr. gen. § XXI.3;
# Missal p. 320, n. 3); in Advent the Advent prayer, from Christmas to the Purification that of Christmastide
PD = fix.ispell(fix.PD)
S['bvm'] = {'la': 'De B. Maria V. (a Purificatione usque ad Adventum)', 'en': 'Of Our Lady (through the year)'}
for kind, la, en in (
    ('or', 'Concéde nos fámulos tuos, quǽsumus Dómine Deus, perpétua mentis et córporis salúte gaudére: et gloriósa beátæ Maríæ semper Vírginis intercessióne, a præsénti liberári tristítia; et ætérna pérfrui lætítia: ' + PD,
     'Grant, we beseech You, O Lord God, that we Your servants may rejoice in lasting health of mind and body, and by the glorious intercession of blessed Mary ever Virgin be delivered from present sorrow and enjoy eternal gladness'),
    ('se', 'Tua, Dómine, propitiatióne, et beátæ Maríæ semper Vírginis intercessióne, ad perpétuam atque præséntem hæc oblátio nobis profíciat prosperitátem et pacem. ' + PD,
     'By Your mercy, O Lord, and the intercession of blessed Mary ever Virgin, may this offering profit us for prosperity and peace, now and for ever'),
    ('pc', 'Sumptis, Dómine, salútis nostræ subsídiis: da, quǽsumus, beátæ Maríæ semper Vírginis patrocíniis nos ubíque prótegi; in cuius veneratióne hæc tuæ obtúlimus maiestáti: ' + PD,
     'Having received, O Lord, the helps of our salvation, grant, we beseech You, that we may everywhere be protected by the patronage of blessed Mary ever Virgin, in whose honour we have offered these gifts to Your majesty')):
    S['bvm'][kind] = prayer(la, ('ai', en))
# Latin initials of the sets, for the lists
INC = {'bvm': 'Concéde nos fámulos', 'bvmAdv': 'Deus, qui de beátæ', 'bvmNat': 'Deus, qui salútis', 'cruce': 'Deus, qui pro nobis', 'd15': 'Deus, qui caritátis', 'd2': 'A cunctis', 'd6': 'Deus ómnium fidélium'}
for k, v in S.items(): v['inc'] = INC.get(k) or ' '.join(v['or']['la'].split()[:4]).rstrip(',:;')
out = 'window.ADDIV = ' + json.dumps({'src': 'Missale O.P. (1939): Orationes ad diversa, pp. 100*-113*; Orationes ad supplendum numerum ternarium, pp. 636-638; In Vigilia Epiphaniae, pp. 32-33',
                                      'sets': S}, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(R + '/data/addiv.js', 'w', encoding='utf8').write(out)
print(len(S), 'sets;', sum(1 for v in S.values() for kind in ('or', 'se', 'pc') if v[kind]['s'] == DM), 'prayers in the 1959 English;', len(out), 'bytes')
