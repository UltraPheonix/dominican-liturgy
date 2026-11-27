"""Chants typeset from the Graduale O.P. (Paredes, 1928) -- the Graduale before 1944 -- for Masses whose chants the Graduale
of 1950 does not have. Each gabc was read note by note from the scan (tools/g28/*.gabc; note heads measured against the
local staff lines with a detector, neume shapes and syllables read by eye). Idempotent: python3 tools/g28/apply.py"""
import json, os, shutil
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
SETS = {
  'PurCordisBMV': {
    'parts': {'in': 'purcordis_in', 'gr': 'purcordis_gr', 'al': 5906, 'of': 'purcordis_of', 'co': 'purcordis_co'},
    'inc': {'in': ('Omnis gloria', '369'), 'gr': ('Nihil inquinatum', '369-370'), 'of': ('Quia fecisti', '371'), 'co': ('Sub umbra', '371')},
    'page': '369-371',
    'note': 'Graduale O.P. (1928), pp. 369-371: Officium Omnis gloria, Responsorium Nihil inquinatum, Offertorium Quia fecisti, '
            'Communio Sub umbra (typeset from the scan for this site); "Allelúia, V. Magníficat, ut in Visitatione B. M. V., die 2 Julii" '
            '(the Visitation Alleluia, Graduale O.P. 1950 p. 510). Missale O.P. (1939), pp. 316-318.'},
}
PN = {'in': 'in', 'gr': 'gr', 'of': 'of', 'co': 'co'}
F = R + '/data/masses.js'
s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
for key, S in SETS.items():
    m = D['masses'][key]; parts = {}
    for p, src in S['parts'].items():
        if isinstance(src, str):
            cid = 'op-g28-' + src.replace('_', '-')
            shutil.copy(H + '/' + src + '.gabc', R + '/gabc/' + cid + '.gabc')
            inc, pg = S['inc'][p]
            D['chants'][cid] = {'p': p, 'i': inc, 'pg': pg}
            parts[p] = [{'id': cid, 'm39': 'G28'}]
        else:
            parts[p] = [{'id': src, 'm39': 'G50'}]
    m['parts'] = parts; m['req'] = list(parts.keys())
    m.pop('pending', None)
    m['note'] = S['note']; m['page'] = S['page']; m['conf'] = 'g28'
    print(key, list(parts))
open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
