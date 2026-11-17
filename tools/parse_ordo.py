import re, json
L = open('sources/ordo_op_2026.txt', encoding='utf8').read().split('\n')
E_RE = re.compile(r'^\s*(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(\d{4})-(\d\d)-(\d\d)\s+Mass\s+(.*?)\s*(?:M33:.*?)?(M39:\s*([^\s]+(?:\s\(\d\))?(?:\s?S\d\s\(\d\))?))?\s*(?:M65:.*)?$')
out, region = [], False
i = 0
while i < len(L):
    l = L[i]
    if l.strip().startswith('Region:'):
        region = True; i += 1; continue
    m = E_RE.match(l)
    if m:
        name = m.group(5).strip()
        # continuation of the Latin name on the next line(s)
        j = i + 1
        while j < len(L) and L[j].startswith(' ' * 20) and L[j].strip() and not re.match(r'^\s*(cl\.|tr\.|Gloria|Mem\.)', L[j]):
            name += ' ' + L[j].strip(); j += 1
        cls = ''
        for k in range(i + 1, min(i + 5, len(L))):
            c = re.match(r'^\s*cl\.\s*(I{1,3}|IV)\b', L[k])
            if c: cls = c.group(1); break
        tr = ''
        for k in range(i + 1, min(i + 6, len(L))):
            t = re.search(r'tr\.\s+(.*)$', L[k])
            if t: tr = t.group(1).strip(); break
        out.append({'date': '%s-%s-%s' % (m.group(2), m.group(3), m.group(4)), 'name': re.sub(r'\s+', ' ', name),
                    'm39': (m.group(7) or '').strip(), 'cls': cls, 'en': tr, 'region': region})
        region = False
    i += 1
json.dump(out, open('ordo2026.json', 'w'), ensure_ascii=False, indent=0)
gen = [o for o in out if not o['region']]
print(len(out), 'entries,', len(gen), 'general;', sum(1 for o in gen if o['m39']), 'with M39 page')
for o in gen[15:40]: print(o['date'], o['cls'], '%-40s' % o['name'][:40], o['m39'], '|', o['en'][:30])
