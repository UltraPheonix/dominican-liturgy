"""Good Friday, 1959 view: the Communion antiphons and Ps 21 of the Cantus Gregoriani ... 1959, pp. 27-30. Idempotent."""
import json, os, re, glob
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.join(H,'..','..','..')
P=os.path.join(R,'data','holyweek.js'); s=open(P).read()
if 'op59-adoramus' in s: print('already'); raise SystemExit
lat,eng=[],[]
for f in sorted(glob.glob(os.path.join(R,'data/office/psalter/[0-9]*.json'))):
    for k,v in json.load(open(f)).items():
        ws=re.findall(r'[a-z]+',v.lower()); en=sum(w in ('the','and','of','he','his','thy','shall') for w in ws)/max(1,len(ws))>0.08
        for line in v.split('\n'):
            m=re.match(r'<n>21:(\d+)</n> (.*)',line)
            if m:
                d=eng if en else lat
                if m.group(2) not in d: d.append(m.group(2))
I=lambda t: t.replace('j','i').replace('J','I')
js=lambda d: '        '+json.dumps(d,ensure_ascii=False)+','
A=[{'r':'Ad Communiónem. Dum Sacraméntum reportátur a loco repositiónis ad altáre maius, omnes genua flectunt et cantántur hæ antíphonæ: — At the Communion. While the Blessed Sacrament is brought back from the place of repose to the high altar, all kneel and these antiphons are sung (Cantus Gregoriani … Hebdomadae Sanctae O.P. instauratum, Rome 1959, pp. 27–28):'},
 {'g':'op59-adoramus','n':'Antiphona 1 · I'},
 {'w':'C','la':'Adorámus te, Christe, et benedícimus tibi, quia per Crucem tuam redemísti mundum.','en':'We adore thee, O Christ, and we bless thee, because by thy Cross thou hast redeemed the world.'},
 {'g':'op59-perlignum','n':'Antiphona 2 · VIII'},
 None,   # the existing Per lignum line stays here
 {'g':'op59-salvator','n':'Antiphona 3 · VII'},
 {'w':'C','la':'Salvátor mundi, salva nos, qui per Crucem et Sánguinem redemísti nos: auxiliáre nobis, te deprecámur, Deus noster.','en':'Saviour of the world, save us, who by thy Cross and Blood hast redeemed us: help us, we beseech thee, O our God.'}]
B=[{'r':'Dum sacra commúnio distribúitur, cani potest psalmus 21 Deus, Deus meus, vel unum aliúdve responsórium ex Matutíno huius fériæ VI. — While Holy Communion is given, Psalm 21, Deus, Deus meus, may be sung, or one or other responsory from the Matins of this Friday (ibid., pp. 28–30).'},
 {'g':'op59-ps21','n':'Psalmus 21'}]+[{'w':'C','la':'%d. %s'%(i+1,I(la)),'en':en} for i,(la,en) in enumerate(zip(lat,eng))]
L=s.split('\n')
i0=next(i for i,l in enumerate(L) if 'Quad6f: {' in l)
iP=next(i for i,l in enumerate(L) if i>i0 and "Per lignum servi facti sumus" in l)
iC=next(i for i,l in enumerate(L) if i>i0 and 'gives Holy Communion to the faithful in the usual way' in l)
out=L[:iP]+[js(d) for d in A[:4]]+[L[iP]]+[js(d) for d in A[5:]]+L[iP+1:iC+1]+[js(d) for d in B]+L[iC+1:]
open(P,'w').write('\n'.join(out)); print('ok',len(lat),len(eng))
