# Hand-checked readings (from the page images) built from the Vulgate verses + the Missal's own changes; writes tools/m33/fixes.json
import json, re, sys
R = '/home/claude/dominican-liturgy/'
def verses(lang, book, ranges):
    V = {}
    for l in open(R + 'bible/%s/%s.txt' % (lang, book), encoding='utf-8'):
        a = l.rstrip('\n').split('\t')
        if len(a) >= 3: V[(int(a[0]), int(a[1]))] = ' '.join(a[2:])
    return ' '.join(V[(c, v)] for c, a, b in ranges for v in range(a, b + 1))
O = json.load(open('/home/claude/m33/readings33b.json'))
T = {}   # titles as the program writes them, by (type, book)
for v in O.values():
    for r in v['readings']: T.setdefault((r['type'], r['ref'].rsplit(' ', 1)[0].split(' ')[0] if False else re.sub(r'\s[\d:, -]+$', '', r['ref'])), (r['title'], r['title_en']))
def rd(typ, book, ranges, p33, pre=('', ''), la_subs=(), en_subs=(), title=None):
    la = verses('la', book, ranges); en = verses('en', book, ranges)
    for a, b in la_subs: la = re.sub(a, b, la, count=1)
    for a, b in en_subs: en = re.sub(a, b, en, count=1)
    if pre[0]: la = pre[0] + ': ' + la[0].upper() + la[1:]; en = pre[1] + ': ' + en
    la = re.sub(r'[,;:]\s*$', '.', la.strip())
    ref = book + ' ' + ', '.join('%d: %d-%d' % (c, a, b) if a != b else '%d: %d' % (c, a) for c, a, b in ranges)
    t = title or T.get((typ, book)) or ('', '')
    return {'type': typ, 'ref': ref, 'title': t[0], 'title_en': t[1], 'la': la, 'en': en, 'p33': p33}
F = {}
F['Dec24'] = [rd('Lesson', 'Isaias', [(62, 1, 4)], 61, ('Hæc dicit Dóminus Deus', 'Thus saith the Lord God'), [(r': et terra tua inhabitábitur\.?$', '.')], [(r' and thy land shall be inhabited\.?$', '')]),
              rd('Epistle', 'Ad Romanos', [(1, 1, 6)], 61, la_subs=[(r'vocáti Jesu Christi:?\s*$', 'vocáti Jesu Christi Dómini nostri.')]),
              rd('Gospel', 'Matthæus', [(1, 18, 21)], 61, la_subs=[(r'(?i)^Christi autem generátio sic erat: Cum esset desponsáta mater ejus María Joseph', 'Cum esset desponsáta mater Jesu María Joseph')],
                 en_subs=[(r'^Now the generation of Christ was in this wise\. When as his mother Mary was espoused to Joseph', 'When as Mary the mother of Jesus was espoused to Joseph')])]
F['Dec25_1'] = [x for x in O['Dec25_1']['readings'] if x['type'] == 'Lesson'] + [
    rd('Epistle', 'Ad Titum', [(2, 11, 15)], 64, ('Caríssime', 'Dearly beloved'), [(r'^Appáruit enim', 'Appáruit'), (r'Hæc lóquere, et exhortáre, et árgue.*$', 'Hæc lóquere, et exhortáre: In Christo Jesu Dómino nostro.')],
       [(r'^For the grace', 'The grace'), (r'These things speak, and exhort and rebuke.*$', 'These things speak, and exhort: in Christ Jesus our Lord.')]),
    rd('Gospel', 'Lucas', [(2, 1, 14)], 65, ('In illo témpore', 'At that time'), [(r'^Factum est autem in diébus illis, [eé]xiit', 'Exiit')], [(r'^And it came to pass, that in those days there went out', 'There went out')])]
F['Jan1'] = [dict(F['Dec25_1'][1], p33=73)] + [x for x in O['Jan1']['readings'] if x['type'] == 'Gospel']
F['Dec25_3'] = [rd('Lesson', 'Isaias', [(52, 6, 10)], 68, ('Hæc dicit Dóminus', 'Thus saith the Lord')),
                rd('Epistle', 'Ad Hebræos', [(1, 1, 12)], 68),
                rd('Gospel', 'Joannes', [(1, 1, 14)], 69, title=('Inítium sancti Evangélii secúndum Joánnem.', 'The beginning of the holy Gospel according to John.'))]
F['Jan5a'] = [rd('Epistle', 'Ad Galatas', [(4, 1, 7)], 75, ('Fratres', 'Brethren'), [(r'^Dico autem: [Qq]uanto', 'Quanto')], [(r'^Now I say, ', '')]),
              rd('Gospel', 'Matthæus', [(2, 19, 23)], 75, ('In illo témpore', 'At that time'), [(r'^Defúncto autem', 'Defúncto')], [(r'^But when Herod was dead', 'When Herod was dead')])]
F['Epi1'] = [x for x in O['Epi1']['readings'] if x['type'] != 'Gospel'] + [
    rd('Gospel', 'Lucas', [(2, 42, 52)], 81, la_subs=[(r'^Et cum factus esset annórum duódecim', 'Cum factus esset Jesus annórum duódecim')], en_subs=[(r'^And when he was twelve years old', 'When Jesus was twelve years old')])]
for k, v in F.items():
    for r in v: r.pop('flag', None); r.pop('first', None)
json.dump(F, open(R + 'tools/m33/fixes.json', 'w'), ensure_ascii=False, indent=1)
for k, v in F.items():
    for r in v: print(k, r['type'], r['ref'], '|', r['title'], '|', r['la'][:70], '...', r['la'][-40:], '|', r['en'][:50])
