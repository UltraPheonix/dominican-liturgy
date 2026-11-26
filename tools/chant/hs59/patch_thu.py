"""Holy Thursday, 1959 view: the Communion psalms (Ps 22, 71, 103, 150) of the Cantus Gregoriani ... 1959, pp. 19-25.
First verse notated as printed; the other verses from the site psalter (data/office/psalter, Latin j written i)."""
import json, os, re, glob
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..')
P=os.path.join(R,'data','holyweek.js'); s=open(P).read()
if 'op59-ps22' in s: print('already'); raise SystemExit
lat,eng={}, {}
for f in sorted(glob.glob(os.path.join(R,'data/office/psalter/[0-9]*.json'))):
    for k,v in json.load(open(f)).items():
        for line in v.split('\n'):
            m=re.match(r'<n>(\d+):(\d+)</n> (.*)',line)
            if not m: continue
            ps=m.group(1); t=m.group(3)
            if ps not in ('22','71','103','150'): continue
            ws=re.findall(r'[a-z]+',v.lower()); en=sum(w in ('the','and','of','he','his','thy','shall') for w in ws)/max(1,len(ws))>0.08
            d=eng if en else lat
            if t not in d.setdefault(ps,[]): d[ps].append(t)
def I(t): return t.replace('j','i').replace('J','I')
lines=[{'r':'Dum célebrans sacram Communiónem distríbuit, cantátur antíphona ad communiónem Dóminus Iesus. Iuxta númerum communicántium addi possunt psalmi 22, 71, 103 et 150, ea ratióne ut antíphona post síngulos psalmos vel post síngulos aut binos versus cuiúsque psalmi repetátur, omísso hódie Glória Patri. — While the celebrant gives Holy Communion, the Communion antiphon Dóminus Iesus is sung. According to the number of communicants Psalms 22, 71, 103 and 150 may be added, the antiphon being repeated after each psalm, or after every one or two verses of each psalm; the Glória Patri is omitted today. (Cantus Gregoriani … Hebdomadae Sanctae O.P. instauratum, Rome 1959, pp. 19–25.)'}]
for ps,g in [('22','op59-ps22'),('71','op59-ps71'),('103','op59-ps103'),('150','op59-ps150')]:
    L,E=lat[ps],eng[ps]
    # Ps 71 begins (v.1) with the title "Deus, iudicium tuum regi da"? keep as in the psalter
    lines.append({'g':g,'n':'Psalmus %s'%ps})
    for i,(la,en) in enumerate(zip(L,E)):
        lines.append({'w':'C','la':'%d. %s'%(i+1,I(la)),'en':en})
    lines.append({'r':'Et repetitur antiphona Dóminus Iesus. — And the antiphon Dóminus Iesus is repeated.'})
sec={'at':'afterCo','la':'Ad Communionem','en':'At the Communion','lines':lines}
i=s.index('  Quad6h: {'); j=s.index('sections: [',i)+len('sections: [')
s=s[:j]+'\n      '+json.dumps(sec,ensure_ascii=False)+','+s[j:]
open(P,'w').write(s); print('ok',{k:(len(lat[k]),len(eng[k])) for k in lat})
