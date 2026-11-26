"""python3 show.py 'MM-DD' : the machine reading of a feast (propers1909.json), its doubtful pieces, and the pdf pages to read
(pdftoppm -f N -l N -r 110 -gray -png /tmp/b09/<vol>.pdf out). For the eye pass → propers_fix.json."""
import sys, json, glob, re, os
import latdict as LD
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'propers1909.json')))
W = re.compile(r"[A-Za-zÀ-ÿǽæœÆŒ]+")
def nb(t): return ' '.join(LD.base(w) for w in W.findall(t))
for k, P in D.items():
    if not k.startswith(sys.argv[1]): continue
    print('=====', k, P.get('rank'), P.get('vol'))
    probes = []
    for sec in ('v1', 'mat', 'laud', 'v2'):
        for kk, v in (P.get(sec) or {}).items():
            print(' %s.%s: %s' % (sec, kk, json.dumps(v, ensure_ascii=False)))
            if isinstance(v, str): probes.append(v)
    for x in P.get('lessons', []):
        print(' L%s [%s] %s' % (x['n'], x.get('src'), x['la'] if '--full' in sys.argv else x['la'][:70] + ' … ' + x['la'][-40:])); probes.append(x['la'][:200])
        if x.get('gospel') and '--full' in sys.argv: print('   gospel: %s | homily head: %s' % (x.get('gospel'), x.get('homily_head')))
        r = x.get('resp')
        if r: print('   R%s: %s * %s | V %s | gloria %s' % (x['n'], r['a'], r['b'], r['v'], r['gloria']))
    print(' Q:', P.get('q')); print(' info:', P.get('info'))
    pages = set()
    keys = [' '.join(nb(p).split()[2:7]) for p in probes if len(nb(p).split()) > 8]
    for f in sorted(glob.glob('/tmp/b09/ocr/%s-*.txt' % P.get('vol'))):
        t = nb(open(f, encoding='utf-8').read().replace('-\n', ''))
        if any(kx in t for kx in keys): pages.add(int(f[-8:-4]))
    print(' pages:', sorted(pages))
