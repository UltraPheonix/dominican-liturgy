"""Matins lessons and responsories of the 1909 Proprium de Tempore from the OCR, repaired against the Vulgate (bible/la) and
Divinum Officium; -> lessons1909.json {daykey: [{'n', 'head', 'la', 'en', 'ref', 'src', 'resp': {...}}]}.
usage: python3 matins.py adv   (Advent: v1 pdf 246-283)"""
import json, os, re, sys, gzip
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import repair as R
OUT = os.path.join(HERE, 'lessons1909.json')
ROMAN = {'i': 1, 'j': 1, 'ii': 2, 'ij': 2, 'iii': 3, 'iij': 3, 'iv': 4, 'v': 5, 'vi': 6, 'vj': 6, 'vii': 7, 'viii': 8, 'viij': 8, 'ix': 9}
RM = r'(?:1\$|R\.|R\?\.?|R7\.?|ty\.|F\$\.|I£\.|l<f\.|Ry\.|fy\.|E£\.|Fy\.|\]£\.|l\^\.|R\\|Ff\.|I\?\.|If\.|ff\.|F\?\.|Rf\.|Rl|I\$\.|1\$|\$\.|l\$\.)'
def text_range(a, b):
    pages = gzip.open(os.path.join(HERE, 'text/v1.txt.gz'), 'rt').read().split('\f### ')[1:]
    out = []
    for pg in pages[a:b]:
        i, body = pg.split('\n', 1)
        cols = body.split('\n||\n')
        for c in cols:
            ls = [l.strip() for l in c.split('\n') if l.strip()]
            if ls and re.match(r'^[\W\dIVXLivxl]{0,6}\s*(DOMINICA|INFRA|IN |FERIA|SABBATO|De T|Adventus|ADVENTUS)', ls[0]): ls = ls[1:]   # running head
            out.append('\n'.join(ls))
    t = '\n'.join(out)
    t = re.sub(r'-\n(\S)', r'\1', t); t = re.sub(r'\s+', ' ', t)
    t = R.fix_ocr(t)
    t = re.sub(r'Lec\s?\.?tio', 'Lectio', t)
    t = re.sub(r'Lectio i v\.', 'Lectio iv.', t); t = re.sub(r'Lectio in\.', 'Lectio iii.', t); t = re.sub(r'Lectio (i|ii|iii)-\s', r'Lectio \1. ', t)
    return t
def split_resp(r):
    """'body * rep y. verse — rep [y. verse2 — rep] Gloria…' -> dict"""
    r = re.sub(r'\s+', ' ', r).strip()
    r = re.split(r'\s(?:Finita resumptione|T Quando|T Non dicitur|T In|Lectio sancti|In I+\.? Nocturno|In Ii+\. Nocturno|Ad Laudes)', r)[0]
    parts = re.split(r'\s(?:y|f|I|V|X|JF|jT|f\$|T-|If|\)T|I\*|\*v-|Y)\s?\.\s*(?:[ivx]+\.\s*)?', ' ' + r)
    body = parts[0].strip(); verses = []
    for p in parts[1:]:
        v = re.split(r'\s[—–-]\s|\s—', p)[0].strip()
        verses.append(v)
    gloria = 'Glória Patri' in r or 'Gloria Patri' in r or re.search(r'\bGlo ?ria\b|\bSória\b|\bG 16ria\b', r) is not None
    if '*' in body: a, b = body.split('*', 1)
    else: a, b = body, ''
    return {'a': a.strip(' :;,'), 'b': b.strip(' :;,'), 'v': verses, 'gloria': gloria}
def rep_line(t, kind):
    if not t: return t, False
    x = R.repair_do(t, kind, 0.7)
    if x: return x[0], True
    return t, False
def lesson_parts(t):
    """strip headings/closing; returns head, body, close"""
    head = []
    t = t.strip()
    t = re.sub(r'^\((?:vel [ivx]+\.?[^)]*|Lóngius[^)]*|Paulo post[^)]*|Post pauca[^)]*)\)\s*', '', t)
    for pat in (r'^(Incipit [^.]+\.)', r'^(De [A-ZÍ]\w+ Proph[^.]*\.)', r'^(Lectio sancti Evang[^.]*\.)', r'^(Cap\. [\w ,.]{1,12}?\.)'):
        m = re.match(pat, t)
        if m: head.append(m.group(1)); t = t[m.end():].strip()
    close = None
    m = re.search(r'\s((?:Hæc|Hasc|Hmc|I[li]ac|Ilæc|Ha\S?c|H\S{1,3}) dicit (?:Dóminus Deus|\.\.\.)[\s\S]*|(?:Hæc|Ha\S?c) dicit\s*\.*\s*$|Tu autem[\s\S]*|Convertímini ad me[\s\S]*)$', t)
    if m: close = 'tu' if m.group(1).startswith('Tu') else 'haec'; t = t[:m.start()]
    return head, t, close
RVAR = {1: 'j', 2: 'ii|ij', 3: 'iii|iij', 4: 'iv', 5: 'v', 6: 'vi|vj', 7: 'vii|vij', 8: 'viii|viij', 9: 'ix'}
def parse_day(chunk):
    """[(lesson n, lesson text, responsory text or None)]"""
    marks = [(m.start(), m.end(), ROMAN.get(m.group(1), 0)) for m in re.finditer(r'Lectio ([ivx]+)[\.\-/]\s?', chunk)]
    out = []
    for k, (s, e, n) in enumerate(marks):
        nxt = marks[k + 1][0] if k + 1 < len(marks) else len(chunk)
        x = chunk[e:nxt]
        m = re.search(r'(?:Hæc dicit|Hmc dicit|Tu autem)[^.]*?(?:\.\.\.|\.)(?:\s*\S{1,3}\.?\s*Deo gr[aá]tias\.)?', x)
        start = m.end() if m else int(len(x) * 0.3)
        r = re.search(r'(?:^|\s)\S{0,4}\s?(?:%s)\s?\.\s*(?=\S)' % RVAR.get(n, 'zz'), x[start:]) if n != 1 else (re.search(RM + r'\s*(?:i|j)\s?\.\s*(?=\S)', x[start:]) or re.search(r'^\s*\S{0,4}\s?(?:i|j)\s?[\.\-]\s+(?=[A-ZÁÉÍÓÚÆ])', x[start:]) or re.search(r'(?<=Deo gratias\.)\s+\S{0,4}\s?(?:i|j)\s?\.\s+(?=[A-ZÁÉÍÓÚÆ])', x[start:]) or re.search(r'\s(?:i|j)-\s+(?=[A-ZÁÉÍÓÚÆ])', x[start:]))
        if not r and len(RVAR.get(n, 'zz').split('|')[0]) > 1:
            r = re.search(r'(?:^|\s)\S{0,4}\s?(?:%s)\s+(?=[A-ZÁÉÍÓÚÆ])' % RVAR.get(n, 'zz'), x[start:])
        if r: out.append((n, x[:start + r.start()], x[start + r.end():]))
        else: out.append((n, x, None))
    return out
def build_lesson(n, t):
    head, body, close = lesson_parts(t)
    hom = re.search(r'\s((?:Homilía|Sermo|Ex Tractátu|Ex libro)[^.]*\.(?:\s*\([^)]*\))?)\s', ' ' + body + ' ')
    out = {'n': n, 'head': head, 'close': close}
    if hom:
        gosp = body[:hom.start()].strip(); out['homily_head'] = hom.group(1).strip(); body = body[hom.end() - 1:].strip()
        g = R.repair_do(gosp, 'lesson', 0.6)
        out['gospel'] = g[0] if g else gosp
        m2 = re.search(r'secúndum (\w+)', ' '.join(head)); out['evangelist'] = m2.group(1) if m2 else None
    sc = R.repair_scripture(body, 0.72) or (None if hom else R.repair_scripture(body, 0.5))
    if sc and not hom:
        out.update(la=sc[0], en=sc[1], ref=sc[2], src='vulgate %.2f' % sc[3]); return out
    d = R.repair_do(body, 'lesson', 0.65) or R.repair_do(body, 'lesson', 0.5)
    if d:
        out.update(la=d[0], src='DO %.2f %s' % (d[2], os.path.basename(d[1])))
        e = R.do_english(d[3], len(d[0].split()))
        if e: out['en'] = e
    else: out.update(la=body, src='OCR')
    return out
def build_resp(n, t):
    p = split_resp(t)
    whole = re.split(r'\sGl[oó] ?ria|\sSória|\sG 16ria', t)[0]
    d = R.repair_resp(whole, 0.8)
    if d and d['a'] and d['b']:
        vs = d['v']
        ob = [R.nb(w) for w in p['b'].split()][:2]; full = (d['a'] + ' ' + d['b']).split()
        if ob and ob[0]:
            for i in range(len(full) - 1):
                if R.nb(full[i]) == ob[0] and (len(ob) < 2 or R.nb(full[i + 1]) == ob[1]):
                    d['a'], d['b'] = ' '.join(full[:i]), ' '.join(full[i:]); d['b'] = d['b'][0].upper() + d['b'][1:]; break
        for extra in p['v'][len(vs):]:   # a Dominican verse not in the Roman responsory
            vs.append(rep_line(extra, 'resp')[0])
        return {'n': n, 'a': d['a'].rstrip(' :;,'), 'b': d['b'].rstrip(' :;,'), 'v': vs, 'gloria': p['gloria'], 'src': 'DO %.2f' % d['cov']}
    a, ok1 = rep_line(p['a'], 'resp'); b, ok2 = rep_line(p['b'], 'resp')
    vs = [rep_line(v, 'resp')[0] for v in p['v']]
    return {'n': n, 'a': a, 'b': b, 'v': vs, 'gloria': p['gloria'], 'src': 'part' if ok1 or ok2 else 'OCR'}
ADV_ANCHORS = [('adv1-0', r'Dominica I\. Adventus\. Ad Matutinum')] + \
    [('adv%d-%d' % (w, d), None) for w in (1,) for d in range(1, 7)]
def advent():
    t = text_range(246, 284)
    names = {1: 'Feria Secunda', 2: 'Feria Tertia', 3: 'Feria Quarta', 4: 'Feria Quinta', 5: 'Feria Sexta', 6: 'Sabbato'}
    seq = []
    for w in (1, 2, 3, 4):
        seq.append(('adv%d-0' % w, r'Dominica %s\. Adventus\.' % ['I', 'Ii', 'Iii', 'Iv'][w - 1]))
        for d in range(1, 7): seq.append(('adv%d-%d' % (w, d), r'(?:%s|%s)' % (names[d], names[d].upper().replace('FERIA', '1ERIA'))))
    seq.append(('vig-nat', r'In Vig\. Nativ'))
    pos, anchors = 0, []
    for k, pat in seq:
        best = None
        for m in re.finditer(pat, t[pos:], re.I):
            look = t[pos + m.end(): pos + m.end() + 400]
            if re.search(r'Lectio i\b|De Is\w* Proph|Incipit liber|Invitatorium|Lectio sancti', look): best = pos + m.start(); break
        if best is None: print('anchor not found', k); continue
        anchors.append((k, best)); pos = best + 10
    out = {}
    for i, (k, s) in enumerate(anchors):
        e = anchors[i + 1][1] if i + 1 < len(anchors) else len(t)
        chunk = t[s:e]
        cut = re.search(r'Ad Laudes|Ad Benedíctus', chunk)
        mat = chunk[:cut.start()] if cut and k.endswith('-0') else chunk[:cut.start()] if cut else chunk
        L = []
        for n, x, r in parse_day(mat):
            L.append(build_lesson(n, x))
            if r: L[-1]['resp'] = build_resp(n, r)
        out[k] = L
        print(k, len(L), [(x['n'], x['src'][:12], 'R' if 'resp' in x else '-') for x in L])
    return out
if __name__ == '__main__':
    D = json.load(open(OUT)) if os.path.exists(OUT) else {}
    if sys.argv[1] == 'adv': D.update(advent())
    json.dump(D, open(OUT, 'w'), ensure_ascii=False, indent=1)
