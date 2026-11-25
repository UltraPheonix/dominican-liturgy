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

# ---- step 2 (2026-11-25): doubtful readings, each checked on the page image ----
JUNK = r'[a-zà-ÿæœǽ][A-ZÀ-ÞÆŒ]|[<>^|0-9]'
def okr(r): return 'weak' not in r.get('flag', []) and not re.search(JUNK, r['la']) and re.match(r'[A-ZÀ-ÞÆŒ]', r['la'])
def mass(k, fix=lambda r: None):
    """All readings of Mass k that pass the scan check; fix(r) may return a replacement for any reading."""
    out = []
    for r in (F[k] if k in F else O[k]['readings']):
        n = fix(r)
        if n: out.append(dict(n, p33=r['p33']))
        elif okr(r): out.append(r)
    out.sort(key=lambda r: r['type'] == 'Gospel')   # stable: lessons first
    F[k] = out
def subs(k, ref, *pairs):
    def f(r):
        if r['ref'] != ref: return None
        r = dict(r)
        for a, b in pairs: r['la'] = re.sub(a, b, r['la'], count=1)
        return r
    mass(k, f)
# drop caps split across the first word
subs('Quad4w', 'Isaias 1: 16-19', (r'LavaSecunda et tértia Orátio, Lavámini', 'Lavámini'))
subs('Quad4h', 'Regum 4 4: 25-38', (r'SunaSecunda et tértia Orátio, mitis', 'Sunamítis'))
subs('Pent0m', 'Joannes 3: 16-21', (r'NicoM demo', 'Nicodémo'))
subs('S0324', 'Isaias 7: 10-15', (r'DomiX ad', 'Dóminus ad'))
subs('S0325', 'Lucas 1: 26-38', (r'AngeX', 'Ángelus'))
F_s0325 = list(F['S0325'])
subs('S1208', 'Lucas 1: 26-28', (r'AngejjC', 'Ángelus'))
subs('S0424', 'Canticum Canticorum 3: 7-11, 4: 1, 8', (r'fordLL\. Ámbiunt', 'fortes ámbiunt'))
subs('S0921', 'Ezechiel 1: 10-14', (r"animaO' Jium", 'animálium'))
# Ecce sacerdos magnus (Eccli. 44 et 45), Commune Conf. Pont. M33 p. 16* (pdf 662) and the proper pages that repeat it
_E = [r for r in O['C32s']['readings'] if r['type'] == 'Lesson'][0]
ECCE = {'type': 'Lesson', 'ref': 'Ecclesiasticus 44: 16-27, 45: 3-20', 'title': _E['title'], 'title_en': _E['title_en'],
 'la': 'Ecce sacérdos magnus, qui in diébus suis plácuit Deo, et invéntus est justus: et in témpore iracúndiæ factus est reconciliátio. '
       'Non est invéntus símilis illi, qui conservávit legem Excélsi. Ideo jurejurándo fecit illum Dóminus créscere in plebem suam. '
       'Benedictiónem ómnium géntium dedit illi, et testaméntum suum confirmávit super caput ejus. Agnóvit eum in benedictiónibus suis: '
       'conservávit illi misericórdiam suam: et invénit grátiam coram óculis Dómini. Magnificávit eum in conspéctu regum: et dedit illi '
       'corónam glóriæ. Státuit illi testaméntum ætérnum, et dedit illi sacerdótium magnum: et beatificávit illum in glória. Fungi '
       'sacerdótio, et habére laudem in nómine ipsíus, et offérre illi incénsum dignum in odórem suavitátis.',
 'en': 'Behold a great priest, who in his days pleased God, and was found just: and in the time of wrath he was made a reconciliation. '
       'There was not found the like to him, who kept the law of the most High. Therefore by an oath the Lord made him to increase among '
       'his people. He gave him the blessing of all nations, and confirmed his covenant upon his head. He acknowledged him in his blessings: '
       'he preserved for him his mercy: and he found grace before the eyes of the Lord. He glorified him in the sight of kings: and gave him '
       'a crown of glory. He made an everlasting covenant with him, and gave him a great priesthood: and made him blessed in glory. To '
       'execute the office of the priesthood, and to have praise in his name, and to offer him a worthy incense for an odour of sweetness.'}
for k in 'C32s S0510 S0519 S0606 S1104 S1111 S1117 S0530b S0803b S1023b'.split():
    mass(k, lambda r: ECCE if r['type'] == 'Lesson' and r['ref'].startswith('Ecclesiasticus 44') else None)
F['S1126b'] = [dict(ECCE, p33=661), [r for r in O['C32s']['readings'] if r['type'] == 'Gospel'][0]]   # Bl. James of Benevento: Statuit
def one(k, typ, new):  # replace the reading(s) of this type that the scan could not give
    mass(k, lambda r: new if r['type'] == typ and not okr(r) else None)
one('Quad6t', 'Lesson', rd('Lesson', 'Jeremias', [(11, 18, 20)], 169, ('In diébus illis: Dixit Jeremías', 'In those days: Jeremias said'),
    [(r'^Tu autem Dómine demonstrásti', 'Dómine, demonstrásti')], [(r'^But thou, O Lord, hast', 'O Lord, thou hast')]))
one('S1102_3', 'Lesson', rd('Lesson', 'Apocalypsis', [(14, 13, 13)], 625, ('In diébus illis', 'In those days'), [(r'^Et audívi', 'Audívi')], [(r'^And I heard', 'I heard')]))
one('S1002', 'Lesson', rd('Lesson', 'Exodus', [(23, 20, 23)], 596, ('Hæc dicit Dóminus Deus', 'Thus saith the Lord God'),
    [(r'(Præcedétque te ángelus meus),.*$', r'\1.')], [(r'(And my angel shall go before thee),.*$', r'\1.')]))
one('S0914', 'Epistle', rd('Epistle', 'Ad Philippenses', [(2, 8, 11)], 580, ('Fratres', 'Brethren'),
    [(r'^Humiliávit semetípsum factus obédiens', 'Christus factus est pro nobis obédiens')], [(r'^He humbled himself, becoming obedient', 'Christ became for us obedient')]))
_g = rd('Gospel', 'Matthæus', [(24, 3, 13)], 586, ('In illo témpore', 'At that time'), [(r'^Sedénte autem eo', 'Sedénte Jesu')], [(r'^And when he was sitting', 'When Jesus was sitting')])
F['S0919'] = [rd('Epistle', 'Ad Hebræos', [(10, 32, 38)], 585, ('Fratres', 'Brethren'), [(r'(ex fide vivit):.*$', r'\1.')], [(r'(liveth by faith);.*$', r'\1.')]), _g]
F['G475'] = [rd('Lesson', 'Canticum Canticorum', [(3, 2, 5), (8, 6, 7)], 777)] + [r for r in O['G475']['readings'] if r['type'] == 'Gospel' and okr(r)]   # B. Imelda, suppl. p. 2
F['S0508'] = [rd('Lesson', 'Isaias', [(55, 1, 5)], 779),     # B.M.V. Mediatrix, suppl. p. 4 (dated 31 May there)
              rd('Gospel', 'Joannes', [(19, 25, 27)], 779, ('In illo témpore', 'At that time'), [(r'^Stabant autem', 'Stabant')], [(r'^Now there stood', 'There stood')])]
F['S1113'] = [dict(r, p33=738) for r in F.get('S1102_2') or O['S1102_2']['readings'] if okr(r)]   # In anniversario defunctorum, pro pluribus

subs('Quad4w', 'Ezechiel 36: 23-28', (r'Sanctijjj, sanctificábo', 'Sanctificábo'))
subs('5a', 'Ad Corinthios 1 13: 1-13', (r'Nun\] quam', 'Nunquam'))
for _k in ('EmbSatSept', 'EmbSatSeptS'): subs(_k, 'Ad Hebræos 9: 2-12', (r'sed ■A’ per', 'sed per'))
def _passion(r):   # Mark 14:5-8 lost in the scan (column break, M33 p. 169-170)
    if r['type'] != 'Gospel': return None
    r = dict(r, ref='Marcus 14: 1-72, 15: 1-46')
    r['la'] = r['la'].replace('Erant autem quidam indígne feréntes Amen dico vobis', verses('la', 'Marcus', [(14, 4, 8)]) + ' Amen dico vobis', 1).replace('(quia \\a erat', '(quia erat')
    r['en'] = r['en'].replace('Why was this waste of the ointment made? Amen, I say', 'Why was this waste of the ointment made? ' + verses('en', 'Marcus', [(14, 5, 8)]) + ' Amen, I say', 1)
    return r
_q = F['Quad6t']; F['Quad6t'] = [_passion(r) or r for r in _q]
# S0324 (S. Gabriel) took the Annunciation's first lesson (Isaias 7, M33 p. 454 = 25 Mar.)
_is7 = [r for r in F['S0324'] if r['ref'].startswith('Isaias 7')]
F['S0324'] = [r for r in F['S0324'] if not r['ref'].startswith('Isaias 7')]
F['S0325'] = _is7 + [r for r in F_s0325 if r['type'] == 'Gospel']

mass('S0519', lambda r: rd('Gospel', 'Matthæus', [(19, 27, 29)], 488, ('In illo témpore: Dixit Petrus ad Jesum', 'At that time: Peter said to Jesus'),
     [(r'^Tunc respóndens Petrus, dixit ei: ', '')], [(r'^Then Peter answering, said to him: ', '')]) if r['type'] == 'Gospel' else (ECCE if r['ref'].startswith('Ecclesiasticus 44') else None))
F['G475'] = F['G475'][:1] + [rd('Gospel', 'Joannes', [(6, 32, 37)], 778, ('In illo témpore: Dixit Jesus turbis Judæórum', 'At that time: Jesus said to the multitudes of the Jews'),
     [(r'^Dixit ergo eis Jesus: ', '')], [(r'^Then Jesus said to them: ', '')])]
F['S0919'][0]['la'] = F['S0919'][0]['la'].replace('Rememorámini autem prístinos', 'Rememorámini prístinos', 1)
F['S0919'][0]['en'] = re.sub(r'^Brethren: But call to mind', 'Brethren: Call to mind', F['S0919'][0]['en'])

# Quad1w: the lesson is 3 Reg. 19:3-8 (M33 p. 58-59; the scan merged "Ber-|sabée ... patres mei")
mass('Quad1w', lambda r: rd('Lesson', 'Regum 3', [(19, 3, 8)], 108, ('In diébus illis', 'In those days'),
     [(r'^Tímuit ergo Elías, et surgens ábiit quocúmque eum ferébat volúntas: venítque in', 'Venit Elías in')],
     [(r'^Then Elias was afraid, and rising up he went whithersoever he had a mind: and he came to', 'Elias came to')]) if r['ref'].startswith('Regum 3 19') else None)
G25 = rd('Gospel', 'Matthæus', [(25, 14, 23)], 661, ('In illo témpore: Dixit Jesus discípulis suis parábolam hanc', 'At that time: Jesus spoke this parable to his disciples'),
         [(r'^Sicut enim homo', 'Homo')], [(r'^For even as a man going into a far country, called', 'A man going into a far country called')])
# scan errors that recur (checked against the Vulgate vocabulary, tools: /tmp vocab check in HANDOFF)
GLOBAL = [(r'ZPtayi', 'Optávi'), (r'parábolam hanb ', 'parábolam hanc: '), (r'\blesus\b', 'Jesus'), (r'\bArnen\b', 'Amen'),
          (r'^Ómine Deus noster, Pasce', 'Dómine Deus noster, pasce'), (r'^Ómine Deus meus,? [Ee]xaltásti', 'Dómine Deus meus, exaltásti'),
          (r'Domiat,', 'Dóminus'), (r'Asgrotavit', 'Ægrotávit'), (r'discípulis silis', 'discípulis suis'), (r'adjesum', 'ad Jesum'),
          (r'^En edictio', 'Benedíctio'), (r'Designávit Domiti,', 'Designávit Dóminus'), (r'suffértis insiy ', 'suffértis '),
          (r'^Ómnibus réquiem', 'In ómnibus réquiem'), (r'Ave Rabbi\. -i\.j Jesus', 'Ave Rabbi. Et osculátus est eum. Dixítque illi Jesus'),
          (r'^Secúnda et tértia Orátio, diébus illis: Dixit Isaías: mine, Quis', 'In diébus illis: Dixit Isaías: Dómine, quis')]
def _g(r):
    if r['ref'] == 'Matthæus 25: 14-23' and 'discious' in r['la']: return dict(G25)
    if not any(re.search(a, r['la']) for a, b in GLOBAL): return None
    r = dict(r)
    for a, b in GLOBAL: r['la'] = re.sub(a, b, r['la'])
    return r
for _k in list(O):
    src = F[_k] if _k in F else O[_k]['readings']
    if any(_g(r) for r in src):
        if _k in F: F[_k] = [_g(r) or r for r in F[_k]]
        else: mass(_k, _g)

def _lk(r):   # Luke 23:23-32 lost at a column break (M33 p. 175)
    if not r['ref'].startswith('Lucas 22'): return None
    r = dict(r, ref='Lucas 22: 1-71, 23: 1-53')
    r['la'] = r['la'].replace('corrípiam ergo et latrónes', 'corrípiam ergo illum, et dimíttam. ' + verses('la', 'Lucas', [(23, 23, 32)]) +
                              ' Et postquam venérunt in locum, qui vocátur Calváriæ, ibi crucifixérunt eum: et latrónes', 1)
    r['en'] = r['en'].replace('and let him go. And when they were come', 'and let him go. ' + verses('en', 'Lucas', [(23, 23, 32)]) + ' And when they were come', 1)
    return r
F['Quad6w'] = [_lk(r) or r for r in (F['Quad6w'] if 'Quad6w' in F else O['Quad6w']['readings'])]

# whole verses lost at column/page breaks: rebuilt from the Vulgate with the Missal's opening (M33 pages checked)
def _whole(k, old, new):
    src = F[k] if k in F else O[k]['readings']
    F[k] = [dict(new, p33=r['p33'], title=r['title'], title_en=r['title_en']) if r['ref'] == old else r for r in src if r['ref'] == old or okr(r)]
_whole('Epi', 'Matthæus 2: 1-4, 10-12', rd('Gospel', 'Matthæus', [(2, 1, 12)], 0, la_subs=[(r'^Cum ergo natus', 'Cum natus')], en_subs=[(r'^When Jesus therefore was born', 'When Jesus was born')]))
_whole('Quad2s', 'Lucas 15: 11-13, 21-32', rd('Gospel', 'Lucas', [(15, 11, 32)], 0, ('In illo témpore: Dixit Jesus Pharisǽis, et Scribis parábolam istam', 'At that time: Jesus spoke to the Pharisees and Scribes this parable'),
       [(r'^Ait autem: Homo', 'Homo')], [(r'^And he said: A certain', 'A certain')]))
_whole('Quad4f', 'Joannes 11: 1-6, 8-45', rd('Gospel', 'Joannes', [(11, 1, 45)], 0, ('In illo témpore', 'At that time'), [(r'^Erat autem quidam', 'Erat quidam')], [(r'^Now there was', 'There was')]))
_whole('Quad6h', 'Ad Corinthios 1 11: 20-26, 29-32', rd('Epistle', 'Ad Corinthios 1', [(11, 20, 32)], 0, ('Fratres', 'Brethren'), [(r'^Conveniéntibus ergo vobis', 'Conveniéntibus vobis')]))

F['C76s'] = [dict(r) for r in O['C75s']['readings']]   # M33 p. 43*: Holy Spirit in Septuagesima, 'cetera ut supra'
for k, v in F.items():
    for r in v: r.pop('flag', None); r.pop('first', None)
json.dump(F, open(R + 'tools/m33/fixes.json', 'w'), ensure_ascii=False, indent=1)
for k, v in F.items():
    for r in v: print(k, r['type'], r['ref'], '|', r['title'], '|', r['la'][:70], '...', r['la'][-40:], '|', r['en'][:50])
