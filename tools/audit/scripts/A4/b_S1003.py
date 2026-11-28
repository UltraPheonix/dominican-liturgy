# ---- S1003 St Teresa of the Child Jesus, "IN MISSIONIBUS" leaf pp. 634-635 (pdf 356)
PG='M39 pp. 634-635 "IN MISSIONIBUS" (pdf 356)'
SUB('data/orations.js',['S1003','or',0],[('regnum cœlórum: da nobis, quǽsumus: ita sanctæ Teresiæ','regnum cælórum: da nobis, quǽsumus; ita sanctæ Terésiæ'),('ætérna. Qui vivis','ætérna: Qui vivis')],'M39 p. 634 (pdf 356)','the site had the Divinum Officium pointing; as printed: "cælórum : da nobis, quǽsumus; ita sanctæ Terésiæ"; "ætérna : Qui vivis" (addressed to the Son, Rubr. gen. XI.2 p. 52 "si ad Filium, Qui vivis")')
SUB('data/orations.js',['S1003','se',0],[('concíliet: ut, in cuius honóre sollémniter','concíliet: ut in cuius honóre solémniter')],'M39 p. 635 (pdf 356)','as printed: "concíliet : ut in cujus honóre solémniter exhibétur"')
SUB('data/orations.js',['S1003','pc',0],[('Illo nos, Dómine amóris igne cœléste','Illo nos, Dómine, amóris igne cæléste'),('sancta Teresia Virgo','sancta Terésia Virgo')],'M39 p. 635 (pdf 356)','as printed: "Illo nos, Dómine, amóris igne cæléste"; "Terésia"')
RAW('data/orations.js',['S1003','src'],'Sancti/10-03','Missale O.P. (1939), p. 634-635 (In Missionibus)',PG,'source of the orations (checked on the scan)')
SUB('data/readings33.js',['S1003',0,'la'],[('Dicit Dóminus: Ecce','Hæc dicit Dóminus: Ecce'),('germinábunt: et cognoscétur','germinábunt, et cognoscétur')],'M39 p. 634 (pdf 356)','as printed: "Hæc dicit Dóminus : Ecce"; "germinábunt, et cognoscétur"')
EN('S1003',0,[('For thus saith the Lord:','Thus saith the Lord:')],'M39 p. 634 (pdf 356)','the Latin is "Hæc dicit Dóminus" (no "For")')
G=F.A.RD['S1003'][1]
NL=G['la'][:G['la'].index(' Et qui suscéperit')].replace('Quis putas, major','Quis, putas, major')
NE=G['en'][:G['en'].index(' And he that shall receive')]
RAW('data/readings33.js',['S1003',1,'la'],G['la'],NL,'M39 p. 635 (pdf 356)','the Missal prints Matth 18:1-4 only (ending "hic est major in regno cælórum."); the site had vv. 1-10 (the Guardian Angels\' Gospel); also "Quis, putas, major" as printed')
RAW('data/readings33.js',['S1003',1,'en'],G['en'],NE,'M39 p. 635 (pdf 356)','cut to vv. 1-4, as the Latin')
RAW('data/readings33.js',['S1003',1,'ref'],G['ref'],'Matthæus 18: 1-4','M39 p. 635 (pdf 356)','the Missal prints vv. 1-4 (masses.js already says 18: 1-4)')
SUB('data/masses.js',['masses','S1003','title'],[('Infante, V. D.','Infante, V.')],'M39 p. 634 (pdf 356)','the Missal: "S. TERESIÆ A JESU INFANTE Virginis" (she was declared a Doctor only in 1997)')
SUB('data/masses.js',['masses','S1003','en'],[('Infante, V. D.','Infante, V.')],'M39 p. 634 (pdf 356)','as the Latin title')
SUB('data/masses.js',['masses','S1003','name_en'],[('St. Therese of the Child','St. Therese of the Child Jesus')],'M39 p. 634 (pdf 356)','the English name was cut ("of the Child")')
SUB('data/masses.js',['masses','S1003','note'],[(F.A.D['masses']['S1003']['note'],'Missale O.P. (1939), pp. 634-635 ("In Missionibus", Totum Duplex I classis): Officium Veni de Líbano; R/. Confíteor tibi; Allelúia Quasi rosa; Tract Jam hiems; Offertorium Magníficat; Communio Circumdúxit. Chant: the Graduale O.P. 1950 insert pp. 586¹-586⁶.')],PG,'the old note was wrong: the chants are read from the G50 insert pp. 586¹-586⁶ (see the gabc headers), not from the Graduale Romanum, and the Missal\'s Alleluia is Quasi rosa (Eccli 39), not In humilitate')
