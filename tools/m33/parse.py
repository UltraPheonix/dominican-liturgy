import json, re, unicodedata
L = json.load(open('/home/claude/m33/lines.json'))
def norm(s):
    s = unicodedata.normalize('NFD', s); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.lower().replace('æ', 'ae').replace('œ', 'oe').replace('j', 'i').replace('v', 'u')
    return re.sub(r'[^a-z]+', ' ', s).strip()
# join lines into a stream with soft hyphen / hyphen joins
HEAD = [('introit', r'^(Officium|Introitus)[.■]?(\s*$|\s+[A-Z]|\s+(Psalm|Ps)\.)'), ('oratio', r'^(Oratio|Collecta)\b'), ('lesson', r'^\W{0,3}(Lectio|Lectio)\b'),
        ('gospel', r'^.{0,5}?(Sequentia sancti Evangelii|Initium sancti Evangelii|Passio Domini)'),
        ('gradual', r'^(.{0,5}?\b(Psalm|Ps)\.\s*\d|Graduale\b|\W{0,3}(&|Tk|1\$|\$|R|IJ|Bf|fy|Ę)\.\s*(Psalm|Ps\.|Isa|Eccli|Joann|Matth|Luc|Dan|Exo|Ap|Jer|Sap|Prov|Cant|Job|Judith|Esther|Gal|Rom|Phil|Hab|Zach|Tob|II|I )|Psalm\.)'),
        ('alleluia', r'^Alleluia,? alleluia\.'), ('tract', r'^Tractus\b'), ('sequence', r'^Sequentia(?! sancti)'),
        ('offertory', r'^Offertorium\b'), ('secret', r'^Secreta\b'), ('communion', r'^Communio\b'), ('postcommunion', r'^Postcommunio\b'),
        ('credo', r'^Credo\.?$'), ('gloria', r'^Gloria in excelsis'), ('rubric', r'^(Non dicitur|Dicitur|In fine|Hae|Haec|Si |Ubi |Tempore Paschali|Extra)')]
HR = [(k, re.compile(p)) for k, p in HEAD]
masses = []; cur = None; title = []
for i, (pg, kind, l) in enumerate(L):
    if kind == 'T':
        if cur is None or cur['parts']: cur = {'title': [], 'page': pg, 'parts': []}; masses.append(cur)
        cur['title'].append(l); continue
    if cur is None: continue
    k = next((k for k, r in HR if r.match(l)), None)
    if k: cur['parts'].append([k, pg, [l]])
    elif cur['parts']: cur['parts'][-1][2].append(l)
    else: cur['title'].append(l)
def join(ls):
    s = ''
    for l in ls:
        if s.endswith('\xad') or s.endswith('-'): s = s[:-1] + l
        else: s += (' ' if s else '') + l
    return re.sub(r'\s+', ' ', s).strip()
for m in masses:
    for p in m['parts']: p[2] = join(p[2])
json.dump(masses, open('/home/claude/m33/masses33.json', 'w'), ensure_ascii=False, indent=0)
