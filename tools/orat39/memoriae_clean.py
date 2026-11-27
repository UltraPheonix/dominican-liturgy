"""Clean and accent the Memoriae prayers read by memoriae.py; writes memoriae_la.json {md|title: {or,se,pc: Latin}}.
Manual corrections (read against the Missal's text where the OCR is damaged) in MEMO_FIX below."""
import json, re, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); os.chdir(H)
from accent import accent
d = json.load(open('memoriae_raw.json', encoding='utf8'))
MEMO_FIX = json.load(open('memoriae_fix.json', encoding='utf8')) if os.path.exists('memoriae_fix.json') else {}
OCR = [  # the Missal's text layer: drop capitals split off, broken letters (read against the printed words)
 (r'^(Pr[^a-z ]{0,3}esta|PfUESTA|Fuesta|PRiESTA|Piuesta|Fgesta|PRxLSTA|F! jESTA|Presta|PRAESTA)\b', 'Praesta'),
 (r'^Pr/es I A\b', 'Praesta'), (r'^Ad esto\b', 'Adesto'), (r'tibi\. Domine', 'tibi, Domine'), (r'\bqusesumus\b', 'quaesumus'),
 (r'^H\.uc\b', 'Haec'), (r'\bDom ne\b', 'Domine'), (r'\(Per Dominum\.\)', 'Per Dominum.'), (r' et \d{2,3} (?=[A-Z])', ' et '),
 (r'^(QlLESUMUS|QUAiSUML S|Qua e s u m u s|Quaesum us)\b', 'Quaesumus'), (r'\bqujesumus\b', 'quaesumus'),
 (r'\bm ysteriis\b', 'mysteriis'), (r'natalltia', 'natalitia'), (r'Martlnae', 'Martinae'), (r'^Deu s\b', 'Deus'),
 (r'\bD ?eu ?s\b', 'Deus'), (r'^Eus, qui nos beati TheoD dori', 'Deus, qui nos beati Theodori'), (r'circumdas \^ et', 'circumdas et'),
 (r'^Exa udi', 'Exaudi'), (r'^Ho stias', 'Hostias'), (r'^(Sum ptis|Umptis)', 'Sumptis'), (r'^(Susc ipe|Sús c ip e|Su sc ipe|Sus c ip e)', 'Suscipe'),
 (r'^Refec ti', 'Refecti'), (r'^(R efecti|Efecti|efecti) cibo potuque (caeR lesti|caelesti|cae R lesti)', 'Refecti cibo potuque caelesti'),
 (r'^[Dd]juvet', 'Adjuvet'), (r'beMi', 'beati'), (r'^(Ai xiliem l r|Auxit\.tenti jr)', 'Auxilientur'),
 (r'^Umpsim u s, Domine, celeS britatis', 'Sumpsimus, Domine, celebritatis'), (r'^Ivini muneris largitate sad tiati', 'Divini muneris largitate satiati'),
 (r'^Atiasti Domine familiam S tuam', 'Satiasti Domine familiam tuam'), (r'^Slper', 'Super'), (r'^(HiEC|Hjeq|H\.EC|HAEC)\b', 'Haec'),
 (r'^Ostiarum nostrarum tibi, H Domine', 'Hostiarum nostrarum tibi, Domine'), (r'Salut\\ris', 'Salutaris'), (r'Ccelestis', 'caelestis'),
 (r'bea ii', 'beati'), (r'\btuse\b', 'tuae'), (r'in- \d+ terventione', 'interventione'), (r'jugi- \d+ ter', 'jugiter'), (r'Mar\d+ tyris', 'Martyris'),
 (r'exui matis', 'exui malis'), (r'^Dcmine', 'Domine'), (r'^C/elestem', 'Caelestem'), (r'^Sum psim us', 'Sumpsimus'),
 (r'^Aelesti alimonia refecti, C supplices', 'Caelesti alimonia refecti, supplices'), (r'Martvrum', 'Martyrum'), (r'commemorat one', 'commemoratione'),
 (r'^Ecc l e s ia m', 'Ecclesiam'), (r'quae\s+\d+\s+pro', 'quae pro'), (r'cujus \d+ solemnia', 'cujus solemnia'),
]
def clean(t):
    t = t.replace('­', '').replace('­', '')
    t = re.sub(r'\b([A-Z])\s+([A-Z]{2,})', r'\1\2', t)                 # "P ROTEGAT"
    t = re.sub(r'^((?:[A-Za-z] ){2,}[A-Za-z]+)', lambda m: m.group(1).replace(' ', ''), t)   # "Ec c l e s ia m"
    t = re.sub(r'^([A-Z][a-z]) ([a-z]{1,3}) ', r'\1\2 ', t)           # "De u s"
    t = re.sub(r'\s+([:;,.])', r'\1', t)
    w = t.split(' ', 1)
    if w[0].isupper() and len(w[0]) > 1: t = w[0].capitalize() + (' ' + w[1] if len(w) > 1 else '')
    for p_, r_ in OCR: t = re.sub(p_, r_, t, flags=re.I)
    t = re.sub(r'(Per Do?\s*-?\s*m?i?n?u?m\.?|Per Domi­?num\.?|Per Doninum\.?)\s*$', 'Per Dóminum.', t)
    t = re.sub(r'Per\s+eum\s*-?\s*dem[^.]*\.?\s*$', 'Per eúndem Dóminum.', t)
    t = re.sub(r'(?<=[a-z,;:]) \d{2,3} (?=[a-z])', ' ', t)          # page numbers in the running text
    t = re.sub(r'\s+', ' ', t).strip()
    return t
sys.path.insert(0, os.path.join(H, '..', 'addiv')); import fix as _fx
CON = {k: _fx.ispell(getattr(_fx, k)) for k in ('PD', 'PDS', 'PE', 'PES', 'QV', 'QT')}
O = json.loads(open('../../data/orations.js', encoding='utf8').read().split('=', 1)[1].strip().rstrip(';'))
AD = json.loads(open('../../data/addiv.js', encoding='utf8').read().split('=', 1)[1].strip().rstrip(';'))['sets']
WFIX = {'laetificent': 'lætíficent', 'contigimus': 'contígimus', 'sociarumque': 'sociarúmque', 'largiorem': 'largiórem',
        'supplicando': 'supplicándo', 'provocemur': 'provocémur', 'intendas': 'inténdas', 'Crispiniano': 'Crispiniáno',
        'Quintino': 'Quintíno', 'Britio': 'Brítio', 'Albino': 'Albíno', 'Quirico': 'Quírico', 'Christophoro': 'Christóphoro',
        'Cucuphate': 'Cucupháte', 'Nazario': 'Nazário', 'Cucuphátém': 'Cucuphátem', 'Euphemia': 'Euphémia', 'oratio': 'orátio',
        'Angelam': 'Ángelam', 'Angelæ': 'Ángelæ', 'repetita': 'repetíta', 'Crispino': 'Crispíno'}
def matched(x):
    if x.get('ratio', 0) < 0.995: return None
    m = x['match']
    if m.startswith('A:'): k, f = m[2:].split('.'); return AD[k][f]['la'] + ' ' + AD[k][f]['lc']
    k, f = m.split('.'); return O[k][f][0]
def conclude(la, kind):
    # cut at the Missal's short conclusion and write it out in full; nothing after it belongs to the prayer
    m = re.search(r'(Per Dóminum|Per eúndem|Qui vivis|Qui tecum|Dóminum nostrum I?J?esum Christum Fílium tuum\.? Qui tecum)', la)
    if not m:
        m2 = re.search(r'\(Per Dóminum\.\)', la)
        body = la[:m2.start()] if m2 else la
        body = body.rstrip(' .;:')
        if re.match(r'^Dómine Iesu Christe|^Dómine Jesu Christe', body): return body + ': ' + CON['QV'].replace('Qui', 'Qui', 1)
        return body + ('. ' if kind == 'se' else ': ') + CON['PD']
    body, s_ = la[:m.start()].rstrip(' :'), m.group(1)
    if s_.startswith('Dóminum nostrum'): return body + ' Dóminum nostrum Iesum Christum Fílium tuum: Qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
    c = {'Per Dóminum': 'PDS' if 'ejúsdem' in la[m.start():m.start() + 120] else 'PD', 'Per eúndem': 'PE', 'Qui vivis': 'QV', 'Qui tecum': 'QT'}[s_]
    sep = '' if kind != 'or' or body.endswith(('.', ':')) else ':'
    return body.rstrip('.') + ('.' if kind == 'se' else ':') + ' ' + CON[c]
out = {}; rep = []
for k, v in d.items():
    out[k] = {}
    for f, x in v.items():
        key = k + '|' + f
        if key in MEMO_FIX: out[k][f] = MEMO_FIX[key]; continue
        mt = matched(x)
        if mt: out[k][f] = mt; continue
        la, unk = accent(clean(x['t']))
        la = la[0].upper() + la[1:]
        for w_, r_ in WFIX.items(): la = re.sub(r'\b%s\b' % w_, r_, la)
        unk = [u for u in unk if u not in WFIX]
        la = conclude(la, f)
        la = _fx.ispell(la) if hasattr(_fx, 'ispell') else la
        out[k][f] = la
        if unk: rep.append((key, unk, la))
json.dump(out, open('memoriae_la.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for r in rep: print(r[0], r[1], '\n   ', r[2])
print(len(rep), 'to check')
