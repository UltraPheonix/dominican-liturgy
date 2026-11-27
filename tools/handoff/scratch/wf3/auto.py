import json, re, sys
S = {r['date']: r for r in json.load(open('/tmp/wf3/site44.json'))}
O = json.load(open('/home/claude/dominican-liturgy/tools/ordo44/ordo1944b.json'))
def sq(t): return re.sub(r'(?<=\b\w) (?=\w\b)', '', re.sub(r'[ \t]+', ' ', t))
PF = [(r'Praef\.?\s*(de\s+)?Nat', 'Nativitate'), (r'Praef\.?\s*(de\s+)?Trin', 'SS. Trinitate'), (r'Praef\.?\s*(de\s+)?Apost', 'Apostolis'),
      (r'Praef\.?\s*(de\s+)?comm', 'Communis'), (r'Praef\.?\s*(de\s+)?Quadr', 'Quadragesima'), (r'Praef\.?\s*(de\s+)?(S\.\s*)?Cruc', 'Sancta Cruce'),
      (r'Praef\.?\s*(de\s+)?Pasch', 'Paschalis'), (r'Praef\.?\s*(de\s+)?Ascens', 'Ascensione'), (r'Praef\.?\s*(de\s+)?Spir', 'Spiritu Sancto'),
      (r'Praef\.?\s*(de\s+)?(В|B)\.?\s*(М|M)\.?\s*(V|В)|Praef\.?\s*(de\s+)?B\.\s*V', 'B. Maria Virgine'), (r'Praef\.?\s*(de\s+)?(S\.\s*)?Jos', 'S. Ioseph'),
      (r'Praef\.?\s*(de\s+)?(S\.\s*P\.\s*N\.\s*)?Domin', 'Dominico'), (r'Praef\.?\s*(de\s+)?Epiph|Praef\.? et Communic\.? (de )?oct', 'Epiphania?'),
      (r'Praef\.?\s*(de\s+)?(SS\.\s*)?Cord', 'Corde Iesu'), (r'Praef\.?\s*(de\s+)?Defunct', 'Defunctorum'), (r'Praef\.?\s*(de\s+)?S\.\s*Franc', 'Francisco'),
      (r'Praef\.?\s*(de\s+)?(D\.\s*N\.\s*J|Chr)', 'D. N. Iesu Christo')]
COL = {'Alb': 'white', 'Rb': 'red', 'Vr': 'green', 'Vl': 'violet', 'VI': 'violet', 'Nr': 'black', 'Rs': 'rose'}
for o in O:
    d = o['date']; t = sq(o.get('text') or '')
    if not t or d not in S: continue
    s = S[d]; m0 = s['masses'][0] if s['masses'] else {}
    lines = t.split('\n')
    # colour: a colour word at the end of one of the first 2 lines
    col = None
    for l in lines[:3]:
        mm = re.search(r'\b(Alb|Rb|Vr|Vl|VI|Nr|Rs)\.?\s*-?$', l.strip())
        if mm: col = COL[mm.group(1)]; break
    msg = []
    if col and m0 and m0.get('color') != col: msg.append('colour Ordo %s site %s' % (col, m0.get('color')))
    mass = ' '.join(l for l in lines if re.search(r'Missa|In M\.|Praef|Credo|Gloria|Or\.|Orat', l))
    for rx, nm in PF:
        if re.search(rx, mass):
            if nm.endswith('?'):
                continue
            if m0.get('pref') != nm and not any(m.get('pref') == nm for m in s['masses']): msg.append('Praef Ordo %s site %s' % (nm, [m.get('pref') for m in s['masses']]))
            break
    if re.search(r'(sine|absque)\s+Credo', mass):
        if m0.get('credo'): msg.append('Ordo sine Credo; site Credo (%s)' % m0['key'])
    elif re.search(r'Credo', mass) and not any(m.get('credo') for m in s['masses']): msg.append('Ordo Credo; site none')
    if re.search(r'sine\s+Gloria', mass) and m0.get('gloria'): msg.append('Ordo sine Gloria; site Gloria')
    if re.search(r'cum\s+Gloria', mass) and not m0.get('gloria'): msg.append('Ordo cum Gloria; site none')
    if msg: print(d, m0.get('key'), '|', '; '.join(msg))
