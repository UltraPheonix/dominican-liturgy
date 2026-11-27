# QC audit: chants of the sanctoral Masses and Commons (pre-1955 Dominican rite)

Read-only audit. Nothing in the repo was edited.
- Data snapshot: `data/masses.js` and `tools/g28/corrections.json` as of 27 Nov 2026, 12:04:53. corrections.json has 85 entries, the latest being S1009.
- Sources:
  - G50 = Graduale O.P. 1950 (OCR `/tmp/g50all.txt`, page index `index.csv`)
  - G28 = Graduale O.P. 1928 (`/tmp/g28pages.json`)
  - M39 = Missale O.P. 1939 (`tools/orat39/m39lin.txt`)
- Method: I split G50 into day sections (282) and then into feasts (304). For each feast I parsed the rubric references, the "Missa X, de Communi…, pag. N" lines and the chants printed in full, then matched them by name to the site's S\*/G\* Masses. Every automatic difference was re-read in the raw OCR, and in G28/M39 where the OCR was unclear.
- Already fixed in corrections.json or REVIEW.md is not reported again. S1009 (B. Louis Bertrand) was fixed while the audit was running and is now correct.
- Abbreviations:
  - "latent" = the wrong item is never sung on that date (for example a Gradual on a day that is always in Paschaltide), but the data is still wrong.
  - "DM" = the Mass's note says "Chants as assigned by the St. Dominic Missal (1959)".
  - The site's chant for each part is given as id «incipit» page.

---

## 1. WRONG (sanctoral, by date)

| # | Key / title | Part | Site | Source reading | Note |
|---|---|---|---|---|---|
| 1 | S0111b B. Bernard Scammacca (site 11 Jan; G50 16 Feb) | all | Common of a Confessor Bishop, Statuit: 5417 Statuit 32*, 6123 Juravit 33*, 6785 Inveni David 34*, 5857 Justus ut palma 34*, 5854 Beatus servus 32* | G50 p.432: "Missa Os justi, de Communi unius Conf. non Pont., pag. 42*." → 5885, 7142, 6895, 6021, 4856 (Tract 7125) | "guess" from his title. His readings are the Epiphany's (Isaias 60, Matthew 2) |
| 2 | S0116b B. Gundisalvus (16 Jan) | al | 6890 «Beatus vir qui suffert» 373 | G50 p.394: "Missa Justus, de Communi unius Confessoris non Pontificis, pag. 39*." Common on G50 41*: "Alleluia, V. Laetabitur, pag. 9*" → 6582. M39: "Officium Justus ut palma, de Communi Conf. non Pont., pag. 22*" | DM. 6890 is St Francis Xavier's Alleluia |
| 3 | S0121 St Agnes (21 Jan) | gr; Septuagesima Tract | gr 5531 «Adjuvabit eam» 418 (St Agatha's); Tract 6032 Veni sponsa | G50 p.402: "Missa Me expectaverunt, de Communi unius Virg. et Mart., pag. 48*." → gr 5634 Specie tua 46*; G50 49*: "Infra Septuagesimam Tractus Qui seminant, pag. 23*" → 4978. M39: "Officium Me exspectaverunt, ut in Comm. Virg. et Mart." | DM (Common No. 17) |
| 4 | S0127 St John Chrysostom | co | 5854 Beatus servus 32* | G50 p.407: "Missa In medio, in Festo unius Doctoris, pag. 35*." The Doctors' Communio is printed on G50 39*, and M39's Common of Doctors has "Communio Matth. 25 Domine, quinque talenta" → 5425 | DM (No. 12) |
| 5 | S0129 St Francis de Sales | co | 5854 | G50 p.408: "Missa In medio, de Communi unius Doctoris, pag. 35*"; M39: "Officium In medio, ut in Communi Doct., pag. 20*" → 5425 | DM |
| 6 | S0202 Purification | se (missing) | no Sequence | G50 p.416: "Alleluia, V. Adorabo, pag. 354. Sequentia Laetabundus, pag. 33. Infra Septuagesimam, omissis Alleluia, V. et Sequentia, dicitur [Tractus Gaude Maria]"; M39: "Infra Septuages. nec Alleluia, nec Sequentia dicantur" → add se 4214 Laetabundus, outside Septuagesima | |
| 7 | S0212 Seven Founders | Septuagesima Tract | 6182 «Quid mihi est» 430 (St Catherine de' Ricci's) | G50 p.426: "Infra Septuagesimam Tractus Qui seminant, pag. 23*"; M39: "Infra Septuag. Tractus Ps. 125" → 4978 | REVIEW.md called this a false positive because the day is "always in Paschaltide". 12 Feb is never in Paschaltide, and it often falls after Septuagesima |
| 8 | S0215 B. Henry Suso (site 15 Feb; G50, G28 and M39: 2 Mar) | in, al, of | Os justi Mass: 5885, 6895, 6021 | G50 p.433 (and G28 p.226): "Missa Justus, de Communi unius Confessoris non Pontificis, pag. 39*"; M39 2 Mar: "Officium Justus ut palma" → 4283, 6582, 5857 (gr 7142 and co 4856 are the same in both Masses) | corrections.json S0215 cites "G28 p.225: Missa Os justi", but that is B. Jordan's line (15 Feb), so the wrong saint's rubric was applied. DM |
| 9 | S0222 Chair of St Peter at Antioch | all, and Tract | Common of Apostles: 4899, 9858, 5348, 5848, 5171; Tract 6463 | G50 p.432: "Missa ut in festo Cathedrae Romanae ejusdem, pag. 395"; M39: "Officium Statuit, et reliqua ut in [Cathedra Romana]" → as S0118_2: 5417, 5552, 6296, Tract 7023, 7170, 5396 | "guess" |
| 10 | S0223 St Peter Damian | co | 5854 | G50 p.433: "Missa In medio, in festo unius Doctoris, pag. 35*" → 5425 | DM |
| 11 | S0228b B. Villana | Septuagesima Tract | 4978 Qui seminant | G50 p.433: "Missa Gaudeamus, de Communi unius sanctae Mulieris, pag. 59*"; G50 59*: "…praeter seq. (Infra Septuagesimam) [Tractus] Veni, sponsa Christi" → 6032 | 28 Feb always falls after Septuagesima, so this is sung every year |
| 12 | S0303b B. Peter of Geremia (site 3 Mar; G50 and M39: 10 Mar) | all | Statuit Mass (as #1) | G50 p.434: "Missa Os justi, de Communi unius Conf. non Pont., pag. 42*"; M39: "Officium Os justi, ut in Communi Conf. non Pontif." | "guess" |
| 13 | S0307 St Thomas Aquinas | co | 5854 | G50 p.434: "Missa In medio, de Communi unius Doctoris, pag. 35*"; M39 7 Mar (p.234): "Communio Matth. 25 Domine [quinque talenta]" → 5425 | DM |
| 14 | S0409b B. Antony Pavoni | of, co | 6358 Posuisti 10*, 6386 Magna est 11* | G50 p.448: "Missa Laetabitur, de Communi unius Martyris non Pont., pag. 18*." The Mass on G50 18* is "…pag. 7*, praeter Offertorium Gloria, pag. 17*, et Communionem Qui vult, pag. 17*." M39's Common of one Martyr not a Bishop (9*): "Offertorium Ps. 8 Gloria et honore … Communio Matth. 16 Qui vult" → 5797, 6924 | |
| 15 | S0410b B. Antony Neyrot | of, co | same as #14 | G50 p.448: same rubric as #14 | DM (No. 4) |
| 16 | S0423 St George (Paschaltide) | of, co, II Alleluia | of 5797, co 6924; second Alleluia 5767 Surrexit Pastor 225 | G50 p.452: "Missa Protexisti, de Communi unius Martyris non Pontificis, pag. 19*." G50 19*–20* gives Offertorium Confitebuntur and Communio Laetabitur (20*) and "Tempore Resurrectionis II. Alleluia V. Angelus, pag. 214." M39 11* agrees → 5269, 6576, 6824 | 23 Apr is almost always in Paschaltide, so this is sung |
| 17 | S0426b BB. Dominic and Gregory | co | 7015 «Ego sum vitis» 455 | G50 p.456: "Missa Justus, in festo unius Confessoris non Pontificis, pag. 39*"; M39: "Officium Justus ut palma" → 4856 Amen dico vobis 41* | DM |
| 18 | S0428b St Louis Grignion de Montfort (always in Paschaltide) | Paschaltide form missing | the season data has no Paschal Alleluias, so the app shows gr 7142 + one Alleluia 6895 | G50 p.456: "Missa Os justi … pag. 42*"; G50 42*: "Tempore Resurrectionis II. Alleluia V. Angelus, pag. 214. Tempore Ascensionis … Ascendit Deus, pag. 240" → Paschal Alleluias 6895 + 6824, Ascension 5352 | |
| 19 | S0502 St Athanasius | gr (latent) | 5522 «Ostende nobis» p.11 (an Advent gradual) | G50 p.466: "Missa In medio, pag. 35*, praeter sequens [Off. Meditabor]" → 4733 Os justi 36* | 2 May is always in Paschaltide |
| 20 | S0514b B. Giles (latent) | gr | 6123 Juravit | G50 p.476: "Missa Os justi …, pag. 42*" → 7142 | DM. 14 May is always in Paschaltide |
| 21 | S0516 St John Nepomucene | Paschaltide of, co, II Alleluia; main of/co (latent) | Paschaltide 5797, 6924, 5767; main 6358, 6386 | G50 p.476: "Missa Protexisti, de Communi unius Mart. non Pont., pag. 19*. Post Trinitatem Missa Laetabitur, pag. 18*." → Paschaltide 5269, 6576, 6824; outside it 5797, 6924 | 16 May is always in Paschaltide |
| 22 | S0527 St Bede | co | 5854 | G50 p.483: "Missa In medio, de Communi unius Doctoris, pag. 35*" → 5425 | DM |
| 23 | S0529b BB. William and companions | Paschaltide co | 6440 Posuerunt 25* | G50 p.484: "Missa Sancti tui, de Communi plurimorum Martyrum, pag. 28*" (Paschaltide); G50 30*: COMMUNIO Justorum animae → 6276 (as in C28s) | |
| 24 | S0602b BB. Sadoc and companions | Paschaltide co | 6440 | G50 p.488: same rubric → 6276 | |
| 25 | S0603 SS. Peter Sanz and companions | Paschaltide co | 6440 | G50 p.488: "Missa Sancti tui … pag. 28*. Missa Intret, pag. 25*" → 6276 | DM |
| 26 | S0610b B. John Dominici | Paschaltide form missing (10 Jun can fall in Ascensiontide) | gr + one Alleluia | Statuit Mass, G50 34*: "Tempore Resurrectionis II. Alleluia, V. Angelus, pag. 214. Tempore Ascensionis II. … Ascendens, pag. 240" → Paschal Alleluias 6785 + 6824, Ascension 5526 | rare |
| 27 | S0613 St Anthony of Padua | Paschaltide I Alleluia; Ascension Alleluia | 6895 Justus germinabit; Ascension 5352 Ascendit Deus | G50 p.490: "Missa In medio, de Communi unius Doctoris, pag. 35*" → I Alleluia 6959 Posui; M39 Doctors: "Tempore Ascens. secundum Alleluia … Ascendens Christus" → 5526 | DM. The season data was left over from the Os justi Common |
| 28 | S0702 Visitation | in | 4291 «Gaudeamus… beatae N.» 51* | G50 p.509: "Missa Gaudeamus, ut in Nativitate ejusdem B. M. V. die 8 Sept., cum nomine Visitationis, pag. 566" → 4289 | minor (the version from the Common of Virgins is used) |
| 29 | S0703 St Irenaeus (site 3 Jul; G50 28 Jun) | all | St Antony Mary Zaccaria's proper: 5436, 6775, 6558, 6990, 4814 | G50 p.502: Irenaeus's own Mass printed in full: Lex veritatis, Propter fratres, Doctrinam, Videte quoniam → 6167, 5864, 7206, 5922, 6938 (the same chants as G502) | DM (No. 10) |
| 30 | S0715 St Henry | gr | 6191 «Tibi Domine» 132 (a Lent gradual) | G50 p.520: "Missa Os justi, de Communi unius Confessoris non Pontificis, pag. 42*" → 7142 | DM |
| 31 | S0720 St Jerome Emiliani | gr | 5092 «Laudate pueri» p.40 | G50 p.523: RESPONSORIUM printed in full, "Deriventur fontes tui foras…" → 5879 (it is in the index) | |
| 32 | S0823b B. James of Bevagna | al | 6890 (Xavier's) | G50 p.560: "Missa Justus, … pag. 39*"; M39: "Officium Justus ut palma" → 6582 | DM |
| 33 | S0909 St Gorgonius | of, co | 6358, 6386 | G50 p.569: "Missa Laetabitur, ex Communi unius Martyris non Pont., pag. 18*"; M39: "Officium Laetabitur, ut in Comm. Mart. non Pont., pag. 9*" → 5797, 6924 | |
| 34 | S1002 Guardian Angels | all | St Michael's chants: 6138, 5301 (78), 5176, 5330, 6241 | G50 pp.582–586 print a proper Mass: Off. "Angelis suis Deus mandavit de te"; Resp. "Laudate Dominum Deum nostrum…"; Alleluia (M39: Ps. 33); Off. "Angeli sunt administratorii Spiritus"; Comm. "Super muros tuos Jerusalem" | none of these is in GregoBase. Needs transcription from G50 |
| 35 | S1010b B. Matthew Carreri | gr, al | 6123 Juravit, 5400 «Diligam te» 286 | G50 p.595: "Missa Os justi, de Communi unius Confessoris non Pontificis, pag. 42*" → 7142, 6895 | DM |
| 36 | S1015 St Teresa of Avila | all | 5331 «Dedit illi» 409 (St John Bosco's), 4733, 6959, 5857, 5425 | G50 pp.601–603 print a proper Mass: "Dedit ei Dominus sapientiam…", Resp. "Danti mihi sapientiam…", "Alleluia V. Declaratio sermonum tuorum", Off. "Factus est in corde meo…", Comm. "Misericordias Domini in aeternum cantabo" | not in GregoBase. Needs transcription. "guess" |
| 37 | S1024 St Raphael | gr | 6214 «Benedicite Dominum omnes» 437 | G50 pp.604–605: RESPONSORIUM printed in full, "Laudate Dominum de caelis… V. Laudate eum omnes Angeli ejus" | DM. Not in GregoBase |
| 38 | S1107b B. Peter of Ruffia | of, co | 6358, 6386 | G50 p.613: "Missa Laetabitur, de Communi unius Martyris non Pontificis, pag. 18*" → 5797, 6924 | DM (No. 4) |
| 39 | S1111 St Martin of Tours | gr | 6123 Juravit | G50 p.614: "Officium Statuit, pag. 32*. Responsorium Inveni David, pag. 12*" → 6727 | |
| 40 | S1115 St Albert the Great | gr, al | 4733 Os justi, 6959 Posui | G50 p.616: "Missa In medio … pag. 35*, praeter sequentia:" then printed: Resp. "Ecce sacerdos magnus … V. Inventus est justus…" and "Alleluia V. Vere magnus est in caelis Albertus…"; M39: "Alleluia … Vere" | DM. Not in GregoBase |
| 41 | S1117 St Gregory Thaumaturgus | gr, al, of | 6123, 6785, 5857 | G50 p.617: "Officium Statuit, pag. 32*. Responsorium Inveni David, pag. 12*. Alleluia V. Posuisti, pag. 13*. Offertorium Veritas mea, pag. 31*. Communio Beatus servus" → 6727, 4966, 7170 | DM. REVIEW.md fixed only the Communio |
| 42 | S1124 St John of the Cross | co | 5854 | G50 p.620: "Missa In medio, de Communi …, pag. 35*"; M39: "Officium In medio, ut in Communi Doctoris" → 5425 | DM |
| 43 | S1126b B. James Benfatti | co | 6516 Fidelis servus 374 | G50 p.620: "Missa Statuit, de Communi unius Conf. et Pont., pag. 32*" → 5854 | DM. A stray Lent Tract 6154 «Domus mea» is also there (latent) |
| 44 | S1202 St Bibiana | in | 8003 Loquebar 45* | G50 p.371: "Officium Me exspectaverunt, de Communi unius Virg. et Mart., pag. 48*. Reliqua ex Missa Loquebar, pag. 45*." → 5273 | DM (No. 16) |
| 45 | S1203 St Francis Xavier | al | 5359 «Beatus vir qui timet» 407 | G50 p.373: printed "Alleluia V. Beatus vir, qui suffert tentationem…"; M39: "Alleluia … Jac. 1" → 6890 | DM. 6890/5359 are swapped among #2, #32 and #45 |
| 46 | S1228 Holy Innocents | al (with the app's logic) | al = 5585 «Herodes» 391 | G50 p.391–392: after the Gradual "Laus tua Deus. V. Herodes iratus…"; "Si Dominica fuerit et in die Oct., loco Laus tua, dicitur Alleluia V. Hi sunt…" (5538, 392); M39: "Loco Alleluia, dicatur Laus tua Deus" | The app empties `al` on weekdays, which drops "Laus tua", the chant prescribed for weekdays. On Sundays it shows "Laus tua" instead of Hi sunt. DM |

## 1b. WRONG (Commons)

| Key | Part | Site | Source reading |
|---|---|---|---|
| C93s Pro fidei propagatione | co | 4994 «Domine Dominus noster» p.99 | G50 (votive section; OCR page about 98*): COMMUNIO printed in full, "Laudate Dominum, omnes gentes…" → 4900 (index 98*) |
| C104s Pro vitanda mortalitate | gr missing; al list | no gr; al list [5286, 5433, 6408] | G50: "Responsorium Misit Dominus, pag. 49." → 6504. 6408 Adjuva nos (108*) belongs to "Pro remissione peccatorum". The correct Alleluias are 5286, with 5433 as the second Paschal Alleluia |

## 2. DOUBTFUL

| Key | Part | Issue |
|---|---|---|
| S0319 St Joseph (19 Mar) | main al 7042 Amavit eum | G50 p.434 gives only "Tempore Paschali … Alleluia V. Joseph fili David … II. Alleluia V. In die, pag. 211". The Alleluia for votive Masses outside Paschaltide is "Fac nos innocuam, pag. 367" (G50 p.368). 7042 has no source. It is never sung on 19 Mar |
| S0428 St Paul of the Cross | all | Not in G50 (28 Apr is St Louis de Montfort only) and not in M39. The site gives a St Dominic Missal 1959 mixture that borrows St Peter Martyr's Alleluia 5207 and Communio 7015. By the site's rule ("absent from the Missal → blank") this should be blank |
| S0508 BVM Mediatrix (site 8 May; G50 31 May, pp.484–487) | gr, tr missing | The chants match the G50 Mass of 31 May, but gr 6822 «In me gratia» 485 and Tract «Ego sum radix» 486 are missing. On the pre-1955 date (31 May) the feast can fall after Paschaltide |
| S0916, S1009_2, S1031 | co | Site 20961 «Gaudete justi» p.612 (All Saints). G50 prints Gaudete justi on p.575 (16 Sept), and St Denis (p.596) and the Relics (p.606) both refer to "pag. 575". The p.575 chant is not in GregoBase, so it is unverified that the melody is the same |
| S0925 Commemoration of St Dominic at Soriano | se | The site has «Laudes ergo», the sequence of the votive Masses. G50 p.579 and G28 p.296: "Omnia ut notatur in principali Festo ejusdem, pag. 533" → In caelesti hierarchia (5838). M39: "Omnia ut in Missa ejus, quae dicitur Feria iij, inter votivas posita, pag. 64*". The books disagree |
| C7s "Commune unius Martyris" | title / structure | G50 7* is "In Festo unius Martyris **et Pontificis** … Prima Missa". The site has no Common for a Martyr not a Bishop: neither 18* (Laetabitur + Gloria/Qui vult) nor 19* (Paschaltide: Protexisti + Confitebuntur/Laetabitur, II Alleluia Angelus). This is the root cause of #14, 15, 16, 21, 33 and 38 |
| C51s "Commune Sanctarum Mulierum" | title | G50 51* is "In Festo unius Virginis non Martyris". The holy-women Mass (59*) is this Mass plus Tract Veni sponsa |
| C25s | al | The main al list includes 5648 Sancti et justi, which belongs to the Paschaltide Mass (28*). The app drops it outside Paschaltide, but in Paschaltide this Common has no Paschal season data, so it would show gr + two Alleluias |
| C62s, C64s, C68s, C82s, C85s, C89s, C93s | season data | The Paschaltide/Ascension II Alleluias printed in G50 are missing: C62s/C68s Surrexit Christus 222; C82s Surrexit 205; C85s/C89s Ego sum Pastor 222; Ascendens 240 for C64s and C93s |
| C110s | of 6005 In te speravi 317 | Not verifiable: the OCR file ends on the first page of this Mass |

## 3. OK, but needs explaining

- **S0203 St Blaise.** G28 says "…Martyris et Pontificis, pag. 7*", but G50 says "pag. 18*" and M39 gives Off. Gloria et honore, Comm. Qui vult, and "Infra Septuagesimam non dicitur Tractus". The site follows G50 and M39.
- **S0201 St Ignatius, S1229 St Thomas Becket.** Both are bishops, but G28, G50 and M39 all prescribe the Mass for a Martyr not a Bishop (18*). The site is correct.
- **S0325 Annunciation.** The main co is 6887 Ecce Virgo (Advent, p.23); G50 prints it on p.445 (5369, which is used in Paschaltide). Presumably the same melody.
- **S0914 Exaltation of the Cross.** The site uses in 6834 Nos autem from p.169 (Holy Thursday). G50 says "ut in Festo Inventionis … post Trinitatem, pag. 467" (that page has 7245, with alleluias). Check that the post-Trinity form is the same melody.
- **S1024 St Raphael.** G50 reprints "In conspectu Angelorum" and "Stetit Angelus" on pp.604–605; the site uses St Michael's copies (473, 439).
- **S0821 St Jane Frances de Chantal.** G50 says Common of a Virgin, M39 says holy woman. The only difference is the Septuagesima Tract, which does not matter on 21 Aug.
- **S1003 St Thérèse and S1004 St Francis.** Their notes say the chants are "not in the Graduale O.P. of 1950", but G50 prints them (p.586 and pp.587–595) and the site uses op-g50 transcriptions. The notes are out of date.
- **S0811b.** The note says "Proper Mass, Graduale p.543", but G50 p.542 says "Missa Os justi … 42*". The chants are correct.
- **S0920v.** The Introit is labelled p.571; G50 prints it on p.576.
- **S0910_2 St Nicholas of Tolentino.** Not in G50; M39 gives a proper Mass. The site's choice of Introit and Gradual is explained in its note.
- **C68s.** The Alleluia "Ave, Rex noster" is typeset from G28 66* (it is G50 70*, not in GregoBase).
- **Stray "latent" data that is never sung:**
  - Lent Tracts: S0511 (6801), S0825/S1104/S1111/S0914 (6325, which belongs to St John Bosco), S0819b (4978, a Virgin's Tract for a Confessor; G50 puts him on 6 Mar, when it would be sung).
  - Paschal Alleluia: S1030b (7399 Potestas ejus, which belongs to Christ the King).
- **G-keyed Masses.** G420, G475 and G385 are untied proper Masses (Lourdes, Imelda, St Stephen) whose notes wrongly say "Common No. 18/22".
- **Calendar dates that differ from G50 (chants unaffected):** S0111b, S0119b, S0214/S0216b, S0215, S0303b, S0419b, S0503b, S0508, S0511 (G50 1 May), S0703, S0811b, S0819b, S0905b, S1007 (G50 first Sunday of October), S1010b, S1127b.

## 4. Out of scope (not in the 1950/1928 books)

- Beatified or canonised after 1950: S0110b, S0401b, S0508b, S0516b, S0521b, S0620bx, S0704b, S0718b, S0727 (BB. Joseph and Melchior, 1951), S0727b, S0812b, S0813b, S0902b, S0906b, S0907b, S1006b, S1014b, S1019b, S1030bx, S1119b, S1209b.
- Not in the Dominican books at all: S0708b (Fortescue).
- Post-1954 feasts: S0501 (St Joseph the Worker, which uses Roman-melody chants r646/r26/r28), S0531 (Queenship of Mary), S0903 (St Pius X).

## 5. Readings flagged `roman: True`

207 Masses in all; 112 are sanctoral, Commons or votive. Full list: `/tmp/qc/roman.txt`.
- Sanctoral and G-keyed: S0102b, S0103b, S0110b, S0111b, S0119b, S0120, S0125, S0130b, S0201, S0205, S0207, S0211, S0212, S0214, S0222, S0224, S0228b, S0303b, S0308, S0309, S0317, S0319, S0321, S0323b, S0325, G446, S0327, S0401b, S0409b, S0413b, S0427b, S0504, G470, S0508, S0508b, G475, S0512b, S0516, S0520b, S0521b, S0524, G481, S0526, S0528b, S0529b, S0530b, S0602b, S0604, S0606, S0610b, S0614, S0620b, S0620bx, S0622b, G499, S0626, G502, G502_3, S0701, S0703_2, S0704b, S0705, G515, S0707b, S0708b, S0710, S0713b, S0716, S0719, S0721, S0722, S0723b, S0726, S0727, S0727b, S0731, S0802, S0803b, S0805, S0806, S0808b, S0810, S0812, S0813b, S0816, S0821, S0822, S0827, S0901, S0904b, S0905b, S0907b, G555, S0908, S0909, S0911, S0920, S0921, S0924, S0927, S0929, S1001, S1004, S1005, S1008, S1011b, S1013b, S1014b, S1101, S1114b, S1116b, S1117, S1119, S1119b, S1121, S1125, S1127b, G369, S1130, S1203, S1206, S1209b, S1220, S1221, S1222, G385, G505.
- Commons and votive Masses: C1s, C7s, C18s, C21s, C30s, C32s, C51s, C55s, C62s, C64s, C68s, C75s, C82s, C85s, C89s, C93s, C104s, C110s.
- Temporal (about 90): Advent, Lent ferias, Sundays after Pentecost, and others.
- Readings that clearly don't fit the saint:
  - S0111b: Epiphany readings for a confessor.
  - S0708b: Proverbs 31 ("Mulierem fortem") for a male martyr.
  - S0803b: St Stephen's Epistle (Acts 6–7) for a confessor bishop.
  - S1011b: Marian readings (Ecclus 24, Luke 2:43) for a confessor.
  - S1127b: Marian readings (Apoc 12, Cana) for a widow.
  - S1114b: a bishop's readings for a confessor who was not a bishop.
  - S0119b and S1005: martyrs' readings (Heb 10:32–38, Luke 12:1–8) for confessors.

## 6. Masses noted "St. Dominic Missal (1959)" whose chants differ from G50 or M39

165 Masses carry the note. These 26 differ from the books: S0116b, S0121, S0127, S0129, S0215, S0223, S0307, S0410b, S0426b, S0428, S0514b, S0527, S0603, S0613, S0703, S0715, S0823b, S1010b, S1024, S1107b, S1115, S1117, S1124, S1126b, S1202, S1203, S1228 (plus S0319 as DOUBTFUL). The other 1959-noted Masses agree with G50.

---

## Summary

- **Checked:** 304 G50 feasts matched to 319 S\* Masses and 32 C\* Commons, plus the dated G-keyed Masses.
- **WRONG:** 46 sanctoral Masses (12 of them affect only Paschaltide or Septuagesima variants; 4 are latent) and 2 Commons.
- **DOUBTFUL:** 10 entries (4 Masses, 3 that share one Communio, 4 Common or votive-set issues, and 1 unverifiable).
- **OK but needs explaining:** about 14 entries, plus a group of latent stray data.
- **Out of scope:** 25 Masses.
- **Roman readings:** 207 Masses carry `roman: True`.

**The 10 most important problems**
1. **The Doctors' Communio is wrong in 7 Masses.** S0127, S0129, S0223, S0307 (St Thomas Aquinas), S0527, S1124 have Beatus servus where the Common of Doctors has Domine quinque talenta (5425). S0613 has the wrong Paschal Alleluias.
2. **The Common for a Martyr not a Bishop is missing** (G50 18*/19*). Because of this, S0409b, S0410b, S0909 and S1107b have the wrong Offertory and Communion, and S0423 and S0516 have the wrong Paschaltide chants. A common "Laetabitur + Gloria/Qui vult" and a Paschaltide "Protexisti + Confitebuntur/Laetabitur" are needed.
3. **Whole Masses are taken from the wrong saint or Common:** S0703 (Irenaeus has St Antony Mary Zaccaria's Mass), S0222 (Chair at Antioch has the Apostles' Common), S0111b and S0303b (a bishop's Common for confessors who were not bishops).
4. **Proper Masses printed in G50 are replaced by borrowed chants:** S1002 Guardian Angels, S1015 St Teresa, S1115 St Albert (gr, al), S1024 St Raphael (gr). These need transcription from G50 pp.582–586, 601–603, 616–617 and 604–605.
5. **Septuagesima Tracts that are actually sung are wrong:** S0212 (REVIEW.md had dismissed it), S0228b and S0121.
6. **St Henry Suso (S0215)** uses the Os justi Mass instead of Justus; the earlier correction took B. Jordan's line.
7. **Wrong Alleluias in three Masses:** S0116b and S0823b have Xavier's Alleluia, and S1203 (Xavier) has Nolasco's.
8. **The Purification (S0202) has no Sequence Laetabundus**, which G50 and M39 both prescribe.
9. **Wrong single Graduals or Introits:** S0715 (a Lent gradual), S0720 (Deriventur 5879 exists and isn't used), S1010b, S1111, S1117, S1202, S0502, S0514b.
10. **Paschaltide forms:** the Communio of BB. William, Sadoc and Peter Sanz (S0529b, S0602b, S0603) should be Justorum animae. S0428b and S0610b have no Paschaltide Alleluias. For the Holy Innocents (S1228), "Laus tua" is dropped on weekdays.
