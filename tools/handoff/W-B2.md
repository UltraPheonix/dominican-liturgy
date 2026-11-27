# W-B2: Holy Week 1939 tones, Palm Sunday to Wednesday (stopped 27 Nov 2026)

## State
- Generator: `tools/hw39/gen_quad6.js`. It covers all four days, and each item carries its book, page, rubric and tone.
- 26 gabc files written, and all compile in gregorio without errors:
  - `gabc/op-hw-quad6-1..6`
  - `gabc/op-hw-quad6m-1..9, 11`
  - `gabc/op-hw-quad6t-1, 2, 3, 5`
  - `gabc/op-hw-quad6w-1, 2, 4, 5, 6, 8`
- **Not wired.** No G: lines were inserted and no .src file was changed. build.py and the Chrome test have not been run.
- **Not yet checked by a second reader against the scan.** I checked these by eye only:
  - the DV and Oremus of Proc. p. 404 (300 dpi);
  - the tone III conclusion and Amen, p. 408;
  - the pointing on Proc. pp. 20-21, 23-24 and 33.
- Engine: Lead B's OPMassTones.*Proc in js/mtones.js (declared STABLE).

## Resume
1. `node tools/hw39/gen_quad6.js` (dry run). Add `SHOW=1` to print the gabc.
2. `node tools/hw39/gen_quad6.js --write`
3. `cd /tmp && gregorio -o x.gtex /abs/gabc/op-hw-quad6*.gabc`
4. Second pass against the scan. Settle the questions below first.
5. `node tools/hw39/gen_quad6.js --insert`. It re-reads each .src right before each insertion, adds only G: lines, and skips any that are already there.
6. `python3 tools/hw39/build.py`
7. Headless Chrome on `holyweek.html#Quad6&d=2027-03-21` and on Quad6m, Quad6t and Quad6w (d = 03-22 to 03-24), with localStorage hwRite=1939. Check for console errors and for anything that failed to draw.

## Inventory (Missale O.P. 1939 pages; Proc. = Processionarium O.P. 1913)
| item | file / G placement | tone | rubric |
|---|---|---|---|
| Palm: DV + Orémus of the blessing | already op13-palm-benedictio-dv | III | Proc. p. 20 |
| quad6-1 Blessing *Omnípotens sempitérne Redémptor* (pp. 137-138) | Quad6.src, before the T ^OMNIPOTENS sempitérne Redémptor | III, book pointing | Missal p. 137 "benedicat eo modo, quo dicuntur Orationes ad Horas"; Proc. p. 20 "eo tono"; Proc. pp. 20-21 pointing: flexa at "voluísti" (Missal "."); the final "...sæculórum ‡." takes the flexa (p. 408) |
| Palm: DV + Sequéntia | already op13-palm-evangelium-dv | VI | Proc. p. 23 |
| quad6-2 Gospel *Cum appropinquásset*, body only (p. 139) | before the T ^IN illo témpore : Cum appropinquásset | VI | Missal "legat"; Proc. pp. 22-23 "cantet Evangelium" |
| quad6-3 Procession prayer *Orémus. Omnípotens... qui humáno* (Proc. p. 33) | Quad6_proc.src, before "T: Orémus." | III, book pointing | "absque Dóminus vobíscum, præmisso Orémus, dicat Orationem eo modo quo dicitur ad Horas" |
| quad6-4 Mass Collect with DV + Orémus (p. 139) | before the T ^OMNIPOTENS... qui humáno (Quad6.src) | II | "Hæc Oratio sola dicatur"; Rubr. gen. XI.1, p. 52 |
| quad6-5 Epistle Phil. 2 with its title (pp. 139-140) | before the T {L}éctio Epístolæ | V | Proc. p. 414 |
| quad6-6 Postcommunion (p. 146) | before the T ^PER hujus | II | no DV (the Order of Mass sings it at X: post) |
| Passion, Secret (said secreto, pp. 38-39), and the Gospel at the end of a private Mass | not sung / Lead C | | |
| quad6m-1 DV + Orémus (also used Tue, and before Wed's 2nd Collect) | before G op-m39-flectamus | II | Proc. pp. 404-405 |
| quad6m-2 Collect *Da quǽsumus* (p. 146) | before the T | II | |
| quad6m-3/4 2nd (Orémus, no conclusion) and 3rd (with conclusion) Collects | lent_or.src (shared by Mon-Wed) | II | Rubr. gen. XI.1 |
| quad6m-5 Is. 50 with its title (p. 147); quad6t-2 Jer. 11; quad6w-5 Is. 53 | before the title T | V | in the place of the Epistle (hw_tones §4) |
| quad6m-6 Gospel Jn 12 with DV + Sequéntia (p. 147) | before the T {✠ S}equéntia | VI | Proc. p. 424 |
| quad6m-7, quad6t-3, quad6w-6 Postcommunions | before the T | II | |
| quad6m-8/9 2nd and 3rd Postcommunions | lent_pc.src (shared by Mon-Wed) | II | |
| Orémus before Humiliáte, Mon-Wed | existing op13-quad6f-oremus, before G op-m39-humiliate | II | Proc. p. 405 |
| quad6m-11, quad6t-5, quad6w-8 Oratio super populum | before the T | II | Proc. p. 405 "Ante ultimam Postcommunionem ... Humiliáte" |
| quad6t-1 Collect; quad6w-1 Collect I *Præsta*; quad6w-4 Collect II *Deus qui pro nobis* | before the T | II | |
| Wed: Orémus before the 1st Flectámus | existing op13-quad6f-oremus | II | Missal p. 154 "non dicatur Dóminus vobíscum, sed Orémus" |
| quad6w-2 Lesson I, Is. 62-63, with its title (p. 154) | before the title T | IV | Proc. p. 408 "Prophetias in Missa"; ends by n. 11, p. 413 |

## Open questions (rule 4: ask main)
1. **Palm Gospel pointing.** Proc. pp. 23-24 prints the Gospel pointed for singing, and its punctuation differs from the Missal's (e.g. "dicens eis. Ite...", "Sólvite : et addúcite"). The gabc now uses the Missal's punctuation. Should it use the Proc's?
2. **Blessing prayer, "constráta est."** This is a mid-prayer full stop, and Proc. p. 21 also prints a plain "." there, with no sign. The engine now gives it an elevatio. Should it?
3. **Postcommunions.** They have no DV/Orémus, because the Order of Mass `post` sings them. With the Order of Mass off, the page therefore shows no DV. Is that acceptable?
4. **Is. 50, Jer. 11 and Is. 53 in the Epistle tone.** I followed hw_tones §4. Please confirm against the Dominican practice.
