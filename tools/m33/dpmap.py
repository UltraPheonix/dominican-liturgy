import json, re, difflib, subprocess
import mapall as M
from parse import norm
SEC = json.loads(subprocess.run(['node', '-e', '''global.window={}; eval(require('fs').readFileSync('/home/claude/dominican-liturgy/data/masses.js','utf8').replace(/^var /mg,'global.'));
const o={}; for (const s of DOMINICAN.sections) o[s.id]=s.items; console.log(JSON.stringify(o));'''], capture_output=True, text=True).stdout)
def m33_introits(p0, p1):
    out = []
    for i, (pg, kd, l) in enumerate(M.L):
        if p0 <= pg <= p1 and M.kind(l) == 'introit':
            txt = []
            for j in range(i, i + 8):
                s = M.L[j][2]
                if j == i: s = re.sub(r'^(Officium|Introitus)\s*', '', s)
                if re.match(r'^(Psalm|Ps|[A-Z][a-z]{1,6})\.\s*\d', s) and len(s) < 22: continue
                txt.append(s)
            out.append((i, norm(' '.join(txt))[:80]))
    return out
def sim(inc, txt):
    a = norm(inc).split(); b = txt.split()
    if not a or not b: return 0
    a2 = ' '.join(a)[2:]; b2 = ' '.join(b)[2:2 + len(' '.join(a)) + 4]
    r = difflib.SequenceMatcher(None, a2, b2).ratio()
    k2 = ' '.join(a[1:3])
    if len(a) > 2 and len(k2) >= 9 and k2 in ' '.join(b[:7]): r = max(r, 0.9)
    return r
def dp(keys, ints):
    n, m = len(keys), len(ints)
    S = [[0.0] * (m + 1) for _ in range(n + 1)]; B = [[None] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s = sim(M.INTR.get(keys[i - 1], ''), ints[j - 1][1])
            opts = [(S[i - 1][j], 'u'), (S[i][j - 1], 'l'), (S[i - 1][j - 1] + (s if s > 0.55 else -0.2), 'd')]
            S[i][j], B[i][j] = max(opts)
    i, j = n, m; res = {}
    while i > 0 and j > 0:
        b = B[i][j]
        if b == 'd': res[keys[i - 1]] = ints[j - 1]; i -= 1; j -= 1
        elif b == 'u': i -= 1
        else: j -= 1
    return res
if __name__ == '__main__':
    out = {}
    for sec, (p0, p1) in (('tempore', (44, 385)), ('commune', (645, 677)), ('votivae', (678, 745))):
        keys = [k for k in SEC[sec] if not k.startswith('Quad6')]
        ints = m33_introits(p0, p1)
        r = dp(keys, ints)
        for k in keys:
            out[k] = r.get(k, [None, ''])[0]
            t=r.get(k,[None,'-'])[1]; print(sec, k, M.INTR.get(k, ''), '|', '%.2f'%(sim(M.INTR.get(k,''),t) if k in r else 0), t[:40])
    json.dump(out, open('/home/claude/m33/dpmap.json', 'w'))
