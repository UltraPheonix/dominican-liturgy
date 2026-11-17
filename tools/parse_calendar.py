import re, json
T = open('sources/calendarium_op_1960.txt', encoding='utf8').read().split('\n')
MON = ['IANUARIUS','FEBRUARIUS','MARTIUS','APRILIS','MAIUS','IUNIUS','IULIUS','AUGUSTUS','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']
mon, out, appendix, last = None, [], False, -1
for l in T:
    s = l.strip()
    if s in MON:
        mon = MON.index(s)
        if mon < last: appendix = True
        last = mon
        continue
    if mon is None: continue
    m = re.match(r'^(\d{1,2}):?\s+(.*)$', s)
    if not m: continue
    day, rest = int(m.group(1)), m.group(2).strip()
    rest = re.sub(r'\s{2,}\(M\d.*$', '', rest).strip()
    if not rest or rest.startswith('[') or rest.startswith('<') or rest.startswith('Feria') or rest.startswith('Memoria'):
        continue
    rk = re.search(r'\b(I{1,3}|IV) cl\.', rest)
    rank = rk.group(1) if rk else ''
    name = re.sub(r'\s*\b(I{1,3}|IV) cl\..*$', '', rest).strip()
    name = re.sub(r'\s+\d+$', '', re.sub(r'\s{3,}.*$', '', name)).strip()
    out.append({'month': mon, 'day': day, 'name': name, 'rank': rank, 'beatus': appendix, 'op': bool(re.search(r'O\.\s?P\.|Ord\. Praed', rest))})
json.dump(out, open('calendar.json','w'), ensure_ascii=False, indent=0)
print(len(out)); print('\n'.join('%2d/%2d %-3s %s' % (o['month']+1,o['day'],o['rank'],o['name']) for o in out[::9]))
