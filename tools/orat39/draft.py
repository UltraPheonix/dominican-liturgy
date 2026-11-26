"""Draft orations for a Mass from the Missale O.P. 1939 text layer (m39lin.txt), to be proofed against the page images.
Usage: python3 draft.py KEY:LINE [KEY:LINE ...]   (LINE = a line in m39lin.txt at or before the Mass's Oratio)
Writes /tmp/cand.json (raw text per prayer, for proof2.py crops) and prints accented drafts + St Dominic Missal English."""
import sys, re, json
sys.argv, args = sys.argv[:1], sys.argv[1:]
from build_or import latin, english, clean_en, flat
L = open('m39lin.txt').read().split('\n')
HEAD = {'or': re.compile(r'^Oratio\s*$'), 'se': re.compile(r'^Secreta\b'), 'pc': re.compile(r'^(Pro pluribus )?Postcommunio\b')}
STOP = re.compile(r'^(Secreta|Postcommunio|Praefatio|Graduale|Lectio|Léctio|Communio|Offertorium|Evangelium|Sequentia|Tractus|Alleluia|Die \d|Festa |Oratio|Commemoratio|Secunda|Oremus|Humiliate|Dominica|Feria|DOMINICA|FERIA|Officium|In Vigilia|@@PAGE)')
COMM = re.compile(r'^(De S|De SS|De B|Des\.|De sancta|De Ss|Commemoratio)')
def grab(i, kind):
    j = i
    while j < len(L):
        s0 = L[j].strip()
        if j > i + 3 and re.match(r'^Die \d', s0): return None, i   # next day: this Mass has no proper prayer here
        if HEAD[kind].match(s0):
            prev = [x.strip() for x in L[max(0, j - 2):j] if x.strip()]
            if not (prev and COMM.match(prev[-1])): break
        j += 1
    if j - i > 400 or j >= len(L): return None, i
    out = []; k = j + 1
    while k < len(L):
        s = L[k].strip()
        if s in ('C', '') or re.match(r'^\d+\*?$', s) or s.startswith('@@PAGE') or re.match(r'^Festa |^Commune|^Missae votivae|^Proprium', s): k += 1; continue
        if STOP.match(s): break
        out.append(s); k += 1
    t = ''.join(x[:-1] if x.endswith('­') else x + ' ' for x in out)
    t = re.sub(r'\s+', ' ', t).strip()
    m = re.search(r'(Per (eumdem )?Dominum|Qui vivis|Qui tecum|qui tecum)(\.\.\.[^.]*|[^.])*\.', t)
    if m: t = t[:m.end()]
    return t, k
cand = {}
for a in args:
    key, line = a.split(':'); pr = {}
    if '@' in line:  # explicit: or@L,se@L,pc@L
        for part in line.split(','):
            kind, l0 = part.split('@'); t, _ = grab(int(l0) - 1, kind)
            if t: pr[kind] = t
        line = line.split(',')[0].split('@')[1]
    else:
        i = int(line) - 1
        for kind in ('or', 'se', 'pc'):
            t, i2 = grab(i, kind)
            if t: pr[kind] = t; i = i2
    cand[key] = {'start': int(line) - 1, 'pr': pr}
    hd=[x.strip() for x in L[int(line)-1:int(line)+6] if x.strip()][:4]
    print('=====', key, '|', ' / '.join(hd))
    for kind in ('or', 'se', 'pc'):
        if kind not in pr: print(kind, 'NOT FOUND'); continue
        la, ec, unk = latin(pr[kind])
        r, en = english(kind, flat(pr[kind]))
        en = clean_en(en, ec)[0] if en and r >= 0.75 else ''
        print(kind, '|', la.split(' Per Dóminum nostrum')[0].split(' Qui vivis et')[0][:600], '| unk', unk)
        print('   EN', round(r, 2), en[:400])
json.dump(cand, open('/tmp/cand.json', 'w'), ensure_ascii=False)
