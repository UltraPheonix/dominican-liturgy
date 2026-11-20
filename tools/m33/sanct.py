import json, re
L = json.load(open('/home/claude/m33/lines.json'))
MON = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'Maj': '05', 'Mai': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
E = []
for i, (pg, k, l) in enumerate(L):
    m = re.search(r'Die\s+(\d{1,2})\s+(Jan|Feb|Mar|Apr|Maj|Mai|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b(?!\s*\d{4})', l)
    if m and len(l) < 45 and pg > 380 and not re.search(r'\d{4}', l):
        name = ' '.join(x[2] for x in L[i + 1:i + 4])
        E.append({'line': i, 'page': pg, 'date': MON[m.group(2)] + '%02d' % int(m.group(1)), 'name': name})
json.dump(E, open('/home/claude/m33/sanct.json', 'w'), ensure_ascii=False)
if __name__ == '__main__':
    print(len(E)); import collections
    c = collections.Counter(e['date'][:2] for e in E); print(sorted(c.items()))
    for e in E[:8]: print(e)
