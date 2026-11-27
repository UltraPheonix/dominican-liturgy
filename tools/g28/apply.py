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
# the 'inferred' chants the Graduale of 1928 names for the same Mass (tools/g28/confirmed.json)
C = json.load(open(H + '/confirmed.json', encoding='utf8'))
for k, ps in C.items():
    if k.startswith('_') or k not in D['masses']: continue
    for p, pg in ps.items():
        for x in D['masses'][k]['parts'].get(p, []):
            if isinstance(x, dict) and (x.get('inferred') or x.get('v28')): x.pop('inferred', None); x['v28'] = pg

# inferred chants corrected or confirmed from the Graduale of 1950/1928 and the Missal of 1939 (tools/g28/corrections.json)
K = json.load(open(H + '/corrections.json', encoding='utf8'))
for k, c in K.items():
    if k.startswith('_') or k not in D['masses']: continue
    m = D['masses'][k]
    for p in c.get('drop', []):
        m['parts'].pop(p, None)
        if p in m.get('req', []): m['req'].remove(p)
    for p, ids in c.get('set', {}).items():
        m['parts'][p] = [{'id': i, 'm39': 'G50', 'v50': c['src']} for i in ids]
        if p not in m.get('req', []): m.setdefault('req', []).append(p)
    if c.get('conf'): m['conf'] = c['conf']
    elif c.get('set') and k.startswith('S') and k[1:5].isdigit(): m['conf'] = 'g50'
    if c.get('page'): m['page'] = c['page']
    if c.get('note'): m['note'] = c['note']
    for p, pg in c.get('ok', {}).items():
        for x in m['parts'].get(p, []):
            if isinstance(x, dict) and (x.get('inferred') or x.get('v50')): x.pop('inferred', None); x['v50'] = 'G50 p. ' + pg
open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
