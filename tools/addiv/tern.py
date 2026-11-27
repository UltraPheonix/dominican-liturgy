"""Orationes ad supplendum numerum ternarium (Missale O.P. 1939, pp. 636-638) and the Christmastide prayer of Our Lady
(In Vigilia Epiphaniae, Secunda Oratio, Secreta, Postcommunio, pp. 32-33): -> tern.json"""
import re, json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import fix
os.chdir(H + '/../orat39')
L = open('m39lin.txt', encoding='utf8').read().split('\n')
def grab(a, head, stop):
    i = next(j for j in range(a, a + 400) if L[j].strip().startswith(head)) + 1
    out = []
    while not re.match(stop, L[i].strip()):
        s = L[i].strip()
        if not re.match(r'^(@@PAGE.*|\d+\*?|Orationes ad supplendum numerum ternarium|In Vigilia Epiphaniae Domini|ORATIONES)$', s): out.append(s)
        i += 1
    return '\n'.join(out)
A = next(j for j in range(68600, 68800) if L[j].strip() == 'AD SUPPLENDUM NUMERUM TERNARIUM')
STOP = r'^(Tertia |Secunda |\d\s*—|5 — |ORATIONES$|Secreta$|Postcommunio$|1\s*$|@@PAGE 358)'
def sec(n):  # start line of section n
    return next(j for j in range(A, A + 400) if re.match(r'^%d\s*(—|$)' % n, L[j].strip()))
raw = {
 'bvmAdv': [grab(sec(1), 'Secunda Oratio', STOP), grab(sec(1), 'Secunda Secreta', STOP), grab(sec(1), 'Secunda Postcommunio', STOP)],
 'caritatis': [grab(sec(2) if False else A + 1, 'Deus, qui caritatis dona', STOP), grab(A + 1, 'Secunda Secreta', STOP) if False else None, None],
}
# section 2 starts at "— A DOMINICA SEPTUAGESIMA"
s2 = next(j for j in range(A, A + 400) if 'SEPTUAGESIMA AD PASCHA' in L[j])
s3 = next(j for j in range(A, A + 400) if 'RESURRECTIONIS' in L[j])
s4 = next(j for j in range(A, A + 400) if 'POST OCT. EPIPHANIA' in L[j])
s5 = next(j for j in range(A, A + 500) if 'PRO DOMINO PAPA' in L[j])
raw['caritatis'] = [grab(s2, 'Secunda Oratio', STOP), grab(s2, 'Secunda Secreta', STOP), grab(s2, 'Secunda Postcommunio', STOP)]
raw['cruce'] = [grab(s3, 'Secunda Oratio', STOP), grab(s3, 'Secunda Secreta', STOP), grab(s3, 'Secunda Postcommunio', STOP)]
raw['cunctis'] = [grab(s4, 'Secunda Oratio', STOP), grab(s4, 'Secunda Secreta', STOP), grab(s4, 'Secunda Postcommunio', STOP)]
raw['papa'] = [grab(s5, 'Oratio', STOP), grab(s5, 'Secreta', r'^(1\s*$|Postcommunio$)'), grab(s5, 'Postcommunio', r'^(@@PAGE 358|Die 19)')]
V = next(j for j in range(11600, 11700) if L[j].strip() == 'In Vigilia Epiphaniae Domini')
raw['bvmNat'] = [grab(V, 'Secunda Oratio', r'^Tertia'), grab(V, 'Secunda Secreta', r'^Tertia'), grab(V, 'Secunda Postcommunio', r'^Tertia')]
out = {}
for k, v in raw.items():
    out[k] = {}
    for kind, t in zip(('or', 'se', 'pc'), v):
        t, unk = fix.clean(fix.clean.__globals__['re'].sub(r'-\s*\n', '', t.replace('­\n', '').replace('­\n', '')).replace('\n', ' '))
        out[k][kind] = t; 
        if unk: print(k, kind, unk)
json.dump(out, open(H + '/tern_raw.json', 'w'), ensure_ascii=False, indent=1)
for k, v in out.items():
    print('==', k)
    for kind in ('or', 'se', 'pc'): print(' ', kind, v[kind])
