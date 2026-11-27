"""Corrections from the review of the Graduale O.P. (1950) check (tools/g50/check_report.txt) against the Missale O.P. (1939).
- S. Margarita ab Hungaria (19 Jan.): her own Mass in the Graduale, pp. 398-399 (Officium Vultum tuum, pag. 571; Responsorium
  Unam petii, pag. 381; Alleluia Omnia detrimentum and Offertorium Praecepta Domini printed; Communio Simile est, pag. 48*;
  infra Septuag. Tractus Qui seminant, pag. 23*), as in the Missal's supplement; it had the Common of a Virgin (St Dominic Missal 1959).
- The Septuagesima Tracts of the Commons, as both books give them: Sacerdotes tui Desiderium (14*); Statuit, Justus ut palma,
  Os justi Beatus vir (9*); Loquebar, Gaudeamus (Virgin), Dilexisti Qui seminant (23*). And of the feasts that take those Masses
  whole and can fall after Septuagesima: S. Andreas Corsini (Statuit), S. Scholastica, BB. Sibyllina and Margarita de Castello
  (Gaudeamus of a Virgin: the Graduale gives the Common whole). The widows keep Veni sponsa (Common of a holy woman).
- S. Scholastica: the Tract Tu gloria (p. 422, of the Apparition of Our Lady on 11 Feb.) removed."""
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = R + '/data/masses.js'
s = open(F, encoding='utf8').read(); h, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
M = D['masses']; g = lambda *ids: [{'id': i, 'm39': True} for i in ids]
m = M['S0118']
m['parts'] = {'in': g('op-g50-vultum-tuum'), 'gr': g(4740), 'al': g(4858), 'of': g(6796), 'co': g(6271)}
m['season'] = {'lent': {'tr': g(4978)}}
m['conf'] = 'g50'; m['note'] = 'Chants as in the Graduale O.P. (1950), pp. 398-399.'; m.pop('extras', None)
for k, t in {'C30s': 6463, 'C32s': 7125, 'C39s': 7125, 'C42s': 7125, 'C45s': 4978, 'C51s': 4978, 'C55s': 4978}.items():
    M[k]['parts']['tr'] = g(t)
M['S0204']['parts'].pop('tr', None); M['S0204'].setdefault('season', {})['lent'] = {'tr': g(7125)}
M['S0210']['parts'].pop('tr', None)
for k in ('S0210', 'S0323b', 'S0413b'): M[k].setdefault('season', {})['lent'] = {'tr': g(4978)}
open(F, 'w', encoding='utf8').write(h + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('done')
