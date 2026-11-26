"""Corrections from the check against the Graduale O.P. (1950) sanctoral (tools/g50/check.py + the page images).
Each entry: Mass key -> parts as the Graduale assigns them (GregoBase source 14 ids), with the Graduale page as the tag.
Merged into tools/m33/propers_fix.json (so every rebuild keeps them) and applied with propers_apply.py.
Chants the site did not list yet are added from the GregoBase dump (gabc file + chants entry)."""
import json, os, sys, sqlite3
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, R + '/tools/m33')
import propers_apply
FIX = {
  'S0117': ({'gr': [4733]}, 'G50 p. 394: Responsorium Os justi, pag. 36*'),
  'S0120': ({'al': [6943]}, 'G50 p. 400: Alleluia V. Sancti tui (printed)'),
  'S0123': ({'al': [6833]}, 'G50 p. 402: Alleluia V. Optime pater (printed)'),
  'S0118_2': ({'gr': [5552]}, 'G50 p. 395: Responsorium Exaltent eum (printed)'),
  'S0719': ({'gr': [4733], 'al': [5359]}, 'G50 p. 522: Responsorium Os justi, pag. 36*; Alleluia V. Beatus vir qui timet, pag. 407'),
  'S0731': ({'gr': [7142]}, 'G50 p. 528: Missa Os justi, de Communi unius Conf. non Pont., pag. 42*'),
  'S0825': ({'gr': [7142]}, 'G50 p. 561: Responsorium Domine praevenisti, pag. 40*'),
  'S1226': ({'se': [4214]}, 'G50 p. 387: Sequentia Laetabundus, pag. 33'),
  'S1227': ({'in': [6549], 'se': [4214]}, 'G50 p. 388-389: Officium In medio, pag. 35*; Sequentia Laetabundus, pag. 33'),
  'S1228': ({'al': [5585]}, 'G50 p. 391-392: Alleluia V. Herodes (Hi sunt only on a Sunday and on the Octave)'),
  'S0430': ({'in': [7243]}, 'G50 p. 458: Officium Mihi adhaerere (printed)'),
  'S0502': ({'of': [5315]}, 'G50 p. 466: Missa In medio, pag. 35*, praeter Offertorium Meditabar (printed)'),
  'S0510': ({'of': [5315]}, 'G50 p. 474 / Missale O.P. 1939: Offertorium Meditabar (p. 466)'),
  'S0327': ({'gr': [5703], 'lent_tr': [6931]}, 'G50 p. 445*-446*: Responsorium Deus qui praecinxit; Tractus Persequar'),
  'S1028': ({'gr': [6863]}, 'G50 p. 606: III. Responsorium Nimis honorati sunt, pag. 4*'),
  'S1104': ({'gr': [6727], 'of': [7170]}, 'G50 p. 613: Responsorium Inveni David, pag. 12*; Offertorium Veritas mea, pag. 31*'),
}
# In medio of the Common of Doctors (p. 35*) in place of St Dominic's copy (p. 533), wherever the Graduale says pag. 35*
DOCT = ['S0127', 'S0129', 'S0209', 'S0223', 'S0307', 'S0404', 'S0405', 'S0411', 'S0421', 'S0527', 'S0618', 'S0714', 'S0820',
        'S0828', 'S1018', 'S1115', 'S1124', 'S1204', 'S0506']
for k in DOCT: FIX.setdefault(k, ({}, 'G50: Officium In medio, de Communi unius Doctoris, pag. 35*'))[0]['in'] = [6549]
F = R + '/data/masses.js'
s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
GB = sqlite3.connect(R + '/tools/gregobase/gb.sqlite')
PARTN = {'in': 'Introitus', 're': 'Graduale', 'gr': 'Graduale', 'al': 'Alleluia', 'tr': 'Tractus', 'se': 'Sequentia', 'of': 'Offertorium', 'co': 'Communio'}
def addchant(i):
    if str(i) in D['chants']: return
    r = GB.execute('select c.incipit,c."office-part",c.mode,c.gabc,c.transcriber,s.page from gregobase_chants c join gregobase_chant_sources s on s.chant_id=c.id where c.id=? and s.source=14', (i,)).fetchone()
    inc, p, mode, g, tr, pg = r; g = json.loads(g)
    open(R + '/gabc/%s.gabc' % i, 'w').write('name:%s;\noffice-part:%s;\nmode:%s;\nbook:Graduale O.P. (Suarez), 1950, p. %s;\ntranscriber:%s;\n%%%%\n%s\n' % (inc, PARTN.get(p, p), mode or '', pg, tr or '', g))
    D['chants'][str(i)] = {'p': p, 'i': inc, 'pg': pg}; print('added chant', i, inc)
PF = R + '/tools/m33/propers_fix.json'; PX = json.load(open(PF, encoding='utf8'))
for k, (parts, why) in FIX.items():
    for ids in parts.values():
        for i in ids: addchant(i)
    e = PX.setdefault(k, {}); e.update(parts); e['p39'] = why.split(':')[0]; e['_why_g50'] = why
json.dump(PX, open(PF, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
n = propers_apply.apply(D)
open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(len(FIX), 'Masses corrected;', n, 'parts set')
