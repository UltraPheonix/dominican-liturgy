"""Breviarium S.O.P. 1924 (Theissling; djvu text layer, djvutxt -> /tmp/b24.txt): for each day of the Proper of the Saints,
whether its Office has a proper Homily in the III Nocturn or proper Responsories. Rubricae generales § VII.2: the Homily of an
impeded Sunday is read on the least solemn day of its week among "Tota Duplicia communia et infra, quae propriam Homiliam vel
propria Responsoria non habeant, vel omnes Octavae et Feriae, quae propria Homilia non gaudeant"; the Missal (Rubr. III.3)
resumes the Sunday's Mass on that day.  usage: homily.py /tmp/b24.txt > tools/b24/homily.json"""
import sys, re, json
T = open(sys.argv[1], encoding='utf8').read().split('\n')
MON = {'Januarii': 1, 'Februarii': 2, 'Martii': 3, 'Aprilis': 4, 'Maji': 5, 'Maii': 5, 'Junii': 6, 'Julii': 7, 'Augusti': 8,
       'Septembris': 9, 'Octobris': 10, 'Novembris': 11, 'Decembris': 12}
MON.update({'Jan.': 1, 'Febr.': 2, 'Feb.': 2, 'Mart.': 3, 'Apr.': 4, 'Maj.': 5, 'Jun.': 6, 'Jul.': 7, 'Aug.': 8, 'Sept.': 9, 'Sep.': 9,
            'Oct.': 10, 'Nov.': 11, 'Dec.': 12})
# the heading of an Office ("Die 24 Januarii") and the running heads of its pages ("562 Die 25 Jan.")
H = re.compile(r'^\s*(?:\d+\s+)?Die\s+([0-9IlOoi]{1,2})\s+(' + '|'.join(re.escape(m) for m in MON) + r')(?=\s|$)')
full, run = [], []
for i, l in enumerate(T):
    m = H.match(l)
    if not m: continue
    d = m.group(1).replace('I', '1').replace('l', '1').replace('i', '1').replace('O', '0').replace('o', '0')
    if not (d.isdigit() and 1 <= int(d) <= 31): continue
    (run if m.group(2).endswith('.') or re.match(r'^\s*\d', l) else full).append((i, MON[m.group(2)], int(d)))
# Offices begin at their heading; a running head starts one only where the heading itself was not read
have = set((mo, d) for _, mo, d in full)
starts = sorted(full + [r for r in run if (r[1], r[2]) not in have and not have.add((r[1], r[2]))])
out = {}
for k, (i, mo, d) in enumerate(starts):
    j = starts[k + 1][0] if k + 1 < len(starts) else min(len(T), i + 3000)
    blk = T[i:j]; txt = '\n'.join(blk)
    ph = False
    flat = re.sub(r'-\s*\n\s*', '', txt); flat = re.sub(r'\s+', ' ', flat)
    for m in re.finditer(r'IN\s+III\s+NOCTURNO', flat):
        nxt = flat[m.end():m.end() + 160]
        if re.search(r'de\s+Comm', nxt): ph = ph or False
        elif re.search(r'Homilia|Evangelii|Lectio\s+vi', nxt): ph = True
    pr = len(re.findall(r'(?m)^\s*R[\.\-,:]\s*(?:j|ij|iij|iv|v|vj|vij|viij|ix)\b', txt)) >= 3
    md = '%02d%02d' % (mo, d)
    if md in out:  # the same date met twice (the Office and its octave pages): keep "proper" if either says so
        out[md]['ph'] = out[md]['ph'] or ph; out[md]['pr'] = out[md]['pr'] or pr
    else:
        out[md] = {'ph': ph, 'pr': pr, 'line': i}
print(json.dumps(out, sort_keys=True))
print(len(out), 'days', file=sys.stderr)
