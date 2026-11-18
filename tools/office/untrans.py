"""Collect the Latin lines that appear untranslated in the English column."""
import glob, re, json, collections, sys
from parse import parse
LAT = re.compile(r'[áéíóúǽ]')
lines = collections.Counter(); where = {}
for f in sorted(glob.glob(sys.argv[1] + '/*/*.html') if len(sys.argv) > 1 else glob.glob('/home/claude/dl/do_out/*/*.html')):
    r = parse(open(f, encoding='utf-8').read())
    for la, en in r['rows']:
        for l in en.split('\n'):
            t = re.sub(r'<[^>]+>', '', l).strip()
            if len(re.findall(r'\b\w*[áéíóúǽ]\w*', t)) >= 2:
                lines[t] += 1
                where.setdefault(t, f.split('/')[-1][:-5])
json.dump([[t, n, where[t]] for t, n in lines.most_common()], open('/home/claude/build/do/untranslated.json', 'w'), ensure_ascii=False, indent=0)
print(len(lines), 'distinct untranslated lines,', sum(lines.values()), 'occurrences;', sum(len(t) for t in lines), 'chars')
