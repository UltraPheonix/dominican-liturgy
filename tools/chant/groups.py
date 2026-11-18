"""groups.py PAGE : per staff, note groups (notes closer than G px join a group), in gabc letters, with x; bars dropped."""
import sys, subprocess, re
G = int(sys.argv[2]) if len(sys.argv) > 2 else 30
out = subprocess.run(['python3', '/tmp/rt/heads.py', sys.argv[1]], capture_output=True, text=True).stdout
for line in out.split('\n'):
    if line.startswith('staff'): print(line.split(' lines')[0], end=': ')
    m = re.match(r'\s+clef pos \[([^\]]*)\]\s+notes: (.*)', line)
    if m:
        ns = [(int(t[:-1]), t[-1]) for t in m.group(2).split() if t[-1] not in 'ab']
        gs = []; 
        for x, p in ns:
            if gs and x - gs[-1][-1][0] < G: gs[-1].append((x, p))
            else: gs.append([(x, p)])
        def fmt(g):
            # same x = stacked: lower first (pes)
            g = sorted(g, key=lambda t: (t[0] // 8, t[1]))
            return ''.join(p for x, p in g)
        print('clef', m.group(1), '|', ' '.join('%s@%d' % (fmt(g), g[0][0]) for g in gs))
    if line.strip().startswith('lyrics'): print('   ', line.strip())
