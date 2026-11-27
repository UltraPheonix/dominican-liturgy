# QC: Holy Week, 1939 form (holyweek.html), checked against the Missale O.P. 1939

Read-only check. No repo file was edited. Scratch files are in /tmp/qchw_scratch.
- Data snapshot 1: data/holyweek_text.js at 12:19 CET, 27 Nov 2026.
- Data snapshot 2: the file was rewritten at 12:32:16 and again at 12:32:48 by the agents adding chant. Everything below was rechecked at 12:33–12:34. Items fixed in between are marked **[fixed 12:32]**.
- Screenshots were taken 12:25–12:31 on server :8792, using Chrome and Playwright, in the 1939 form (`#hwRite` 1939 on, localStorage `hwRite=1939`), with "Propers only" selected. The Order of Mass was also checked as "Solemn" (`#selOrdo`).
- Method: I diffed the page text word by word against the OCR (tools/orat39/m39lin.txt). For every real difference I looked at the scan (M39.pdf; pdf page = OCR @@PAGE + 1, two book pages per image).
- No JS console errors and no "could not be drawn" errors on any day, in either mode.
- Nothing post-1955 was found on the 1939 pages: no Lumen Christi, triple candle, baptismal vows or Christus heri. One indirect leak exists through `HOLYWEEK` (the 1959 data); see "All days".

Page numbers are those of the Missal (book pages).

---

## ALL DAYS (display logic, js/app.js)

**WRONG**
1. **Order of Mass on: the 1959 data feeds the 1939 page.** `drawOrdo` (app.js ~1276–1291) reads `window.HOLYWEEK[state.key]` (data/holyweek.js, the 1959 transcription) whatever `state.hwr` is:
   - `HOLYWEEK.Quad6h.canon` replaces lines inside the Canon on 1939 Thursday.
   - `HOLYWEEK.Quad6.lastGospel` and `Quad6s.alleluiaDismiss` also apply.
   - The texts happen to agree with the 1939 Missal (pp. 146, 163, 191), but they come from the 1959 book.
   - Fix: gate these on `state.hwr !== '1939'`, or take the 1939 values from HW_TEXT.
2. **Order of Mass on, Holy Saturday: the Canon shows the ordinary Communicantes and Hanc igitur.** The page shows "Communicántes, et memóriam venerántes…" and "Hanc ígitur… quǽsumus, Dómine, ut placátus" right after the proper Easter texts it has just printed. The Missal (p. 189) has "Communicantes, et noctem sacratissimam…" and "Item Hanc igitur… pro his quoque, quos regenerare dignatus es".
   - Fix: when HW_TEXT has `Infra Canonem` blocks, put them into the Canon (or drop them from the ordo Canon) for Quad6s, as is done for Quad6h.

**CLUNKY**
3. **Order of Mass on, Thursday: three texts appear twice.** The proper Communicantes, Hanc igitur and Qui pridie are printed in the propers (p. 163) and again inside the Canon. Fix: show them once, inside the Canon.
4. **Order of Mass on, Holy Saturday: two problems.**
   - The ordo "Offertorium" says "Then he says Oremus, and the Offertory", but the Missal says "nec Offertorium" (p. 188).
   - "Communio" (the priest's communion) is drawn before the rubric "Postea dicente Sacerdote Pax Domini… sed Agnus Dei non dicatur…" (pp. 189–190).
   - Fix: add an `X:` marker so the communion comes after the Pax rubric, and use a no-Offertory variant of `offerDial`.

**COSMETIC**
5. **The jump bar on Palm Sunday highlights the wrong item.** At the top of the page it marks "Agnus Dei" and is scrolled sideways, so "Benedictio ramorum" is hidden. Screenshot 12:25.
6. **Sung items inside closed folds are not drawn until the fold is opened.** These are the Tenebrae psalm tones, the Vespers and Compline psalms, the Ablutio antiphons and the Litany chant. This is by design, but in the printed booklet or a full-page capture they are blank.
   - A full-page Playwright screenshot of Thursday came out reflowed and blank (responsory boxes empty). Viewport screenshots were fine. Worth a check of print/PDF output of long days.

---

## PALM SUNDAY (Quad6, pp. 137–146)

**WRONG**: none found. The text matches the OCR word for word.

**CLUNKY**
1. **The procession rubric is printed before the procession it describes.** The rubric "Perlecto Evangelio… fiat Processio : qua finita, Prior cum ministris in sacristiam revertatur… assumptisque aliis coloris violacei… procedant more solito ad altare" (p. 139) comes before the whole "Ad Processionem" section. The Processionarium section then ends with "Prior et Ministri, ad Sacristiam redeant", so the return to the sacristy is read twice.
   - Fix: split the rubric at "fiat Processio :". Put "qua finita… ad altare" after the procession, as the end of "Ad Processionem" or at the head of "Ad Missam".
2. **The Asperges is drawn above the Blessing of Palms.** The order is right ("facta aspersione aquæ benedictæ more solito", p. 137), but it has no heading saying it belongs to this rite. Suggest a one-line rubric pointing to p. 137.

**COSMETIC**
3. **Procession chant labels disappeared at 12:32.** The procession chants lost their captions (`G op13-cumappropinquaret` and the others now have no `n`), so the "Processionarium O.P. 1913, p. …" source line is gone. Restore it if that was not deliberate.

---

## MONDAY (Quad6m, pp. 146–148)

The text matches the OCR. The Ordinary is right: Kyrie VIII, no Gloria, no Credo, Preface of the Cross in ferial tone, Agnus Dei, Benedicamus. "Humiliate capita" and "Flectamus" got chant at 12:32.

**COSMETIC**
- **lent_or.src, unclear conclusion.** "(Per Dóminum... ejúsdem.)" has an unclear ending. Write "(Per Dóminum… in unitáte ejúsdem Spíritus Sancti…)" or just "(Per Dóminum.)". The same applies on Tuesday and Wednesday.

## TUESDAY (Quad6t, pp. 148–154)

**WRONG (minor)**
- **Spelling differs from the Missal.** "convitiabántur ei" should be "conviciabántur" (p. 152, scan checked).

**CLUNKY**
- **The Passion English drops the opening phrase.** The English begins "Now the feast of the pasch…" and leaves out "At that time" (Latin "In illo témpore"). Wednesday ("Now the feast of unleavened bread…") is the same.

**CHECK**
- **Where the chants come from.** masses.js says Tuesday's Gradual, Offertory and Communion (6359/7181/5409) "were found by the incipits of the same day in the Roman Graduale". Make sure these are the Graduale O.P. melodies (they carry v28 "91/1" refs) and not Roman ones.

## WEDNESDAY (Quad6w, pp. 154–160)

**WRONG**
- **Luke 23:26 has the wrong word.** "apprehendérunt Simónem quemdam Cyrenǽum" should be "**Cyrenénsem**" (p. 159, scan checked). Mark on Tuesday correctly has Cyrenǽum.

**COSMETIC**
- **The Gradual has a period that should be a colon.** "in quacúmque die tríbulor. inclína ad me" has a period and a lower-case letter. Use a colon: "tríbulor : inclína".

---

## MAUNDY THURSDAY (Quad6h, pp. 160–166)

The Ordinary matches the Missal:
- Gloria (p. 161), Credo (p. 163), and Preface "Qui salutem humani" (p. 163).
- The proper Communicantes, Hanc igitur and Qui pridie (p. 163).
- "Dicatur Agnus Dei, sed pax non detur" (p. 163): the Agnus Dei is drawn.
- Ite missa est with blessing and "In principio" (p. 164).
- Vespers alternative (p. 165).
- Mass text, procession and Vespers match the OCR word for word.

The Tenebrae, Hours, Ablutio, Mandatum and Compline come from the Triduum O.P. 1927 (Dominican); they were not proofread here.

**WRONG (minor)**
- **"leva" should be "læva".** The rubric reads "dextera manu, et leva mundam … mappulam"; the Missal has "**læva**" (p. 164, scan checked).

**CLUNKY**
- **The Mass ends twice.** The Mass ends with Ite missa est and the last Gospel. The procession and Vespers then follow, and Vespers ends again with "…dicatur Ite Missa est… In princípio". This is the Missal's alternative ("Si vero prius Vesperæ dicantur…", p. 165), but nothing on the page says the two endings are either/or.
  - Fix: a one-line italic note before Vespers, e.g. "If Vespers are said before the end of Mass, the Postcommunion and dismissal are said after them, as follows."

## GOOD FRIDAY (Quad6f, pp. 166–179)

There is no Ordinary, Preface or Agnus. No Pax Domini and no Agnus Dei in the Presanctified (p. 178). The text matches the OCR, apart from the items below.

**WRONG**
1. **Stray "1" in the Passion Latin.** "consílium déderat Iudǽis, 1 Quia éxpedit" has an OCR "1" left in (joannes_parts.txt). Delete it.
2. **"Dicit" should be "Dixit".** "Dicit ergo Petro ancílla ostiária" should be "**Dixit** ergo Petro" (p. 168, scan checked).
3. **"et superni" should be "ut superni".** In "Flecte ramos", "nativítas et supérni membra Regis" should be "**ut** supérni" (p. 176, scan checked).
4. **"Hac" should be "Hæc".** In the rubric after Ecce lignum, "Hac eo incipiente" should be "**Hæc** eo incipiente" (p. 175, scan checked).
5. **The Tract Eripe me differs from the Missal.** "cogitavérunt advérsus me … ne umquam exalténtur" should be "advérsum me … ne unquam" (p. 167, per the OCR).

**CLUNKY**
6. **Stray capitals mid-sentence.** "Iesus Ítaque sciens" and "prætórium Íterum" should be "ítaque" and "íterum" (OCR residue in joannes_parts.txt).
7. **"Post hæc autem" is run into the previous block.** It is run in as "POST hæc autem" in caps mid-block. The Missal starts a new paragraph with a large initial and has the parenthesis "(eo quod esset discipulus Jesu, occultus autem propter metum Judæorum)" (p. 170).
   - Fix: make it its own T block with `^`, and restore the parentheses.
8. **The Improperia chant is not beside its verses.** Chant 9867 (Popule meus + Agios + Quia eduxi + Quid ultra) is drawn once, after verse 1. Verses 2 and 3 and the Agios then appear further down as plain text, between rubrics, with no notes beside them (pp. 174–175).
   - Fix: split 9867 at the verses, or add a note under the first verse: "the whole chant, with verses 2 and 3, is given above".
9. **The John Passion English adds words and drops the speaker marks.** It begins "When Jesus had said these things, he went forth…", which is not in the Latin "Egressus est Iesus". It also lacks the speaker marks (✠ C S) that the Matthew English has.

## HOLY SATURDAY (Quad6s, pp. 179–191)

The Ordinary matches the Missal:
- Kyrie and Gloria after the Litany (p. 188).
- No Credo and no Offertory (p. 188).
- Easter Preface "in hac potissimum nocte", solemn tone (p. 188).
- Proper Communicantes and Hanc igitur (p. 189).
- Pax Domini answered, no Agnus, no pax (pp. 189–190).
- Vespers, then Ite missa est, alleluia, alleluia, Placeat, blessing and In principio (p. 190).

**WRONG**
1. **The Alleluia "Confitemini" has no notes.** The block `C al 0` is in the data but is never drawn: state.parts.al is [] because `massParts` empties `al` in Lent (app.js line ~426, `if (s === 'lent') parts.al = []`), and that rule reaches Holy Saturday. Seen at 12:31 and confirmed in the DOM.
   - Fix: exempt `Quad6s` from that line.
2. **Isaias 55:11 has two wrong words.** "quod egrediátur de ore meo : Non revertátur ad me" should be "egrediétur … revertétur" (p. 185, scan checked).
3. **The Exsultet text differs from the Missal's in two words.**
   - "tuba ínsonet salutáris" should be "**íntonet**" (p. 180, scan checked; the chant above already sings íntonet).
   - "noctis, fugat scélera" should be "**purgat** scélera" (p. 181, scan checked; the chant has purgat).
   - The page now shows text and chant disagreeing a few lines apart.
4. **"Genetrícis" should be "Genitrícis".** It is in the Communicantes "…Vírginis Maríæ, Genetrícis eiúsdem Dei" (p. 189, per the OCR; Thursday correctly has Genitrícis).
5. **[fixed 12:32] The oration after Isaias was in the wrong place.** "Deus, qui Ecclesiam tuam semper Gentium vocatione" was placed after the Tract Sicut cervus; the Missal has the oration, then the Tract, then "Concede" (p. 185, scan checked). It is now right.
6. **[fixed 12:32] Lesson 4 English had an extra sentence.** It began "No weapon that is formed against thee shall prosper…", which is not in the Latin. It now begins "This is the inheritance…".

**CLUNKY**
7. **The Litany is one huge run-on paragraph.** The Missal prints one invocation per line (pp. 185–188). Split it into lines or blocks.
8. **The header says Missa I but the page sings other Masses.** The header line says "Kyriale: Missa I", but the page sings Kyrie IV and Gloria II (Triduum p. 281), with Sanctus I and Ite IV. Make the header line say what is sung, or give the Triduum's Sanctus if it names one.

**COSMETIC**
9. **A sentence lacks its period.** The Exsultet English reads "…(or King, or Duke)  Through the same…": there is no period and there is a double space.

---

## 5. Sung items without notes (as of 12:33–12:34)

**Choir chants**
| Day | Item | Where | Missal |
|---|---|---|---|
| Sat | Alleluia ℣. Confitemini (5407) | Ad Missam, after the Epistle | p. 188 (bug WRONG 1 above) |
| Fri | Improperia ℣. 2 "Quia eduxi te per desertum" and ℣. 3 "Quid ultra", and Agios/Sanctus Deus 2 and 3 | Adoratio Crucis, text between rubrics | pp. 174–175 (notes only in the 9867 block above) |
| Sat | Litany (op-lit-1..6) | in a closed fold above the plain-text Litany | pp. 185–188 (shown only on opening) |

**Celebrant, deacon and subdeacon tones (no notes anywhere on the 1939 pages)**
| Day | Items | Missal |
|---|---|---|
| Sun | Blessing of palms: Dominus vobiscum / Oremus and the oration (a chant was added at 12:32 for Dominus vobiscum · Oremus); Gospel "Cum appropinquasset"; procession oration "Omnipotens… qui humano generi"; Mass Collect, Epistle, Passion of Matthew, Secret (silent), Postcommunion | pp. 137–146 |
| Mon–Wed | Collects, 2nd and 3rd collects, Lessons/Epistles, Gospel (Mon), Passions of Mark and Luke, Postcommunions, Orationes super populum | pp. 146–160 |
| Thu | Absolution: Ne reminiscaris (said "sine nota"), versicles and Exaudi; Mass Collect, Epistle, Gospel, Postcommunion; procession oration "Deus qui nobis"; Panem de caelo | pp. 160–165 |
| Fri | Lesson Osee and Lesson Exodus (read "in tono Lectionis"); oration "Deus a quo"; John Passion; the solemn orations (only the Oremus/Flectamus intonations have notes since 12:32); "Respice" after the Adoration | pp. 166–176 |
| Sat | Blessing of fire "Domine sancte"; the 4 prophecies and their orations; Mass Collect, Epistle and Gospel; Postcommunion | pp. 179–190 |

Notes:
- The Passion tones are known to be missing: there is no Dominican source (PROGRESS.md).
- The Prefaces, Pater noster (Friday, since 12:32) and Exsultet are notated.
- With "Sung" or "Solemn" Order of Mass on, the Dominus vobiscum dialogues before the Collect and Postcommunion get tones from the ordo.
