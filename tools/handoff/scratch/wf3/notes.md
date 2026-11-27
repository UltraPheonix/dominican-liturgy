# W-F3 notes (raw)
## Jan
- 01-02 Nat2: site 2nd prayer bvmNat; Ordo none in conv/sung (only m. B. Stephanae in private). cause prescribed(): dayRank('Nat2') has no rank -> seasonPrayers bvmNat; X.1 b exempts? (b: "praeterquam in festo S. Familiae"; Holy Name Tot.Dupl. I cl -> no added prayers)
- 01-03 S0103b: site [Oct S.Joan, Deus qui salutis]; Ordo "In M. mem. ut in L." = Lauds m. diei oct. S. Joan., SS. Innoc. et B.M.V. -> missing comm. of the octave of the Holy Innocents. cause mrank commems.
- 01-04 S1228 octave day (3 Lect.): site no 2nd/3rd prayers; Ordo "2-a Or. B. V., 3-a pro Papa" (= Rubr. X.1 b "Die 4 Januarii 2a Oratio erit de B.M.V., 3a pro Papa"). cause prescribed(): dayRank(S1228)=kalendar rank of the feast (dup) not the day's office (3 Lect.)
- 01-05 Jan5a: Ordo Alb.; Missal p. 31 Introit "Gloria Patri. Gloria in excelsis", "Non dicitur Credo, nisi Dominica". site violet, no Gloria, Benedicamus, Ky VIII. cause rubricsOf old branch isVigil(); massColor /Vigilia/.
- 01-07,08,10,11,12 Epi within oct.: Ordo "In Missa (sine Sequentia) m. B. V.; Credo, Praef. et Communic. de oct." site prayers none. cause prescribed(): KALRANK['Epi'] 'I classis' -> mem only (X.1 b: daily Deus qui salutis 2 Jan - oct. day excl.).
- 01-09 Holy Family: Ordo "cum mem. oct." only; site + Deus qui salutis (X.1 b excepts S. Familia). cause prescribed() bvmNat branch.
- 01-13 EpiOct: Ordo "absque mem." ; site A cunctis + ad lib. cause prescribed(): no rank for EpiOct (should be Totum Duplex octave day).
- 01-16, 01-30 Sundays: Ordo 4-a A cunctis after 2 memoriae (Lauds "m. X, Y et B. V."); site stops at 2 (X.1 e). cause prescribed() mem.length>=2.  (Rubr X preamble: "tot Orationes quot memoriae in Laudibus" - the Lauds suffrage B.V. -> A cunctis)
- 01-19 site S. Margaret of Hungary (canonized 1943, post-Ordo) vs Ordo B. Andreas a Piscaria: explained (supplement)
- 01-23 Raymund on Sunday: Ordo Praef. Trinit., ult. Ev. Dom.; site Communis. cause prefaceOf(): feast on Sunday without own preface -> Sunday's (Trinity).
- 01-24/26 resumed Sunday: Ordo 24 Jan (Marcolinus Semid, homily of Sunday) 1-a Missa conv. in Choro de Dom. praec. (absque Credo, 2-a A cunctis, 3-a ad lib., Praef. comm., Vir.); 2-a extra Chorum de festo; unica: de Dom. cum 2-a Or. festi, 3-a S. Timothei. Site: 24 = feast only; Sunday resumed 26 Jan (B. Margaret day vacant in site because of her 1943 canonization moved to 18/19 Jan). Site's 26 Jan: Epi3 with no Gloria, Ky VIII, Benedicamus. Rubr IX.2: resumed Sunday Mass follows the rite of the day -> Gloria when Te Deum.
- 01-25 Conversion S. Paul: Ordo "Credo, Praef. Apost."; site Communis. cause prefaceOf (Apostles' preface feasts).
- 01-18 Cathedra: ok Pf Apost.
## Feb
- 02-03 Blase 3 Lect: ok (sine Gloria, A cunctis + ad lib, Bened.). Kyriale VII (G28 p.136*) vs site VIII.
- 02-04 Anniv. Patrum et Matrum (2nd conv. sung): Ordo 1-a Deus indulg., 2-a Deus qui nos patrem, 3-a Omnipotens; site S1113 own collect only (moreAllowed() false for requiem keys except C114s). Also "Ubi Missa Anniv. cantari non potest ... unica Missa de festo, in qua add. Or. Omnipotens (Rubr. VI,2)" not modelled.
- 02-06 Septuagesima: Ordo 2-a Vedast & Amand, 3-a A cunctis; site 3rd Deus qui caritatis. cause prescribed(): sp.with3 'd15' for Sept-Lent; X.1 d gives Deus qui caritatis only in place of the ad-lib (i.e. when BVM/All Saints commemorated). [24 Feb/feria "2-a et 3-a Or. Dom. Septuag." = DqC + A cunctis: ok]
- 02-13 Sexagesima: Ordo "2-a et 3-a Or. ut in Missali" (St Catherine de Ricci transferred to 14th, not commemorated); site commemorates S0213 on the Sunday (and transfers it): mrank commems keeps the transferred feast. -> site 2nd = Catherine, no DqC/A cunctis.
- 02-14 Catherine de Ricci (Tot.Dupl. II cl., transferred): Ordo conv. Mass keeps m. B. Nicolai (Semid.), omits only S. Valentini; site marks B. Nicolai privateOnly. Rubr. VIII.2: in II class omit only 3 Lect./octaves 3 Lect./memoriae. cause mrank VIII.2 limits.
- 02-16 B. Bernard Scammacca Semid. (Septuagesima time, no memoria): Ordo (scan p.19 checked) "2-a Orat. A cunctis., 3-a ad libitum"; site DqC + A cunctis.
- 02-17 Translatio S. Cath. Sen. Tot.Dupl.: ok (m. B. Reginaldi, Credo).
- 02-18, 02-21 Requiem unica + private Sunday Mass: ok. ("Omitt. Tractus et dicitur tantum R." for the Sunday Mass on a feria: not checked)
- 02-22 Cathedra Antioch.: Ordo Praef. Apost.; site Communis.
- 02-23 Ash Wed: Ordo "2-a Orat. B. Petri Dam., 3-a A cunctis"; site none (engine: Peter Damian privateOnly). Ferias not limited by VIII.2.
- 02-25 Matthias in Lent: ok both Masses.
- 02-26, 02-29 two conv. Masses: ok.
- 02-27 Quad1: Ordo "2-a et 3-a Orat. ut in Missali" (Missal prints DqC + A cunctis, m39lin 14733); site none: prescribed() returns mem only for temporal class 1.
## Mar
- 03-01 S0301b (2nd conv. Mass, feast): Ordo 2-a S. Albini, 3-a A cunctis; site 3rd DqC (same with3 cause as 02-06).
- 03-02, 03-12 Anniv. election (2 Mar) / coronation (12 Mar) of Pius XII: Ordo "Oratio pro Eo in omnibus Missis" (12 Mar: 3-a Pro Papa); not modelled (year-specific; optional).
- 03-04 Casimir: Ordo Tot. Dupl. (Polish patron; P.P.) vs site Simplex -> explained (Polish rank). Site's 2nd Mass adds BVM (Sat) because of Simplex.
- 03-05 Quad2, 03-26 Quad5: Ordo "2-a et 3-a Or. Dom. I Quadrag."; site none (I-class temporal cause).
- 03-07 St Thomas Tot. Dupl. I cl.: Ordo (scan p.30 checked) "cum Gloria, Credo et Praef. Quadrag."; site Preface of St Thomas (masses S0307 pref; M39 pdf p.137 'in omnibus Missis de S. Thoma', a leaf after p.136, not in the chant Appendix of Prefaces). QUESTION for main: later grant? In Lent?
- 03-12 Quad3: Ordo 2-a Or. S. Gregorii (Dupl. imped.), 3-a pro Papa; site Gregory privateOnly, none. VIII.2 restricts I class FEASTS only; VIII.1: Sunday with Dupl. memoria omits 3rd prayer.
- 03-19 Laetare: Ordo colour "Vl. vel Ros."; St Joseph transferred to 20th, not commemorated (Lauds m. B.V. only); site commemorates S0319 on the Sunday (transferred-feast cause, as 02-13).
- 03-31 Compassion BVM (Tot. Dupl., 2nd conv. Mass extra Chorum): Ordo Alb., Credo, Praef. B.M.V. (Et te in Compassione), sine mem.; site Quad5f violet, no Gloria, no Credo, Praef. Cruce, DqC + A cunctis, Ky VIII. cause: app.js ownFeriaMass() regex Quad[1-5][mtwhfs] catches Quad5f; masses.js Quad5f color 'violet'; PREF39 lacks Quad5f -> 'B. Maria Virgine' (bvmWord Compassion already exists).
- private-Mass variants and the "Ubi habetur unica Missa conv." variants are not modelled anywhere (site shows choir/extra-choir pair only): general note.
## Apr
- 04-03 Mon, 04-05 Wed Holy Week: Ordo "2-a et 3-a Or. Dom. I. Quadr."; site none (temporalClass 1 -> mem only). 04-05 site also commemorates S. Vincent Ferrer (transferred to 17 Apr; Ordo: no memoria) -> transferred-feast cause.
- 04-04 Tue Holy Week: Ordo "m. S. Isidori ttm" (Dupl. imped.); site none (Isidore privateOnly).
- 04-06 Maundy Thu: ok (Gloria, Credo, Praef. Cruc., ritu Toto Duplici). Kyriale: ritu Toto Duplici -> II by G28 heading (site I).
- 04-09..15 Easter octave: ok (Sequence, Credo, Praef. Pasch.). 04-13 Ordo "m. B. Margaritae", 04-14 "m. B. Petri" (Semid. imped., in conv. Mass); site privateOnly -> none. (10/11 Apr I cl.: "hoc anno nihil fit" for Neyrot / S. Leo: site privateOnly, ok.)
- 04-09.. Kyriale: G28 IV "Tempore Paschali in Dominicis et Duplicibus et supra" = whole Ordinary IV; site Missa I/II/III with Kyrie IV.
- 04-16 Low Sunday ok (nulla mem.; Ite sine Allel.).
- 04-17 S. Vincent Ferrer transf. (Tot. Dupl. II cl.): Ordo "m. B. Clarae" (Semid.) in conv. Mass; site privateOnly (VIII.2 cause, as 02-14).
- 04-18 Requiem unica + private Pasc1 (2-a Crucis, 3-a A cunctis): ok.
- 04-19 Wed: Ordo conv. Mass "vel de Dom. praec.; vel Missa vot. S. Thomae Aq. cum 2-a Or. Dom. praec., 3-a Crucis; dic. Gloria" (Rubr. V.1 weekly votive); site offers only Pasc1.
- 04-23 Sunday: Ordo 2-a S. Adalberti (Polish), 3-a S. Georgii -> explained (Polish); site George + Crucis ok for 1939 calendar.
- 04-25 S. Mark + Litaniae: Ordo (with procession) 1-a conv. de Rog. (sine Gloria et Credo, 2-a et 3-a Or. Dom. I P.O.P., Praef. Pasch., Bened., Viol.), 2-a de festo (sine mem. Rog.; Credo, Praef. Apost.); without procession: one Mass de festo, m. Rog., Credo, Praef. Apost., Ev. Rog. in fine. Site: feast first ("In choir"), Litaniis "Outside choir"; the single-Mass form with m. Rog. not given.
- 04-26 Solemnity of St Joseph (Tot.Dupl. I cl.): Ordo conv. Mass no memoria (BB. Dominic & Gregory private only), Credo, Praef. propr.; site adds Deus qui pro nobis + A cunctis (prescribed(): Pasc2w has no rank -> seasonal prayers).
- 04-27..30 ok (m. oct., Praef. S. Joseph; 30 Apr Catherine on Sunday: m. Dom., Praef. Pasch., Ev. Dom.).
## May
- 05-02 resumed Sunday (Pasc3) in choir + Athanasius extra Chorum: Ordo 1-a "de Dom. (cum Gloria et Credo) sine mem. — Praef. S. Joseph"; site adds Crucis + A cunctis (DOUBTFUL: "sine mem." may mean only no memoria of feast/octave; within a solemn octave X.1 adds none). 2nd Mass ok.
- 05-03/04/08/16 Polish shifts (B.M.V. Regina Poloniae 3 May, Invention moved to 4 May, S. Stanislaus 8 May I cl., S. Andrew Bobola 16 May): explained.
- 05-14 Sunday IV P.O.P.: Ordo 2-a B. Aegidii, 3-a Crucis, 4-a A cunctis (Lauds m. Aegidii, Crucis, B.M.V.); site stops at Crucis (Sunday 4th-prayer cause).
- 05-15 Rogation Mon: ok. 
- 05-17 Vigil of Ascension (1-a conv. in Choro): Ordo "de Vig. (sine Gloria) cum 2-a Or. Rogat., 3-a Crucis — Praef. Pasch. — Bened. Domino et ult. Ev. Rogat. — Viol."; site AscVig white, 2nd/3rd Crucis + A cunctis, label "In choir: the Rogations", Kyrie IV. cause: masses.js AscVig colour, mrank label, prescribed() no Rogation commemoration on the Vigil, paschalKyrie() for a vigil.
- 05-19 S. Peter Celestine: Ordo "m. Ascens. ttm" ("De S. Pudentiana hoc anno nihil fit"); site + S. Pudentiana. 05-25 octave day: Ordo "nulla mem." ("de S. Urbano ... nihil fit"); site commemorates S. Urban. cause mrank: simple memoriae/3-Lect. not dropped within the octave of the Ascension (solemnissima).
- 05-26 S. Philip Neri: Ordo "In Missa m. fer. (Or. Dom. praec.), Praef. Ascens. (sed non Communicantes)"; site no commemoration of the feria. cause mrank: feria after the Ascension octave not commemorated.
- 05-27 Vigil of Pentecost: Ordo "unica Oratio (non dic. Credo)"; site Credo. cause rubricsOf() old branch (Pasc6s in the c regex) - engine branch skipped for Pasc6s.
- 05-31 Ember Wed in Pentecost octave: Ordo "m. B.M.V. Omn. Grat. Mediatr., Credo"; site Mediatrix privateOnly. (also 06-01 m. BB. Alphonsi, 06-02 m. BB. Sadoc - check June)
## Jun
- 06-01/02/03 Pentecost Ember days in the octave: Ordo "m. BB. Alphonsi" / "m. BB. Sadoc" / "m. BB. Petri (Sanz)", Credo; site none (privateOnly). (cause as 04-13: VIII.2 applied to octave days Wed-Sat, which are not I class)
- 06-04 Trinity ok (Kyriale: Tot.Dupl. I cl -> I; site II as Sunday).
- 06-07 De oct. SS. Trinitatis 1-o: Ordo "Missa ut in die (absque Credo); Praef. Trin." Alb.; site Pent1 green. cause massColor(): Pent1 white only on Sunday.
- 06-09 Ordo "mem. BB. Dianae ac Sod. et Trinit." (SS. Primo et Feliciano nihil fit); site Trinity first, Diana 2nd, + Primus & Felician. 06-10 Ordo "mem. B. Joannis et Trinit."; site Trinity first. 06-12 Ordo "m. B. Stephani" (Basilides etc. nihil fit); site + Basilides. 06-15 octave day "nulla mem." (Vitus nihil fit); site + Vitus. 06-18/19 (SS. Marco et Marcelliano / Gervasio et Protasio nihil fit) site commemorates them.
   cause mrank: (a) memoriae / 3 Lect. not dropped in octavae solemnissimae (Corpus Christi, SCJ, Ascension); (b) order: Semid. feast of the day before the commemoration of the octave of Trinity.
- 06-11 Sunday in oct. Corp. Chr.: Ordo "Missa ab omnib. de Dom. cum mem. oct. et S. Barnabae ... Alb."; site green and + "Dies octava: SS. Trinitas" (Ordo: no memoria of Trinity's octave day). cause massColor (Pent2 green) and mrank Trinity octave day.
- 06-16..23 Sacred Heart and its octave (and 06-18 Sunday in the octave, 06-20 B. Osanna, 06-22 B. Innocent V, 06-23 2nd Mass): Ordo "Praef. Nativ."; Missal 1939 p.130 (Praefatio de Nativitate rubric): "item in omnibus Missis SS. Cordis Jesu extra Septuagesimam et Tempus Paschale, et per ejus Octavam". Site 'Corde Iesu' (app.js prefaceOf key SCJ, seasonPreface f 68-75); the SCJ preface (M39 pdf p.135-136) contradicts p.130 (later insertion, like St Thomas p.137).
- 06-18 Sunday in SCJ octave: Ordo Alb.; site green. 
- 06-23 Vigil of St John in choir: Ordo Praef. comm.; site Corde Iesu (octave preface given to the vigil Mass). 2nd Mass (octave day) Ordo Praef. Nat.
- 06-27 within simple octave of St John: ok (Gloria, A cunctis, ad lib.). Kyriale VI by G28; site I.
- 06-28 Vigil SS. Peter & Paul + Irenaeus: ok.
## Jul
- 07-02 Visitation on Sunday: ok (conv.: m. Dom.; Credo, Praef. B.V.; ult. Ev. Dom.).
- 07-04 resumed Sunday (Pent5) within oct. Apost.: Ordo "Missa conv. unica de Dom. praec. (dic. Gloria) cum m. oct. ttm; Praef. Apost."; site Pent5 with A cunctis + ad lib (no commemoration of the octave). Private Mass "de oct. cum m. Dom." – site's S0629 alt has no m. Dom.
- 07-05 Ordo "m. oct. et SS. Cyrilli et Methodii; Praef. Apost."; site has no Cyril & Methodius at all (not in kalendar39). DOUBTFUL: may be a Polish addition (Cracow keeps them as Tot. Dupl. I cl.); check M39 Kalendarium July.
- 07-06 Octave day SS. Peter & Paul (solemn): Ordo "Missa propr. cum Credo, Praef. Apost." (no further prayers); site A cunctis + ad lib. cause prescribed(): KALRANK 'Octava solemnis' not treated as Duplex.
- 07-08 Polish S. Joannes de Dukla (Tot.Dupl. II cl.) vs site Saturday of Our Lady: explained. 07-17/18/20 Polish moves (B. Ceslaus 20 Jul, B. Simon of Lipnica): explained. 07-27 B. Cunegundis (Polish) vs BB. Joseph & Melchior (1954 supp.): explained.
- 07-09 Gorkum Martyrs (Tot.Dupl. II cl.) on Sunday: Ordo "m. Dom. (cujus Ev. in fine), Credo, Praef. Trinit."; site Communis (as 01-23).
- 07-12 Anniv. sepultorum: Ordo sung Mass "1-a Deus indulg., 2-a Deus, cuius miseratione, 3-a Omnipotens"; site S1113 one prayer (as 02-04).
- 07-15 resumed Sunday on Saturday + S. Henry: ok, both Masses match.
- 07-23 Sunday: Ordo 4-a A cunctis after B. Joanna + S. Apollinaris; site 3 prayers (Sunday 4th-prayer cause).
- others ok.
## Aug
- 08-09 resumed Sunday in choir + Vigil of St Laurence + B. John of Salerno: Ordo 1-a "de Dom. praec. (dic. Gloria) cum m. Vigil. ttm; Praef. oct. — Vir."; site Pent10 with A cunctis + ad lib (no m. Vigil.). Site also lists the Vigil Mass as "Outside choir"; Ordo: the Vigil only as a private Mass (Viol.).
- 08-11 octave day of St Dominic: ok (absque Seq. et Credo, m. S. Tiburtii, Praef. S. Dom.).
- 08-14 Vigil of the Assumption: Ordo "2-a Or. S. Eusebii, 3-a ad lib. — Praef. B.M.V. Et te in Veneratione"; site 3rd A cunctis and Preface word "Assumptione". cause prescribed(): A cunctis not dropped for a Marian vigil (X.1 d: BVM commemorated/Marian Mass -> ad lib); bvmWord() matches /Assumpt/ in the vigil title.
- 08-17..24 Polish: S. Hyacinth Tot. Dupl. I cl. with solemn octave (site II cl., no octave): explained; 08-26 B.M.V. Claromontana (Częstochowa) vs Saturday of Our Lady: explained; 08-22 Immaculate Heart (1944 supp.) vs octave day of Assumption: explained.
- 08-20 Sunday: Ordo "2-a Or. S. Bernardi, 3-a Assumpt., 4-a S. Hyac."; site Assumption before Bernard (order of commemorations: impeded Duplex before the day within an octave; cf. 06-09/10).
- others ok (06 Transfiguration Sunday Praef. Trin.; 10 Laurence no Credo, Praef. S. Dom.; 16 Joachim sine Credo; 29 Decollation no Credo).
## RULING (Joseph via main): proper Prefaces from the inserted leaves (St Thomas M39 p.137, Sacred Heart p.135) are KEPT. -> 03-07 and SCJ-octave preface lines become "kept by decision". Still open: 06-23 Vigil of St John (not a Mass of the SCJ nor a saint's feast: Ordo Praef. comm.) and 06-18 Sunday in the octave (Ordo Praef. Nat.; inserted rubric covers "omnibus Missis de SS. Corde Jesu et festis Sanctorum infra Octavam").
## Sep
- 09-01 Polish B. Bronislava (Dupl.) vs S. Giles 3 Lect.: explained.
- 09-05 Anniv. Familiarium et Benefactorum (Missa conv. unica): Ordo "1-a Deus indulg., 2-a Deus veniae., 3-a Omnipotens"; site S1113 one prayer.
- 09-07 Thursday votives: Ordo SS. Sacramento "cum Gloria, 2-a Or. Dom. praec., 3-a A cunctis ... Praef. Nativ."; Christ the Priest "... Praef. Crucis"; site both Praef. Communis (M39 p.130: "necnon in omnibus Missis de SS. Sacramento" -> Nativity). Christ the Priest preface: Ordo Crucis (no rubric found yet in M39 text; votive Mass page to check).
- Rubr. V.1 (M39 p.~6500 lines): weekly votive conv. Masses "Feria III de S. P. N. Dominico, Feria IV de S. Thoma Aquinate, Feria V de SS. Sacramento aut de D.N.J.C. Summo et aeterno Sacerdote ... Feria VI ... de sancta Cruce, vel pro Fratribus mortuis illo anno, vel de S. Vincentio (semel in mense)"; mrank.js offers only Thursday (line ~523). Ordo 19 Apr offers the Wednesday votive of St Thomas.
- 09-09 Saturday of Our Lady: Ordo "(Salve sancta Parens) Gloria; 2-a Or. S. Gorgonii, 3-a ad libitum. Praef. B.M.V. Et te in Veneratione"; site C79s 2nd Ecclesiae tuae (d7), no S. Gorgonius (engine commems empty for bvmSat on 9 Sep; RESUME says this day was checked earlier -> regression?).
- 09-20 Ember Wed + Vigil of S. Matthew (1-a conv. in Choro de feria): Ordo "cum 2-a Or. Vigil. (S. Matthaei), 3-a A cunctis"; site A cunctis + ad lib (vigil not commemorated in the feria Mass).
- 09-22 Polish B. Ladislaus vs site Ember Fri: site matches the Ordo's Warsaw-type "de ea" entry (2-a SS. Mm., 3-a A cunctis): ok.
- 09-25 Commemoration of St Dominic in Soriano: Ordo "Seq. (Laudes ergo.), Praef. S. P. Dominici" (no Credo named; Warsaw note says "dic. Credo"); M39 XIV "In triplici festo B. Dominici P. N." -> site Credo is right; no change.
- others ok.
## RULING 2: apply inserted SCJ rubric literally; where silent follow Ordo: Vigil of St John Praef. comm.; Sunday in SCJ octave Praef. Nativ.
## Oct
- 10-01 Rosary (Tot.Dupl. I cl.) on Sunday: Ordo "m. Dom.; Credo, Praef. B.M.V. Et te in solemnitate, ult. Ev. Dom."; site adds A cunctis (prescribed(): S1007 has no kalendar rank -> seasonal prayer).
- 10-03 resumed Sunday in choir within the Rosary octave: Ordo "de Dom. praec. (absque Credo) sine ulla mem. — Praef. B.M.V."; site A cunctis + ad lib. (supports 05-02: resumed Sunday inside a solemn octave takes no added prayers, X.1 "nisi facta fuerit Memoria ... Octavae solemnis").
- 10-04 St Francis: ok (Kyriale I by rank; site III).
- 10-12 (Chocim thanksgiving), 10-16 (S. Hedwig P.P.), 10-17 Requiem moved, 10-20 (S. John Cantius P.P.): Polish, explained.
- 10-18 S. Luke: Ordo "Credo, Praef. Apost."; site Communis (Evangelists: same as 25 Apr S. Mark which the site gets right).
- 10-22 Dedication on Sunday: Ordo "m. Dom., Credo, Praef. Trinit."; site Communis (feast-on-Sunday preface). Mission Sunday Collecta pro Propagatione Fidei (S.R.C. 14 Apr 1926; non-consecrated churches 4-a) not modelled.
- 10-25 resumed Sunday within the octave of the Dedication: Ordo "de Dom. praec. cum Gloria, 2-a Or. Dedic., 3-a SS. Mm. — Praef. comm."; site Pent21 [Crispin, A cunctis] (octave not commemorated).
- 10-27 Vigil of SS. Simon & Jude within the Dedication octave: Ordo "de Vigilia (sine Gloria) cum 2-a Or. Dedic., 3-a A cunctis"; site A cunctis + ad lib (label says "with a commemoration of the octave" but the prayer is missing).
- 10-29 Christ the King: ok (scan p.120 checked: m. Dom., Credo, Praef. propr., ult. Ev. Dom.).
- 10-30 resumed Sunday + B. Benvenuta: ok.
- 10-31 Relics (2nd conv. Mass extra Chorum): Ordo "(cum Gloria et Credo) cum mem. S. Quintini"; site no Credo (M39 XIV: "in ipsa Ecclesia, ubi habetur Corpus, vel insignis Reliquia").
## Nov
- 11-05 Sunday: Ordo "2-a Or. B. Martini (de Porres, Dupl. imped.), 3-a oct."; site octave first (order, as 08-20).
- 11-10 Anniv. Omnium FFr. et Soror. (scan p.125 checked): Ordo "In Missa cant. 1-a et 2-a Orat. ut supra [Deus indulg., Deus veniae], 3-a Omnipotens"; Polish S. Stanislaus Kostka makes 2 conv. Masses in Poland; site gives the Anniversary as the single conv. Mass (ok outside Poland) with one prayer (anniversary-prayers cause).
- 11-12 All Saints O.P. on Sunday: ok (scan p.126: m. Dom., Credo, Praef. S. P. Dominici).
- 11-13 Patrocinium S. Thomae: Ordo "In Missa Credo" (preface not named) -> St Thomas preface kept by decision.
- 11-14 resumed Sunday + B. John Liccio: ok.
- 11-28 Tuesday: Ordo conv. Mass "vel de Dom. praec.; vel de S. P. Dominico (ut in Missa votiva) cum 2-a Or. Dom. praec., 3-a A cunctis ... dic. Gloria ... Praef. S. Dominici"; site offers only the Sunday (Rubr. V.1 weekly votives).
- others ok.
