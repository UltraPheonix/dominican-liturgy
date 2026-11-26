"""Commune Sanctorum of the 1909 Breviary (vol. 1 pdf 1306-1432) -> communes1909.json: per Common, per Hour, an ordered list of items
('ant', text) ('ps', n | [n...]) ('cap', ref, text) ('hymn', text-or-incipit) ('vr', V, R) ('bened'/'magn'/'invit', text) and the
Matins lessons/responsories. Texts repaired with offices.fix_short / repair (the 1909 text decides)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import matins as M, offices as O
COMMONS = [('bvm', 1306, 1316), ('ded', 1316, 1331), ('apost', 1331, 1341), ('evang', 1341, 1343), ('mart_pont', 1343, 1355),
           ('mart', 1355, 1357), ('mm', 1357, 1373), ('conf_pont', 1373, 1384), ('doct', 1384, 1386), ('conf', 1386, 1390),
           ('abb', 1390, 1392), ('virg_mart', 1392, 1403), ('virg', 1403, 1406), ('mart_fem', 1406, 1409), ('nec', 1409, 1418),
           ('apost_tp', 1418, 1421), ('mart_tp', 1421, 1424), ('mm_tp', 1424, 1427), ('conf_tp', 1427, 1430), ('virg_tp', 1430, 1432)]
HOURS = [('vesp1', r'Ad [I1l]\.? Vesperas'), ('mat', r'Ad Matutinum'), ('laud', r'Ad Laudes'), ('prima', r'Ad Primam'), ('tertia', r'Ad Tertiam'),
         ('sexta', r'Ad Sextam'), ('nona', r'Ad Nonam'), ('vesp2', r'Ad (?:I[iI1l]\.?|Secundas) Vesperas'), ('compl', r'Ad Completorium')]
PSNAME = {'laudate pueri': 112, 'laudate dominum omnes': 116, 'dixit dominus': 109, 'confitebor': 110, 'beatus vir': 111, 'credidi': 115,
          'in convertendo': 125, 'nisi dominus': 126, 'domine probasti': 138, 'lauda jerusalem': 147, 'lauda anima': 145, 'laudate dominum quoniam': 146,
          'dominus regnavit': 92, 'jubilate': 99, 'deus deus meus': 62, 'benedicite': 210, 'laudate dominum de caelis': 148,
          'caeli enarrant': 18, 'domine dominus noster': 8, 'domini est terra': 23, 'eructavit': 44, 'deus noster refugium': 45, 'fundamenta': 86}
OCRD = str.maketrans({'l': '1', 'I': '1', 'i': '1', 'o': '0', 'O': '0', 's': '5', 'S': '5', 'a': '8', 'á': '8', 'z': '2', 'Z': '2', 'g': '9', 'q': '9'})
def psalms_from(txt):
    m = re.match(r'Psalmus\s+([\dlIioOsSaázZgq]{1,3}(?:\s[\dlIioOsSaázZgq])?)\s*[\.\*,]', txt)
    if m:
        x = m.group(1).replace(' ', '').translate(OCRD)
        if x.isdigit() and 1 <= int(x) <= 150: return [int(x)]
    low = O.R.nb(txt[:60])
    for k, v in PSNAME.items():
        if low.startswith(O.R.nb('Psalmus ' + k)) or O.R.nb(k) in low[:40]:
            if 'ceteris' in O.R.nb(txt) or 'céteris' in txt:
                seqs = {112: [112, 116, 145, 146, 147], 109: [109, 110, 111, 112, 113], 92: [92, 99, [62, 66], 210, [148, 149, 150]]}
                return seqs.get(v, [v])
            return [v]
    return None
def parse_common(t):
    pos = []
    for h, pat in HOURS:
        for m in re.finditer(pat, t): pos.append((m.start(), m.end(), h))
    pos.sort(); out = {}
    seen = set()
    for i, (s, e, h) in enumerate(pos):
        if h in seen and h != 'vesp2': continue
        seen.add(h)
        nx = pos[i + 1][0] if i + 1 < len(pos) else len(t)
        out[h] = items(t[e:nx], h)
        if h == 'laud':
            lm = re.search(r'^\s*\S{0,4}\s*Per Horas Antiphonae\.\s*(.+?)(?=Capitulum|Ad Benedíctus|Hymnus)', t[e:nx])
            if lm:
                parts = re.split(r'(?:^|\s)(?:[1lI2-5sS]|ii|iii|iv|v|f|fe|3|tf)\s?[\.\-]\s', ' ' + re.sub(r'Psalmus [^.]*?(?:pag\.\s*[\d\s]+\.?)', '', lm.group(1)))
                parts = [p for p in (O.clean(x) for x in parts) if len(p) > 8]
                out[h].insert(0, ['laudes', [O.fix_short(p) for p in parts[:5]]])
    return out
TOK = re.compile(r'(Super Psalm(?:os|um)(?: Laudum)?(?: sola)?\s*A\w{1,3}\.|Ad Benedíctus\s*A\w{1,3}\.|Ad Magníficat\s*A\w{1,3}\.|Invitatorium\.|\bA(?:na|ha|fia|tia|iia)\.|'
                 r'Psalmus\s+\d+\.|Psalmus\s+[A-ZÁÉÍÓÚ][^.]{2,40}\.(?:,? cum céteris)?|Ps\.\s+[A-ZÁÉÍÓÚ][^.]{2,40}\.|Capitulum\.|Hymnus\.|Hymnus\s+[A-ZÁÉÍÓÚ][^.]{2,40}\.|'
                 r'(?:^|\s)(?:y|f|V|I|X|T)\.\s|In I+\. Nocturno|In Iii?\. Nocturno|Oratio\.|Lectio [ivx]+\.)')
def items(t, hour):
    toks = [(m.start(), m.end(), m.group(1).strip()) for m in TOK.finditer(t)]
    out = []
    for k, (s, e, tag) in enumerate(toks):
        nx = toks[k + 1][0] if k + 1 < len(toks) else len(t)
        body = O.clean(t[e:nx])[:900]
        if tag.startswith(('Super Psalm', 'Ana', 'Aha', 'Afia', 'Atia', 'Aiia')):
            body = re.split(r'\s(?:Psalmus|\(Infra|In Advéntu|T )', ' ' + body)[0] if False else re.split(r'\s(?:\(Infra|Psalmus|T [A-Z])', body)[0]
            out.append(['ant1' if tag.startswith('Super') else 'ant', O.fix_short(O.clean(body))])
        elif tag.startswith('Ad Benedíctus'): out.append(['bened', O.fix_short(O.clean(re.split(r'\sCánticum|\sOratio', body)[0]))])
        elif tag.startswith('Ad Magníficat'): out.append(['magn', O.fix_short(O.clean(re.split(r'\sCánticum|\sOratio', body)[0]))])
        elif tag.startswith('Invitatorium'): out.append(['invit', O.fix_short(O.clean(re.split(r'\sPsalmus', body)[0]))])
        elif tag.startswith(('Psalmus', 'Ps.')):
            p = psalms_from(tag + ' ' + body[:80])
            if p: out.append(['ps', p])
        elif tag.startswith('Capitulum'):
            m = re.match(r'([^.]{1,20}\.\s*\d*\.?)\s*(.+)$', body)
            ref, txt = (m.group(1), m.group(2)) if m else ('', body)
            txt = re.split(r'\s(?:\S{1,3}\.\s*Deo grátias|R\.|Hymnus|1\$\.|l\^\.)', txt)[0]
            out.append(['cap', ref.strip(), O.fix_short(O.clean(txt), 0.6)])
        elif tag.startswith('Hymnus'):
            if tag == 'Hymnus.': out.append(['hymn', O.clean(re.split(r'\s(?:y|f|V)\.\s', body)[0])])
            else: out.append(['hymnref', O.clean(tag[7:])])
        elif re.match(r'^[yfVIXT]\.$', tag):
            m = re.match(r'(.+?[.!?])\s*\S{1,3}\.?\s*(.+?[.!?])', body)
            if m and len(m.group(1)) < 160: out.append(['vr', O.fix_short(m.group(1)), O.fix_short(m.group(2))])
        elif tag.startswith('In I') and 'Nocturno' in tag: out.append(['noct', tag])
    if hour == 'mat':
        L = []
        for n, x, r in M.parse_day(t):
            les = M.build_lesson(n, x)
            if r: les['resp'] = M.build_resp(n, r)
            L.append(les)
        if L: out.append(['lessons', L])
    return out
if __name__ == '__main__':
    D = {}
    for name, a, b in COMMONS:
        t = M.text_range(a, b)
        D[name] = parse_common(t)
        print(name, {h: [x[0] for x in v] for h, v in D[name].items()})
    json.dump(D, open(os.path.join(HERE, 'communes1909.json'), 'w'), ensure_ascii=False)
