"""Introits of two vigils from the Graduale O.P. (1950), transcribed by Andrew Hinkley (GitHub innocentop/atelier,
graduale-tex/hinkley-drafts, commit b2818bb; copies in tools/g50/hinkley/). Their pages were checked against the OCR of the
Graduale (tools/g50/ocr.tgz): p. 571 In Vigilia S. Matthaei, Officium Ego autem, sicut oliva; p. 607 In Vigilia Omnium
Sanctorum, Officium Timete Dominum. Hinkley's transcriptions of nine chants the site already read from the scan agree with
ours note for note to 97-100%. Run: python3 tools/g50/hinkley.py (idempotent)."""
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
NEW = {
  'S0920v': ('op-g50-ego-autem-oliva-in', 'in_ego_autem_sicut_oliva.gabc', 'Ego autem, sicut oliva', '571', 'In Vigilia S. Matthaei Apostoli', 'Missal p. 564'),
  'S1031v': ('op-g50-timete-in', 'in_timete.gabc', 'Timete Dominum', '607', 'In Vigilia Omnium Sanctorum', 'Missal p. 603'),
}
F = R + '/data/masses.js'
s = open(F, encoding='utf8').read(); head, js = s.split('var DOMINICAN = ', 1); D = json.loads(js.rstrip().rstrip(';'))
SP = R + '/tools/m39/new/spec_b6.json'; S = json.load(open(SP, encoding='utf8'))
spec = {x['key']: x for x in S} if isinstance(S, list) else S
for key, (cid, fn, inc, pg, occ, mp) in NEW.items():
    body = open(H + '/hinkley/' + fn, encoding='utf8').read().split('%%', 1)[1].strip()
    mode = re.search(r'^mode:(.*?);', open(H + '/hinkley/' + fn, encoding='utf8').read(), re.M).group(1)
    mode = str({'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8}.get(mode.strip(), mode))
    open(R + '/gabc/%s.gabc' % cid, 'w', encoding='utf8').write(
        'name:%s;\noffice-part:Introitus;\nmode:%s;\nbook:Graduale O.P. (Suarez), 1950, p. %s (%s);\n'
        'transcriber:Andrew Hinkley (github.com/innocentop/atelier, graduale-tex/hinkley-drafts);\n%%%%\n%s\n' % (inc, mode, pg, occ, body))
    D['chants'][cid] = {'p': 'in', 'i': inc, 'pg': pg}
    m = D['masses'][key]
    m['parts'] = dict([('in', [{'id': cid, 'm39': 'G50'}])] + [(p, v) for p, v in m['parts'].items() if p != 'in'])
    if 'in' not in m['req']: m['req'] = ['in'] + m['req']
    if m.get('pending'):
        m['pending'].pop('in', None)
        if not m['pending']: del m['pending']
    m['note'] = re.sub(r'^The Introit .*? is not yet typeset: its page of the Graduale O\.P\. is still to be read\. ', '', m['note'])
    m['note'] = 'Introit: Graduale O.P. (1950) p. %s, transcribed by Andrew Hinkley. ' % pg + m['note'] if 'Hinkley' not in m['note'] else m['note']
    sp = spec[key]; sp['parts'] = dict([('in', [cid])] + [(p, v) for p, v in sp['parts'].items() if p != 'in'])
    sp['note'] = 'Introit: Graduale O.P. (1950) p. %s, transcribed by Andrew Hinkley.' % pg
    sp.pop('pending', None)
    print(key, cid)
open(F, 'w', encoding='utf8').write(head + 'var DOMINICAN = ' + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + ';\n')
json.dump(S, open(SP, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
