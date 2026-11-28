import json, re, unicodedata, difflib
ST = '/tmp/A7/state/'
def R(): return json.load(open(ST + 'readings33.json'))
def M(): return json.load(open(ST + 'masses.json'))
def deacc(s):
    s = s.replace('æ', 'ae').replace('Æ', 'Ae').replace('œ', 'oe').replace('Œ', 'Oe').replace('ǽ', 'ae').replace('Ǽ', 'Ae')
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
def norm(s):   # for similarity: lower, deaccent, j->i, letters only
    s = deacc(s).lower().replace('j', 'i').replace('v', 'u')
    return re.findall(r'[a-z]+', s)
def toks(s):   # words and marks, deaccented, case kept, j->i
    s = deacc(s).replace('j', 'i').replace('J', 'I')
    return re.findall(r"[A-Za-z]+|[.,:;?!]", s)
def sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b), autojunk=False).ratio()
