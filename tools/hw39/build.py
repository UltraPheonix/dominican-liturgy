"""Holy Week as printed, transcribed: hw39/<day>.src -> site/data/holyweek_text.js
Each block keeps the book's words; Latin j is written i (site style)."""
import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.environ.get('SITE', os.path.join(HERE, '..', '..'))

def latin_i(s):
    return s.replace('j', 'i').replace('J', 'I')

def curly(s):
    s = re.sub(r'"([^"]*)"', '\u201c\\1\u201d', s)
    s = re.sub(r"(^|[\s\u201c(])'", '\\1\u2018', s)
    return s.replace("'", '\u2019')

def speakers(s):
    # Passion speaker marks: ✠ (Christ), C (Chronista), S (Synagoga), * (the pause before Mane autem facto)
    s = re.sub(r'(?<![{\w])([CS✠*])(?=\s)', r'{\1}', s)
    return s

def readsrc(path):
    out = []
    for raw in open(path, encoding='utf8').read().split('\n'):
        if raw.startswith('INC: '):
            out += readsrc(os.path.join(HERE, raw[5:].strip() + '.src'))
        else:
            out.append(raw)
    return out

def parse(path, lang_i=True):
    lines = readsrc(path)
    out, stack = [], []
    cur = None
    def target():
        return stack[-1]['blocks'] if stack else (out[-1]['blocks'] if out else None)
    for raw in lines:
        if not raw.strip() or raw.startswith('#'):
            continue
        if raw.startswith(' = '):
            cur['en'] = curly(raw[3:].strip()); continue
        tag, _, body = raw.partition(': ') if not raw.startswith(('==', 'F/')) else (raw[:2], '', raw[2:].strip())
        if tag == '==':
            la, en = [x.strip() for x in body.split('|')]
            out.append({'la': latin_i(la), 'en': en, 'blocks': []}); cur = None; continue
        if tag == 'F/':
            stack.pop(); continue
        if tag == 'F':
            la, en = [x.strip() for x in body.split('|')]
            f = {'t': 'F', 'la': latin_i(la), 'en': en, 'blocks': []}
            target().append(f); stack.append(f); continue
        if tag == 'X':
            for x in body.split(','): target().append({'t': 'X', 'x': x.strip()})
            continue
        if tag == 'G':
            gid, _, lab = body.partition('|'); gid = gid.strip()
            if os.path.exists(os.path.join(SITE, 'gabc', gid + '.gabc')):
                b = {'t': 'G', 'id': gid}
                if lab.strip(): b['n'] = lab.strip()
                target().append(b)
            continue
        if tag == 'C':
            c, _, lab = body.partition('|'); p, i = c.split(); b = {'t': 'C', 'p': p, 'i': int(i)}
            if lab.strip(): b['n'] = lab.strip()
            target().append(b); continue
        if tag == 'P':
            la = open(os.path.join(HERE, body + '_parts.txt'), encoding='utf8').read().strip().split('\n\n')
            en = open(os.path.join(HERE, body + '_en.txt'), encoding='utf8').read().strip().split('\n\n')
            assert len(la) == len(en), (body, len(la), len(en))
            for k, (a, b) in enumerate(zip(la, en)):
                a = speakers(a); b = curly(speakers(b))
                if k == 0 or a.startswith('ALTERA'): a = '^' + a
                target().append({'t': 'T', 'la': latin_i(a), 'en': b})
            continue
        if tag in ('H', 'I', 'L', 'R', 'T'):
            cur = {'t': tag, 'la': latin_i(body.strip())}
            target().append(cur); continue
        raise SystemExit('bad line: ' + raw)
    return out

def check(blocks, where=''):
    for b in blocks:
        if b.get('blocks'): check(b['blocks'], where); continue
        if b['t'] in ('H', 'I', 'L', 'R', 'T') and not b.get('en'):
            raise SystemExit('no English: ' + b['la'][:60])
        for k in ('la', 'en'):
            v = b.get(k, '')
            if v.count('{') != v.count('}') or v.count('*') % 2 and b['t'] == 'R':
                raise SystemExit('unbalanced markup: ' + v[:80])

PAGES = {'Quad6': '137–146', 'Quad6m': '146–148', 'Quad6t': '148–154', 'Quad6w': '154–160', 'Quad6h': '160–166', 'Quad6f': '166–179', 'Quad6s': '179–191'}
PAGES59 = {}
data = {'1939': {}}
data['1959'] = {}
for rite, suf in (('1939', ''), ('1959', '_59')):
  for day in ['Quad6', 'Quad6m', 'Quad6t', 'Quad6w', 'Quad6h', 'Quad6f', 'Quad6s']:
    p = os.path.join(HERE, day + suf + '.src')
    if os.path.exists(p):
        secs = parse(p)
        for s in secs: check(s['blocks'])
        if rite == '1939': secs[0]['src'] = 'Missale Ordinis Prædicatorum (1939), pp. ' + PAGES[day]
        else: secs[0]['src'] = 'St Dominic Missal (1959), pp. ' + PAGES59.get(day, '')
        data[rite][day] = secs
open(os.path.join(SITE, 'data/holyweek_text.js'), 'w', encoding='utf8').write(
    '// Holy Week transcribed as printed: Missale O.P. (1939) and St Dominic Missal (1959) (Latin j written i). Built by tools/hw39/build.py.\n'
    'window.HW_TEXT = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
print({r: {d: sum(len(s['blocks']) for s in v) for d, v in data[r].items()} for r in data})
