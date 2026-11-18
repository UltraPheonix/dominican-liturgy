"""Split a stretch of the St Dominic Missal (1959) text into its English and Latin streams,
then into labelled sections.  usage: dmsplit.py LINE0 LINE1  -> JSON {en:[[label,text]], la:[[label,text]]}"""
import re, sys, json
L = open('/home/claude/dl/txt/dm.txt', encoding='utf8', errors='replace').read().split('\n')
a, b = int(sys.argv[1]), int(sys.argv[2])
EN = set('the and of to him he you that his is was they them with for who have your my me what not are said be will this which you us our we let o shall from by it may grant through lord god'.split())
LA = set('et est in non autem qui ad eum ejus quod illi sunt cum dixit enim ut de quia sed ego vos tu super nos per dominum deus domine quae qui tuam tua meus mea me'.split())
HEAD = re.compile(r'^\s*(\d+\s+)?(THE PROPER OF THE SEASON|[A-Z ]*HOLY WEEK|MAUNDY THURSDAY|GOOD FRIDAY|HOLY SATURDAY|PALM SUNDAY)(\s+\d+)?\s*$')
stream = {'en': [], 'la': []}
last = 'en'
for l in L[a:b]:
    if HEAD.match(l) or not l.strip():
        continue
    w = re.findall(r"[a-zA-Z]+", l.lower())
    e = sum(x in EN for x in w); la = sum(x in LA for x in w)
    lang = 'en' if e > la else 'la' if la > e else last
    stream[lang].append(l.strip()); last = lang
LAB = {'en': r'(Introit|Collect|Prayer|Lesson|Gradual|Responsory|Tract|Gospel|Offertory|Secret|Communion|Postcommunion|Prayer over the people|Epistle)\.',
       'la': r'(Introitus|Oratio|Lectio|Responsorium|Graduale|Tractus|Evangelium|Offertorium|Secreta|Communio|Postcommunio|Oratio super populum|Epistola)\.'}
out = {}
for k, lines in stream.items():
    text = ''
    for l in lines:
        if text.endswith('-'): text = text[:-1] + l
        else: text += ' ' + l
    parts = re.split(r'\s(?=' + LAB[k] + r'\s)', text)
    out[k] = [[re.match(LAB[k], p).group(1) if re.match(LAB[k], p) else '', p] for p in parts]
print(json.dumps(out, ensure_ascii=False, indent=1))
