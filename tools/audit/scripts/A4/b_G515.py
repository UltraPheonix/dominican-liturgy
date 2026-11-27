# ---- G515 Octave of SS. Peter & Paul pp. 488-490 (pdf 283-284): the site had the orations of the Common of Martyrs (Commune/C3a)
CONC_QV=' Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum.'
CONC_PD=' Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus, per ómnia sǽcula sæculórum.'
NEW={'or':'Deus, cuius déxtera beátum Petrum ambulántem in flúctibus, ne mergerétur, eréxit: et Coapóstolum eius Paulum tértio naufragántem de profúndo pélagi liberávit; exáudi nos propítius, et concéde, ut ambórum méritis æternitátis glóriam consequámur:'+CONC_QV,
     'se':'Offérimus tibi Dómine preces et múnera, quæ ut tuo sint digna conspéctu, Apostolórum tuórum Petri et Pauli précibus adiuvémur.'+CONC_PD,
     'pc':'Prótege Dómine pópulum tuum: et Apostolórum tuórum Petri et Pauli patrocínio confidéntem; perpétua defensióne consérva:'+CONC_PD}
PG={'or':'M39 pp. 488-489 (pdf 283)','se':'M39 p. 489 (pdf 283)','pc':'M39 p. 490 (pdf 284)'}
for f in ('or','se','pc'):
    old=F.A.O['G515'][f]
    RAW('data/orations.js',['G515',f],old,[NEW[f],''],PG[f],'WRONG PRAYER: the site had the Common of Martyrs ("N. et N."). The Missal prints the proper '+{'or':'Collect "Deus, cujus déxtera beátum Petrum" with the conclusion "Qui vivis" (Rubr. gen. XI.2, p. 52: "si ad Filium, Qui vivis et regnas cum Deo Patre")','se':'Secret "Offérimus tibi Dómine preces et múnera"','pc':'Postcommunion "Prótege Dómine pópulum tuum"'}[f]+'. Latin from the scan (i/j folded to the site\'s i-spelling); the English is left empty: it needs the 1959 wording, which I have not invented')
RAW('data/orations.js',['G515','src'],F.A.O['G515']['src'],'Missale O.P. (1939), p. 488-490 (In Octava SS. Petri et Pauli, 6 Jul.)','M39 pp. 488-490 (pdf 283-284)','source of the orations')
