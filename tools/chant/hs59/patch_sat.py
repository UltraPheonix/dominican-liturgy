"""Holy Saturday, 1959 view: the procession Lumen Christi and the Lauds antiphon/psalm of hs1959 pp. 33-34. Idempotent."""
import json, os
H=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(H,'..','..','..','data','holyweek.js'); s=open(P).read()
if 'op59-lumen' in s: print('already'); raise SystemExit
js=lambda d: '        '+json.dumps(d,ensure_ascii=False)+','
A=[{'r':'Ad solémnem processiónem cum céreo pascháli (Cantus Gregoriani … Hebdomadae Sanctae O.P. instauratum, Rome 1959, p. 33). Cereo benedicto, the procession is formed: thurifer, crossbearer, the deacon with the lighted paschal candle, the celebrant, subdeacon, acolytes, the brethren and the people. Having entered the church, the deacon, standing, sings alone:'},
 {'g':'op59-lumen'},
 {'w':'D','la':'Lumen Christi.','en':'The light of Christ.'},
 {'r':'All except the thurifer and crossbearer genuflect towards the blessed candle and answer:'},
 {'g':'op59-deogratias'},
 {'w':'C','la':'Deo grátias.','en':'Thanks be to God.'},
 {'r':'All rise; the celebrant lights his own candle from the paschal candle. In the middle of the church the deacon sings again, higher, Lumen Christi; all genuflect and answer Deo grátias, and the candles of the subdeacon, acolytes and brethren are lighted. A third time, before the altar in the midst of the presbytery, he sings yet higher Lumen Christi; all genuflect and answer Deo grátias, and the candles of the people and the lamps of the church are lighted. The brethren then go to their places in choir.'}]
B=[{'g':'op59-alleluia6','n':'Antiphona · VI'},
 {'w':'C','la':'Allelúia, allelúia, allelúia.','en':'Alleluia, alleluia, alleluia.'},
 {'g':'op59-ps150-laudes','n':'Psalmus 150 · tonus VI'}]
L=s.split('\n')
i0=next(i for i,l in enumerate(L) if 'Quad6s: {' in l)
i3=next(i for i,l in enumerate(L) if i>i0 and 'blesses the paschal candle, singing' in l)
iL=next(i for i,l in enumerate(L) if i>i0 and 'Lauds is sung: Psalm 150 with the antiphon' in l)
assert i3<iL
out=L[:i3]+[js(d) for d in A]+L[i3:iL+1]+[js(d) for d in B]+L[iL+1:]
open(P,'w').write('\n'.join(out)); print('ok')
