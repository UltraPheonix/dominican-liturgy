import re, glob, json
from odata import *
CACHE = {}
def _scan():
    if CACHE: return
    for f in sorted(glob.glob(R + '20*/*.json')):
        D = json.load(open(f))
        for h, pairs in D['h'].items():
            for a, b in pairs:
                la = expand(T(D, a)); en = expand(T(D, b))
                for key, title in (('ps', r'<r>Psalmus (\d+)</r>'), ('ca', r'<r>(Canticum [^<]+)</r>')):
                    pass
                i = 0
                while i < len(la):
                    m = re.match(r'<r>Psalmus (\d+)</r>|<r>(Canticum Moysis|Canticum Zachariæ)</r>', la[i])
                    if m:
                        name = m.group(1) or m.group(2)
                        j = i + 1; vs = []
                        while j < len(la) and not re.match(r'<r>(Ant|Psalmus|Canticum)|<n>Glori|<r>Exod|<r>Luc|<h>', la[j]): j += 1
                        # skip ref lines
                        k = i + 1
                        while k < len(la) and (la[k].startswith('<r>Exod') or la[k].startswith('<r>Luc')): k += 1
                        j = k; vs = []
                        while j < len(la) and la[j].startswith('<n>') and re.match(r'<n>\d+:\d+', la[j]): vs.append(j); j += 1
                        if vs and name not in CACHE:
                            # english: same lines by index offset
                            eidx = None
                            for q, l in enumerate(en):
                                if l.startswith(re.sub(r'</n>.*', '</n>', la[vs[0]])): eidx = q; break
                            if eidx is not None:
                                pairs2 = []
                                for n, v in enumerate(vs):
                                    e = en[eidx + n] if eidx + n < len(en) else ''
                                    pairs2.append((re.sub(r'^<n>[\d:]+</n>\s*', '', la[v]), re.sub(r'^<n>[\d:]+</n>\s*', '', e)))
                                CACHE[name] = pairs2
                        i = j
                    else: i += 1
def psalm(n):
    _scan(); return CACHE[str(n)]
