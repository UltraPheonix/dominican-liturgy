# ---- S1004 St Francis (Totum Duplex I cl.) pp. 580-582 (pdf 329-330)
import copy
assert len(F.A.RD['S1004'])==1
_ep=copy.deepcopy(F.A.RD['S0917'][0])
_go=copy.deepcopy(F.A.RD['S1004'][0])
for o,n in (('Confíteor tibi Pater,','Confíteor tibi, Pater,'),('a sapiéntibus, et prudéntibus','a sapiéntibus et prudéntibus')):
    assert _go['la'].count(o)==1; _go['la']=_go['la'].replace(o,n)
RAW('data/readings33.js',['S1004'],F.A.RD['S1004'],[_ep,_go],'M39 pp. 580-581 (pdf 329)','EPISTLE MISSING: readings33 had the Gospel only, so the app showed a Bible text for the Epistle; the Missal prints Gal 6:14-18 "Mihi autem absit gloriári" (the same text as S0917, p. 561, identical on p. 580). Gospel as printed: "Confíteor tibi, Pater"; "a sapiéntibus et prudéntibus"')
SUB('data/masses.js',['masses','S1004','note'],[(F.A.D['masses']['S1004']['note'],'Missale O.P. (1939), pp. 580-582 (Totum Duplex I classis): Officium Gaudeámus (beáti Francísci); R/. Quasi stella; Allelúia O Patriárcha; Sequentia Sanctitátis nova signa; Offertorium Magnificábitur; Communio Non sunt condígnæ. Chant: Graduale O.P. 1950 pp. 587-595.')],'M39 pp. 580-582 (pdf 329-330)','the old note was wrong: the gabc headers show that every chant is read from the Graduale O.P. 1950 (pp. 587-595), not from the Franciscan Graduale, and the Gradual is proper (Quasi stella), not from the Common')
