"""Divinum Officium left some references unresolved in the Office data ("Commune/C1:Ant Vespera.", "... is missing!").
This replaces them with the texts (Roman/Dominican common, Antiphonarium O.P. 1933 where it has them). Idempotent.
Run: python3 tools/office/fix_missing.py"""
import json, os, re
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'office')
# antiphon per psalm number
ANT = {
 'Sancti/01-06:Ant Laudes.': {   # I Vespers of the Epiphany = the antiphons of Lauds (Antiphonarium 1933 pp. 367-370)
   109: ('Ante lucíferum génitus, et ante sǽcula, Dóminus Salvátor noster hódie mundo appáruit.', 'Begotten before the daystar and before all ages, the Lord our Saviour hath this day appeared to the world.'),
   110: ('Venit lumen tuum, Jerúsalem, et glória Dómini super te orta est, et ambulábunt gentes in lúmine tuo, allelúia.', 'Thy light is come, O Jerusalem, and the glory of the Lord is risen upon thee, and the Gentiles shall walk in thy light, alleluia.'),
   111: ('Apértis thesáuris suis, obtulérunt Magi Dómino aurum, thus et myrrham, allelúia.', 'Opening their treasures, the Wise Men offered to the Lord gold, frankincense and myrrh, alleluia.'),
   112: ('María et flúmina, benedícite Dómino: hymnum dícite, fontes, Dómino, allelúia.', 'Seas and rivers, bless ye the Lord: sing a hymn to the Lord, ye fountains, alleluia.'),
   116: ('Stella ista sicut flamma coruscat, et Regem regum Deum demónstrat: Magi eam vidérunt, et magno Regi múnera obtulérunt.', 'This star gleameth like a flame and showeth forth God the King of kings: the Wise Men saw it and offered gifts to the great King.')},
 'Commune/C1:Ant Vespera.': {   # II Vespers of Apostles (Commune Apostolorum)
   109: ('Jurávit Dóminus, et non pœnitébit eum: Tu es sacérdos in ætérnum.', 'The Lord hath sworn, and he will not repent: Thou art a priest for ever.'),
   112: ('Cólloco eum Dóminus cum princípibus pópuli sui.', 'The Lord placeth him with the princes of his people.'),
   115: ('Dirupísti, Dómine, víncula mea: tibi sacrificábo hóstiam laudis.', 'Thou hast broken my bonds, O Lord: I will sacrifice to thee the sacrifice of praise.'),
   125: ('Eúntes ibant et flebant, mitténtes sémina sua.', 'Going they went and wept, casting their seeds.'),
   138: ('Confortátus est principátus eórum, et honoráti sunt amíci tui, Deus.', 'Their principality is exceedingly strengthened, and thy friends, O God, are made exceedingly honourable.')},
}
FIX = [  # plain replacements (la, en)
 ('Sancti/11-01:Versum 0 is missing!', '<r>℣.</r> Exsultábunt sancti in glória.\n<r>℟.</r> Lætabúntur in cubílibus suis.'),
 ('Tempora/Pasc5-4:Responsory Vespera 1 is missing!&Gloria1\n<r>℟.</r> Allelúia.',
  '<r>℟.br.</r> Ascéndens Christus in altum, * Allelúia, allelúia.\nAscéndens.\n<r>℣.</r> Captívam duxit captivitátem. * Allelúia, allelúia.\n<r>℣.</r> Glória Patri, et Fílio, et Spirítui Sancto. Ascéndens.'),
 ('Tempora/Pasc5-4:Responsory Vespera 1 is missing!&Gloria1\n<r>℟.</r> Alleluia.',
  '<r>℟.br.</r> Christ ascending on high, * Alleluia, alleluia.\nChrist ascending.\n<r>℣.</r> He led captivity captive. * Alleluia, alleluia.\n<r>℣.</r> Glory be to the Father, and to the Son, and to the Holy Ghost. Christ ascending.'),
]
EN_VERS = ('Sancti/11-01:Versum 0 is missing!', '<r>℣.</r> The saints shall rejoice in glory.\n<r>℟.</r> They shall be joyful in their beds.')
def fix(t, en):
    if not isinstance(t, str) or ('missing' not in t and 'Commune/' not in t and 'Sancti/' not in t): return t
    for ref, table in ANT.items():
        if ref in t:
            m = re.search(r'<r>Psalm(?:us)? (\d+)', t)
            if m and int(m.group(1)) in table: t = t.replace(ref, table[int(m.group(1))][1 if en else 0])
    for a, b in FIX: t = t.replace(a, b)
    if en: t = t.replace(*EN_VERS)
    return t.replace(FIX[0][0], FIX[0][1])
n = 0
cp = os.path.join(R, 'common.json'); C = json.load(open(cp))
def is_en(t): return bool(re.search(r'<r>Psalm \d|\bthe Lord\b|\bGlory be\b', t or ''))
for k, v in C.items():
    w = fix(v, is_en(v))
    if w != v: C[k] = w; n += 1
json.dump(C, open(cp, 'w'), ensure_ascii=False, separators=(',', ':'))
for y in sorted(os.listdir(R)):
    if not re.match(r'\d{4}$', y): continue
    for f in sorted(os.listdir(os.path.join(R, y))):
        p = os.path.join(R, y, f); d = json.load(open(p)); ch = False
        for k, v in (d.get('b') or {}).items():
            w = fix(v, is_en(v))
            if w != v: d['b'][k] = w; ch = True; n += 1
        if ch: json.dump(d, open(p, 'w'), ensure_ascii=False, separators=(',', ':'))
print(n, 'blocks fixed')
