import json, re, sys
DAY = sys.argv[1]; F = json.load(open('/home/claude/build/ten/final_%s.json' % DAY))
PAGES = json.load(open('/home/claude/build/ten/pages_%s.json' % DAY))
MODE = json.load(open('/home/claude/build/ten/modes_%s.json' % DAY))
def ispell(s): return s.replace('j', 'i').replace('J', 'I')
PART = {'t': 'Antiphona', 'u': 'Antiphona', 'v': 'Versus', 'l': 'Lectio', 'k': 'Versus'}
for code, d in F.items():
    clef, body = d['gabc'].split(' ', 1)
    toks = re.findall(r'([^()]*)\(([^)]*)\)(\s*)', body)
    out = []; pend = ''
    for t, n, sp in toks:
        t0 = t
        t = t.strip()
        if t.startswith('℣.'): t = t[2:].strip(); pend = '<sp>V/</sp>. ' if not pend else pend
        nxt = ''
        if t.endswith('℟.'): t = t[:-2].strip(); nxt = '<sp>R/</sp>. '
        lead = ' ' if t0.startswith(' ') else ''
        if t: t = pend + ispell(t); pend = ''
        out.append('%s%s(%s)%s' % (lead, t, n, sp))
        if nxt: pend = nxt
    body = re.sub(r'\s+', ' ', ''.join(out)).strip()
    if code[0] == 'v': body = '<sp>V/</sp>. ' + body if not body.startswith('<sp>') else body
    hdr = ('name:%s;\noffice-part:%s;\n%sbook:Ecclesiasticum Officium O.P. Triduo ante Pascha (1927), p. %s;\ntranscriber:%s for dominicanrite.com;\ninitial-style:%s;\n%%%%\n'
           % (ispell(d['name']), PART[code[0]], ('mode:%s;\n' % MODE[code]) if MODE.get(code) else '', PAGES[code], d['src'], '0' if code[0] in 'vk' else '1'))
    open('/home/claude/dominican-liturgy/gabc/op-ten-%s-%s.gabc' % (DAY, code), 'w').write(hdr + clef + ' ' + body + '\n')
print('ok', len(F))
