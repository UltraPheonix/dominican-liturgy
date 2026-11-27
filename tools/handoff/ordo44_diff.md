# Ordo O.P. 1944 vs the site's Mass engine: day-by-day differences (W-F3, 27 Nov 2026)

**Scope.** Every day from 1 Jan to 30 Nov 1944 was checked.
- **Not yet checked: December** (and Oct–Nov were done before the stop order, so they are included).
- **Ordo:** /home/claude/dl/ordo44/o44.pdf. The text comes from tools/ordo44/ordo1944b.json and o44L.txt. The OCR is poor; doubtful days were read on the scan, and the pages read are cited.
- **Site:** headless-Chrome simulation of index.html with the repo files served read-only (/tmp/wf3/sim.py, output /tmp/wf3/site44.json). For each date it gives:
  - massesOf()
  - rubricsOf() (Gloria/Credo)
  - prefaceOf()
  - autoKyriale()
  - massColor()
  - prescribed() (2nd/3rd prayers)
- **Raw notes per day:** /tmp/wf3/notes.md. The listings are /tmp/wf3/mMM.txt.
- **Polish provincial feasts** (P.P. etc.) and the post-1944 supplements are marked **explained**: they are not differences to fix.
- **The site models only the conventual Mass (and the Mass outside choir).** The Ordo's variants for private Masses and for "Ubi habetur unica Missa conv." are not on the site anywhere. This is a general gap, not listed day by day.

Line format: `date | Ordo says | site gives | cause | proposed fix`.

## Rulings (Joseph, via main)
- **R1.** The proper Prefaces on the inserted leaves are KEPT: St Thomas (M39 p.137) and the Sacred Heart (M39 p.135). The Ordo's "Praef. Quadrag." on 7 Mar and "Praef. Nativ." in the SCJ octave are therefore **not** errors.
- **R2.** Apply the inserted SCJ rubric literally: "in omnibus Missis de SS. Corde Jesu et in festis Sanctorum infra Octavam". Where it is silent, follow the Ordo:
  - **Vigil of St John (23 Jun):** Praef. communis.
  - **Sunday in the SCJ octave (18 Jun):** Praef. Nativ. (M39 p.130).
- **R3.** Everything else: fix by the Missal 1939 and the Ordo 1944.

---
## A. 2nd/3rd prayers: prescribed() takes the rank of the Mass key, not the day's office (js/app.js prescribed0(), dayRank())
`dayRank(key)` uses KALRANK[massKey]:
- Temporal keys without a kalendar entry get rank '' and fall into seasonPrayers().
- Keys whose kalendar rank is I classis return "memoriae only", even on days inside their octave.
- 'Octava solemnis' is not counted as Duplex.

**Fix:** when the Mass said is the office of the day, use `mr().day(d).office.rank` / `.kind`:
- Totum Duplex / Duplex / octave days of solemn octaves: memoriae only.
- I-class *feast*: none.
- Days within an octave: the rank of that day.
- Lent/Passiontide Sundays and Holy Week ferias are I class but still take the Missal's printed 2nd/3rd prayers (see below).

| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 01-02 Holy Name (Tot.Dupl. I cl.) | "In Missa m. B. Stephanae ... In Missa conv. et cant. omitt. m. B. Steph." (no other prayer) | 2nd Deus qui salutis | no added prayer on a I-class feast (X.1 b covers only Simplex/Semid. days) |
| 01-04 Octave day of the Innocents (3 Lect.) | "2-a Or. B. V., 3-a pro Papa" (= Missal X.1 b, "Die 4 Januarii 2a Oratio erit de B. M. V., 3a pro Papa") | none (S1228 = Totum Duplex) | use the day's rank, 3 Lect. |
| 01-07, 08, 10, 11, 12 within the Epiphany octave | "In Missa (sine Sequentia) m. B. V." | none (KALRANK Epi = I cl.) | X.1 b: Deus qui salutis daily, 2 Jan to the octave day exclusive |
| 01-09 Holy Family | "Missa propr. cum mem. oct." | octave + Deus qui salutis | X.1 b: "praeterquam in festo S. Familiae" |
| 01-13 Octave day of the Epiphany | "absque mem." | A cunctis + ad lib. | octave day solemnissima = no added prayers |
| 02-27, 03-05, 03-26 Lent/Passion Sundays; 04-03 Mon, 04-05 Wed of Holy Week | "2-a et 3-a Or. (Dom. I. Quadrag.) ut in Missali" | none (temporalClass 1 → memoriae only) | the Missal prints Deus qui caritatis + A cunctis (m39lin 14733); add them for Quad1–Quad5 and Quad6m/w |
| 04-26 Solemnity of St Joseph (Tot.Dupl. I cl.) | conv. Mass with no memoria; Credo, Praef. propr. | Deus qui pro nobis + A cunctis | Pasc2w: I cl. → none |
| 07-06 Octave day of SS. Peter & Paul | "Missa propr. cum Credo, Praef. Apost." | A cunctis + ad lib. | 'Octava solemnis' counts as Duplex |
| 10-01 Rosary on Sunday (Tot.Dupl. I cl.) | "m. Dom.; Credo, Praef. B.M.V., ult. Ev. Dom." | m. Dom. + A cunctis | S1007: I cl. → memoriae only |
| 08-14 Vigil of the Assumption | "2-a Or. S. Eusebii, 3-a ad lib." | 3rd A cunctis | in a Mass of Our Lady the 3rd is ad lib. (X.1 d) |

## B. The 3rd prayer in Septuagesima–Lent (prescribed0(), seasonPrayers().with3)
Missal X.1 d (m39lin 7030–7040): with one Memoria the 3rd is A cunctis. Deus qui caritatis replaces only the ad-libitum prayer that follows a commemoration of Our Lady or All Saints.

| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 02-06 Septuagesima | "2-a Or. SS. Vedasti et Amandi, 3-a A cunctis" | 3rd Deus qui caritatis | with3 = d2; d15 only after a BVM/All-Saints memoria |
| 03-01 2nd conv. Mass, B. Christopher | "cum 2-a Or. S. Albini, 3-a A cunctis" | 3rd Deus qui caritatis | same |
| 02-16 B. Bernard Scammacca, Semid. (scan p.19 checked) | "2-a Orat. A cunctis., 3-a ad libitum" | Deus qui caritatis + A cunctis | Septuagesima to Ash Wed: feasts without memoria take A cunctis + ad lib.; ferias and Sundays take the Missal's printed pair |

## C. Sundays: the BVM suffrage at Lauds gives a 4th prayer, A cunctis (prescribed0(), the `mem.length >= 2` branch)
Missal X, preamble: "tot Orationes dicuntur, quot memoriae in Laudibus dictae fuerint, et eodem ordine". When Lauds ends "... et B. V.", the Ordo adds A cunctis after the memoriae.

| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 01-16 | "2-a Or. B. Gundisalvi, 3-a S. Marcelli, 4-a A cunctis" | first two only | add A cunctis on a Sunday with ≥2 memoriae, unless VIII.1 applies (a Totum Duplex/Duplex memoria: "omittenda est tertia Oratio", e.g. 07-30, where the Ordo has 3 prayers) |
| 01-30 | "2-a B. Mariae Mancini, 3-a S. Martinae, 4-a A cunctis" | 2 prayers | same |
| 05-14 | "2-a B. Aegidii, 3-a Crucis, 4-a A cunctis" | 2 prayers | same |
| 07-23 | "2-a B. Joannae, 3-a S. Apollinaris, 4-a A cunctis" | 2 prayers | same |

## D. Commemorations the engine drops or marks private (js/mrank.js commems / privateOnly; VIII.2)
Missal VIII.2:
- Only **I-class feasts** drop Totum Duplex and below at the conventual Mass.
- **II-class feasts** drop only 3 Lect., octaves of 3 Lect. and memoriae.
- Ferias, Sundays and octave days that are not I class are not restricted.

| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 02-14 St Catherine de Ricci (II cl.) | "2-a Or. B. Nicolai (Semid.), 3-a S. Valentini; In Missa conv. omitt. S. Valentini" | B. Nicolai private only | keep Semid. in II-class conv. Mass |
| 04-17 St Vincent Ferrer (II cl.) | "m. B. Clarae, Credo, Praef. Pasch." | private only | same |
| 02-23 Ash Wednesday | "2-a Orat. B. Petri Dam., 3-a A cunctis" | none | no VIII.2 limit on ferias |
| 03-12 Lent Sunday 3 | "2-a Or. S. Gregorii, 3-a Pro Papa" | none | Sundays are not "Festa I classis"; 3rd omitted by VIII.1 (pro Papa: see H) |
| 04-04 Tuesday of Holy Week | "m. S. Isidori ttm" | none | same |
| 04-13, 04-14 Easter Thu/Fri | "m. B. Margaritae" / "m. B. Petri" | private only | octave days Wed–Sat are not I class (Mon/Tue are: Ordo "nihil fit") |
| 05-31, 06-01, 06-02, 06-03 Pentecost octave Wed–Sat | "m. B.M.V. Omn. Grat. Mediatr." / "m. BB. Alphonsi" / "m. BB. Sadoc" / "m. BB. Petri (Sanz)", Credo | none | same |
| 01-03 B. Zedislava | "In M. mem. ut in L." = octave day of St John, **SS. Innocentium**, B.M.V. | no Holy Innocents | commemorate the day within the Innocents' octave |
| 05-26 St Philip Neri | "In Missa m. fer. (Or. Dom. praec.), Praef. Ascens. (sed non Communicantes)" | no feria | commemorate the feria after the Ascension octave (Lauds "m. fer.") |
| 09-09 Saturday of Our Lady | "(Salve sancta Parens) Gloria; 2-a Or. S. Gorgonii, 3-a ad libitum. Praef. ... Et te in Veneratione" | Ecclesiae tuae + ad lib.; engine commems empty | restore the 3 Lect. commemoration on the BVM Saturday (RESUME says this day was once right: regression) |
| 09-20 Ember Wed in choir | "cum 2-a Or. Vigil. (S. Matthaei), 3-a A cunctis" | A cunctis + ad lib. | commemorate the vigil in the feria Mass |
| 05-17 Vigil of the Ascension in choir | "de Vig. (sine Gloria) cum 2-a Or. Rogat., 3-a Crucis ... ult. Ev. Rogat. — Viol." | Crucis + A cunctis; white; label "In choir: the Rogations"; Kyrie IV | commemorate the Rogation; colour violet; label "the vigil"; no paschalKyrie() on a vigil; masses.js AscVig colour |
| 07-05 St Antony M. Zaccaria | "m. oct. et SS. Cyrilli et Methodii" | octave only; Cyril & Methodius not in kalendar39 | DOUBTFUL: may be Polish (Cracow keeps them I cl.). Check the M39 Kalendarium for July before adding |

## E. Commemorations that should NOT be made
**E1. A transferred feast is still commemorated on its impeding Sunday** (mrank.js: drop the transferred feast from commems):

| date | Ordo says | site gives |
|---|---|---|
| 02-13 Sexagesima | "2-a et 3-a Or. ut in Missali" (St Catherine de Ricci moved to the 14th) | m. St Catherine, then nothing added |
| 03-19 Laetare | "2-a et 3-a Or. Dom. I. Quadrag." (St Joseph moved to the 20th) | m. St Joseph |
| 04-05 Wednesday of Holy Week | "2-a et 3-a Or. Dom. I. Quadr." (St Vincent moved to the 17th) | m. St Vincent Ferrer |

**E2. "Hoc anno nihil fit" for memoriae / 3 Lect. inside solemnissima octaves** (Ascension, Corpus Christi, SCJ; mrank.js). Drop them, including in private Masses:

| date | Ordo says | site still commemorates |
|---|---|---|
| 05-19 | "De S. Pudentiana ... nihil fit" | Pudentiana |
| 05-25 | "nulla mem." (S. Urban) | Urban |
| 06-09 | Primus & Felician nihil fit | Primus & Felician |
| 06-12 | Basilides etc. nihil fit | Basilides |
| 06-15 | octave day, "nulla mem." (Vitus) | Vitus |
| 06-18 | Mark & Marcellian nihil fit | Mark & Marcellian |
| 06-19 | "nulla mem." (Gervasius & Protasius) | Gervasius & Protasius |

**E3. The octave day of the Trinity**

| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 06-11 Sunday in the octave of Corpus Christi | "Missa ... cum mem. oct. et S. Barnabae" | + "Dies octava: SS. Trinitas" | no octave-day commemoration of the Trinity (the Ordo commemorates the Trinity on 9 and 10 Jun, not on the 11th) |

## F. Order of commemorations (mrank.js sort)
The Ordo puts the impeded Duplex/Semid. of the day **before** the commemoration of a running octave.

| date | Ordo says | site gives |
|---|---|---|
| 06-09 | "mem. BB. Dianae ac Sod. et Trinit." | Trinity first |
| 06-10 | "mem. B. Joannis et Trinit." | Trinity first |
| 08-20 | "2-a S. Bernardi, 3-a Assumpt., 4-a S. Hyac." | Assumption, then Bernard |
| 11-05 | "2-a B. Martini, 3-a oct." | octave, then Martin |

## G. Resumed Sundays (mrank.js resumed-Sunday branch + prescribed0())
| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 01-24 (Ordo) / 01-26 (site) | Sunday resumed on Mon 24 Jan with B. Marcolinus (Semid., homily of the Sunday): "1-a Missa conv. in Choro de Dom. praec. (absque Credo) cum 2-a Or. A cunctis, 3-a ad libit. — Praef. comm. — Vir."; 2-a extra Chorum de festo | Sunday on 26 Jan, because B. Margaret's day is empty after her 1943 canonization (moved to 19 Jan) | **Explained.** But on 26 Jan the site gives no Gloria, Benedicamus, Kyrie VIII. M39 IX.2: "secus vero si Missa Dominicae resumatur ... conformantur ritui diei": check the Gloria of a resumed Sunday on a feria |
| 05-02 (in St Joseph's octave) | "de Dom. (cum Gloria et Credo) sine mem. — Praef. S. Joseph" | Crucis + A cunctis | within a solemn octave the resumed Sunday takes no added prayer |
| 10-03 (in the Rosary octave) | "de Dom. praec. (absque Credo) sine ulla mem. — Praef. B.M.V." | A cunctis + ad lib. | same |
| 07-04 (in the octave of SS. Peter & Paul) | "Missa conv. unica de Dom. praec. (dic. Gloria) cum m. oct. ttm; Praef. Apost." | A cunctis + ad lib. | commemorate the octave and add nothing else. The private alternative "de oct. cum m. Dom." lacks m. Dom. |
| 08-09 | "1-a de Dom. praec. (dic. Gloria) cum m. Vigil. ttm; Praef. oct." | A cunctis + ad lib.; the Vigil also listed as "Outside choir" | commemorate the vigil; the Vigil Mass is private only (Viol.) |
| 10-25 (in the Dedication octave) | "de Dom. praec. cum Gloria, 2-a Or. Dedic., 3-a SS. Mm. — Praef. comm." | Crispin + A cunctis | commemorate the octave |
| 07-15, 10-30, 11-14 | — | — | ok |

## H. Prayers ordered for the Anniversaries and the Pope (prescribed0() / moreAllowed())
| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 02-04 Anniv. Patrum et Matrum | "1-a Deus indulg., 2-a Deus qui nos patrem, 3-a Omnipotens" | one prayer (moreAllowed() is false for Requiem keys except C114s) | per anniversary: [Deus indulg. (own), 2nd as below, d38 Omnipotens]. Also "Ubi Missa Anniv. cantari non potest ... unica Missa de festo, in qua add. Or. Omnipotens (Rubr. VI.2)" |
| 07-12 Anniv. sepultorum | "2-a Deus, cuius miseratione" | one prayer | as above |
| 09-05 Anniv. Familiarium et Benefactorum | "2-a Deus veniae" | one prayer | as above |
| 11-10 Anniv. FFr. et Soror. (scan p.125) | "1-a et 2-a ut supra [Deus indulg., Deus veniae], 3-a Omnipotens" | one prayer | as above |
| 03-02 / 03-12 Anniversaries of the election and coronation of Pius XII | "Oratio pro Eo in omnibus Missis" | not modelled | year-dependent; optional "pro Papa" on the anniversaries |
| 10-22 Mission Sunday | Collecta pro Propagatione Fidei (S.R.C. 14 Apr 1926); in non-consecrated churches 4-a | not modelled | optional |

## I. Gloria / Credo (app.js rubricsOf, credoDay, ownFeriaMass)
| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 01-05 Vigil of the Epiphany | "Alb."; Missal p.31: Introit "... Gloria Patri. Gloria in excelsis", "Non dicitur Credo, nisi Dominica" | violet, no Gloria, Benedicamus, Kyrie VIII | Jan5a out of isVigil()/ownFeriaMass(); colour white |
| 03-31 Compassion BVM (2nd conv. Mass) | "Credo, Praef. B.M.V. (Et te in Compassione) ... Alb." | violet, no Gloria/Credo, Praef. Cruce, 2nd/3rd prayers | ownFeriaMass() regex `Quad[1-5][mtwhfs]` matches Quad5f: exclude it; masses.js Quad5f color white; PREF39 Quad5f 'B. Maria Virgine' |
| 05-27 Vigil of Pentecost | "unica Oratio (non dic. Credo)" | Credo | old branch of rubricsOf: drop Pasc6s from the Credo regex |
| 10-31 Relics (2nd conv. Mass) | "(cum Gloria et Credo) cum mem. S. Quintini" | no Credo | M39 XIV: "in ipsa Ecclesia, ubi habetur Corpus, vel insignis Reliquia": add S1031 to the Credo days |
| 09-25 Dominic in Soriano | Credo not named | Credo | **No change:** M39 XIV "In triplici festo B. Dominici" |

## J. Prefaces (app.js prefaceOf, PREF39, masses.js pref)
| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 01-25 Conversion of St Paul; 02-22 Chair of Antioch; 10-18 St Luke | "Praef. Apost." | Communis | pref 'Apostolis' for S0125, S0222, S1018 (all Apostles and Evangelists; Mark is already right) |
| 01-23 St Raymund on Sunday; 07-09 Gorkum Martyrs on Sunday; 10-22 Dedication on Sunday | "Praef. Trinit." | Communis | a feast on a Sunday with no proper Preface (and none of a season or octave) takes the Trinity Preface |
| 09-07 Thursday votives | Blessed Sacrament "Praef. Nativ."; Christ the Priest "Praef. Crucis" | Communis for both | M39 p.130: "necnon in omnibus Missis de SS. Sacramento" → PREF39 C62s 'Nativitate', C64s 'Sancta Cruce' |
| 06-23 Vigil of St John | "Praef. comm." | Corde Iesu | seasonPreface() must not give an octave Preface to a vigil Mass (R2) |
| 06-18 Sunday in the SCJ octave | "Praef. Nativ." | Corde Iesu | R2 |
| 08-14 Vigil of the Assumption | "Praef. B.M.V. Et te in Veneratione" | word "Assumptione" | bvmWord(): vigil → Veneratione |
| 03-07 St Thomas, 06-16..22 SCJ octave | Ordo Quadrag./Nativ. | proper Prefaces | **Kept by decision (R1).** No change |

## K. Colours (app.js massColor, masses.js color)
| date | Ordo says | site gives | proposed fix |
|---|---|---|---|
| 06-07 within the octave of the Trinity | Alb. | Pent1 green on weekdays | white within the octave |
| 06-11, 06-18 Sundays in the octaves of Corpus Christi and SCJ | "Alb." | green | white |
| 05-17 Vigil of the Ascension | Viol. | white | see D |
| 01-05 and 03-31 | — | — | see I |
| 03-19 Laetare | "Vl. vel Ros." | rose | ok |

## L. Weekly votive Masses (mrank.js ~line 523)
Missal Rubr. V.1: "Feria III de S. P. N. Dominico, Feria IV de S. Thoma Aquinate, et Feria V de SS. Sacramento, aut de D. N. J. C. Summo et aeterno Sacerdote ... Feria VI ... de sancta Cruce, vel pro Fratribus mortuis illo anno, vel de S. Vincentio (semel in mense)". The engine offers only Thursday.
- The Ordo offers St Thomas on Wed 19 Apr ("cum 2-a Or. Dom. praec., 3-a Crucis; dic. Gloria") and St Dominic on Tue 28 Nov ("omitt. nomen S. P. N. Dom.; dic. Gloria ... Praef. S. Dominici").
- **Fix:** add the Tuesday, Wednesday and Friday options, using the feasts' Mass forms as votives (rules: V.1 and IX.2).

## M. Kyriale (app.js autoKyriale, paschalKyrie): uses the 1960 classes; the Ordo never names a Kyriale
The headings of the Graduale O.P. 1928, Ordinarium Missae pp. 117*–136* (text layer tools/handoff/scratch/g28pages.json, idx 749–792), give the 1939-rank rule:
- I "In Festis solemnibus"
- II "In Totis Duplicibus communibus et Dominicis majoribus (Etiam Dom. infra Oct. sol. et supra; Diebus Oct. sol. et supra; et Dom. in quibus mem. Totius Duplicis vel Oct. sol. facta fuerit)"
- III "In Duplicibus et Dominicis minoribus, et infra octavas solemnissimas et solemnes"
- IV "Tempore Paschali in Dominicis et Duplicibus et supra" (the whole Ordinary, not only the Kyrie)
- V "Sabbatis, Festis et Octavis B.M.V." (Gloria "juxta solemnitatem diei")
- VI "In Semiduplicibus et Simplicibus, infra Octavas simplices et in Missis votivis"
- VII "In Festis Trium Lectionum" (Kyrie and Gloria of VI; Sanctus, Agnus and Benedicamus of VIII)
- VIII "Profestis diebus"
- XII (optional) Advent and Lent Sundays

Where the site differs:
- Totum Duplex (communia) get III or VI: e.g. 01-18, 01-25, 02-17, 03-21, 04-24, 05-06, 08-01. Should be II.
- Totum Duplex I/II cl. get II, III or VI: e.g. 01-02, 01-09, 01-23, 02-14, 04-20, 05-10, 10-04, 11-15. Should be I.
- Days within solemn octaves get I or VI (Epiphany, Corpus Christi, SCJ). Should be III.
- Octave days of solemn octaves get VI or I (01-13, 08-11, 11-08). Should be II.
- 3 Lect. days get VIII (02-03, 07-21, 09-11). Should be VII.
- Paschaltide Doubles and Sundays get Missa I/II/III with Kyrie IV. Should be Missa IV.
- Simple octaves (06-27) get I. Should be VI.
- "Festis solemnibus" is read here as Totum Duplex I and II classis. **Confirm with main.** "Dominicae majores/minores" is not defined in the Graduale; read it as privileged Sundays (Advent, Septuagesima to Low Sunday) versus Sundays per annum. **Confirm with main.**
- Maundy Thursday "ritu Toto Duplici": II by the heading (site I).

## N. Explained (no change)
- **Polish provincial feasts and ranks:**
  - 03-04 Casimir Tot. Dupl.; 05-03 BVM Regina Poloniae, the Invention moved to 05-04
  - 05-08 S. Stanislaus I cl.; 05-16 S. Andrew Bobola
  - 07-08 S. John of Dukla; 07-17/18/20 B. Ceslaus and B. Simon of Lipnica; 07-27 B. Cunegunda
  - 08-17..24 S. Hyacinth I cl. with an octave; 08-26 B.M.V. Claromontana
  - 09-01 B. Bronislava; 09-22 B. Ladislaus; 10-12 Chocim; 10-16 S. Hedwig; 10-20 S. John Cantius; 11-10 S. Stanislaus Kostka
  - Adalbert (04-23 commemoration)
- **Post-1944 supplements:** 01-19 St Margaret of Hungary (canonized 1943); 08-22 Immaculate Heart (1944).
- **Checked and right:** Requiem days (02-18, 02-21, 04-18, 09-13, 10-17, 11-27), the two-conventual-Mass days in Lent and Ember weeks, Easter and Pentecost octaves (Sequence, Credo), Saturday-of-Our-Lady prayers (02-19, 04-22, 07-29, 09-16, 10-21), 03-25, 06-24 (no Credo), 07-26 St Anne (sine Credo), 08-10 Laurence (no Credo), 08-29 Decollation (no Credo), 10-29 Christ the King, 11-12 All Saints O.P. (Praef. S. Dominici).

**December 1944 not yet checked.** To check it, run /tmp/wf3/show.py 12 (listing /tmp/wf3/m12.txt). If /tmp was cleared, the scripts must be recreated.
