"""Error check of every Mass against the St. Dominic Missal (1959): chants and Epistle/Gospel references."""
import json, re, sys, unicodedata
D = json.loads(open('site/data/masses.js', encoding='utf8').read().split('var DOMINICAN = ', 1)[1].rstrip().rstrip(';'))
dm = json.load(open('dm_masses.json'))['masses']
pairs = json.load(open('temporale_dm_pairs.json')) if len(sys.argv) < 3 else {}
def fl(s): return re.sub(r'[^a-z]', '', ''.join(c for c in unicodedata.normalize('NFD', (s or '').lower()) if not unicodedata.combining(c)).replace('j', 'i'))
inc = lambda i: D['chants'].get(str(i), {}).get('i', '?')
import dm_merge
def words(s): return set(w[:5] for w in re.findall(r'[a-z]{4,}', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c))))
def readings_dm(m):
    out = []
    for r in m['readings']:
        if 'book' in r:
            b = dm_merge.book(r['book']); ref = dm_merge.clean_ref(r['ref'])
            if b and ref: out.append((r['type'], b, ref.split(':')[0].strip()))
    return out
report = {'chant': [], 'reading': []}
checked = 0
for s in D['sections']:
    if s['id'] not in ('sanctorum', 'beati'): continue
    for k in s['items']:
        M = D['masses'][k]
        if 'month' not in M or M['month'] > 11: continue
        key = '%02d%02d' % (M['month'] + 1, M['day'])
        cands = [m for m in dm if m['kind'] == 'saint' and m['key'] == key]
        name = words((M.get('name_en') or '') + ' ' + M['title'])
        cands = [m for m in cands if words(m['title']) & name] or ([cands[0]] if len(cands) == 1 else [])
        if not cands: continue
        d = cands[0]; checked += 1
        for p, ids in d['parts'].items():
            ours = [c['id'] for c in M['parts'].get(p, [])]
            if not ours: continue
            if not {fl(inc(x))[:10] for x in ids} & {fl(inc(x))[:10] for x in ours}:
                report['chant'].append((k, M.get('name_en') or M['title'], p, [inc(x)[:24] for x in ours], [inc(x)[:24] for x in ids]))
        ours_r = {(r['type'] if r['type'] != 'Lesson' else 'Epistle', r['ref'].rsplit(' ', 2)[0] if False else re.sub(r'\s+\d+:.*$', '', r['ref'])) for r in M.get('readings', [])}
        for t, b, ch in readings_dm(d):
            t = 'Epistle' if t == 'Lesson' else t
            mine = [r for r in M.get('readings', []) if (r['type'] if r['type'] != 'Lesson' else 'Epistle') == t]
            if mine and not any(r['ref'].startswith(b + ' ' + ch + ':') for r in mine):
                report['reading'].append((k, M.get('name_en') or M['title'], t, [r['ref'] for r in mine], '%s %s' % (b, ch)))
json.dump(report, open('audit_report.json', 'w'), ensure_ascii=False, indent=1)
print('saints checked against the Missal:', checked, '; chant differences:', len(report['chant']), '; reading differences:', len(report['reading']))
for x in report['chant'][:25]: print('  C', x)
for x in report['reading'][:25]: print('  R', x)
