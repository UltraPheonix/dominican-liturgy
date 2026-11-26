"""Compact outline of a feast's Mass in the Missale O.P. 1939 text layer (orat39/m39lin.txt): section heads and their first lines.
Usage: python3 dump.py MMDD [MMDD...]  (finds 'Die D Month' then the title)."""
import sys, re, json
L = open('../../orat39/m39lin.txt').read().split('\n')
MON = ['Januarii','Februarii','Martii','Aprilis','Maii','Junii','Julii','Augusti','Septembris','Octobris','Novembris','Decembris']
HEAD = re.compile(r'^(Officium|Introitus|Oratio|Secreta|Postcommunio|Graduale|Lectio|Léctio|Sequentia sancti|Evangelium|Offertorium|Communio|Tractus|Alleluia|Commemoratio|Missa|Omnia|Et fit|Si |In Missa|Ut in|Praefatio|Credo|Gloria)')
def page_at(i):
    for j in range(i, -1, -1):
        m = re.match(r'@@PAGE (\d+)', L[j])
        if m: return int(m.group(1))
for a in sys.argv[1:]:
    mo, d = int(a[:2]), int(a[2:])
    pat = re.compile(r'^Die %s %s\b' % (r'\s?'.join(str(d)), MON[mo-1]))
    hits = [i for i, l in enumerate(L) if pat.match(l.strip())]
    for h in hits:
        if h < 30000: continue
        end = next((j for j in range(h+1, min(len(L), h+600)) if re.match(r'^Die \d', L[j].strip())), h+600)
        print('=====', a, 'line', h+1, 'pdfpage', page_at(h), '->', page_at(end))
        for j in range(h+1, end):
            s = L[j].strip()
            if j < h+4 or HEAD.match(s):
                nxt = ' '.join(x.strip() for x in L[j+1:j+3])
                print('  %6d %s || %s' % (j+1, s[:70], nxt[:80]))
