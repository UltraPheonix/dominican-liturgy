#!/usr/bin/env python3
"""Extract every reading of the Commune pages (text layer @@PAGE 368-387) -> /tmp/A7/comm_readings.json"""
import re, json
L = open('/tmp/A7/comm.txt', encoding='utf8').read().split('\n')
END = re.compile(r'^\W{0,3}\s*(Offertorium|Graduale|Infra Septuag|Tempore|Credo|In festo|Aliud Evangelium|alia Missa|Secreta|Tractus|Communio|Oratio\b|.{0,4}Sequentia sancti|.{0,3}L\s?e\s?c\s?t\s?i\s?o\b|Lectio|\S{0,4} ?Ps\. ?\d+ |Alleluia, al)')
out = []; page = None; i = 0
while i < len(L):
    l = L[i]
    if l.startswith('@@PAGE'): page = int(l.split()[1])
    if re.search(r'L.?ectio|Sequentia sancti Evangelii', l) and not l.startswith('@@'):
        head = l; j = i + 1; hp = page
        while j < len(L) and not re.match(r'^\s*(IN |In |I N|IX |l illo|[A-Z]{3,}|[A-Z][a-z]+ \S)', L[j]) or re.match(r'^\s*(Apostoli|Joannis|secundum|c\. \d|\d,? ?c\.|Eccli|Prov|Osee)', L[j]):
            head += ' ' + L[j]; j += 1
            if j - i > 6: break
        txt = []; k = j; pg = page
        while k < len(L):
            if L[k].startswith('@@PAGE'): pg = int(L[k].split()[1]); k += 3; continue
            if END.match(L[k]) and k > j: break
            txt.append(L[k]); k += 1
        t = ' '.join(txt); t = re.sub(r'­ ', '', t); t = re.sub(r'(\w)- +(\w)', r'\1\2', t); t = re.sub(r'\s+', ' ', t)
        out.append({'page': hp, 'line': i + 1, 'head': re.sub(r'\s+', ' ', head), 'la': t})
        i = k; continue
    i += 1
json.dump(out, open('/tmp/A7/comm_readings.json', 'w'), ensure_ascii=False, indent=0)
for n, r in enumerate(out): print(n, r['page'], r['head'][:70], '|', r['la'][:60], '...', r['la'][-50:])
