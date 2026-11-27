"""The Ordo of the Order of Preachers for 1944 (Provincia Poloniae; archive.org dlibra.kul.pl.34313, djvu OCR) -> one entry per day.
Days begin with their weekday (Dom., Fer. 2.-6., Sabb.); dates are given by counting, and the weekday sequence is checked."""
import re, json, sys, datetime
T = open(sys.argv[1], encoding='utf8').read().split('\n')
WD = re.compile(r'^\W{0,4}(?:(\d{1,2})\s?[|;:!]\s?)?(Dom\.|Fer\.\s*[2-6lIi]\.?|Fer\.\s*[2-6]|Sabb\.)\s*(.*)$')
starts = []
for i, l in enumerate(T):
    m = WD.match(l.strip())
    if m: starts.append((i, m.group(2), m.group(3), int(m.group(1)) if m.group(1) else None))
def wd(tok):
    if tok.startswith('Dom'): return 6
    if tok.startswith('Sabb'): return 5
    n = re.search(r'[2-6]', tok); return int(n.group()) - 2 if n else None
print(len(starts), file=sys.stderr)
# find the first Saturday 1 January 1944 (Sabb.): the entry with 'Circumcisio'
first = next(k for k, s in enumerate(starts) if 'ircumcis' in ' '.join(T[s[0]:s[0] + 2]))
d = datetime.date(1944, 1, 1); out = []; miss = []
k = first
cand = [st for st in starts[first:] if not re.match(r'^\s*[—\-,;.]|^\s*et\b|^\s*Compl', st[2])]
c = 0; byday = {}
while d.year == 1944 and c < len(cand):
    i, tok, rest, n = cand[c]; w = wd(tok)
    # a printed day of the month: jump to that date (forward up to 12 days, or back up to 3) when the weekday agrees
    if n:
        for off in list(range(0, 13)) + [-1, -2, -3]:
            x = d + datetime.timedelta(days=off)
            if x.day == n and x.year == 1944 and (w is None or w == x.weekday()):
                for y in range(off): miss.append((d + datetime.timedelta(days=y)).isoformat())
                d = x; break
    if w == d.weekday() or w is None:
        j = cand[c + 1][0] if c + 1 < len(cand) else len(T)
        byday[d.isoformat()] = {'date': d.isoformat(), 'head': re.sub(r'\s+', ' ', ' '.join(T[i:i + 3]))[:200], 'text': '\n'.join(T[i:j])}
        d += datetime.timedelta(days=1); c += 1
    elif w == (d + datetime.timedelta(days=1)).weekday():
        miss.append(d.isoformat()); d += datetime.timedelta(days=1)
    else:
        c += 1
out = [byday.get(x.isoformat(), {'date': x.isoformat(), 'head': '(not found in the OCR)', 'text': ''})
       for x in (datetime.date(1944, 1, 1) + datetime.timedelta(days=k) for k in range(366))]
miss = [o['date'] for o in out if not o['text']]
print('missing', miss, file=sys.stderr)
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
print(len(out), 'days; last', out[-1]['date'], file=sys.stderr)
