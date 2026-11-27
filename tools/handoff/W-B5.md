# W-B5: Holy Saturday 1939, priest's and ministers' tones (stopped 27 Nov 2026)

State: research and inventory done, and main answered the questions. NOTHING wired. No gabc/op-hw-quad6s-* written,
no G:/INC lines in tools/hw39/Quad6s.src, no tools/hw39/Quad6s_font.src, no gen_quad6s.js. Engine: js/mtones.js
OPMassTones.*Proc (declared STABLE by Lead B). Model the generator on tools/hw39/gen_quad6f.js, which has the same
structure: ITEMS list, Missal words + Triduum pointing, --gabc --write --compile, and it re-reads the file before
inserting.
Scratch: tools/handoff/scratch/w-b5/ holds the OCR of the Triduum 1927 pdf 137-141 (= pp. 268-277, the lessons and
prayers; o[LR]<pdf>.txt; the flex sign OCRs as "2", "z" or "&", so check against the scan) and the St Dominic Missal
1959 English of the font blessing (pp. 392-398, the OCR is interleaved with Latin).

## Books / pages
- Missal O.P. 1939 /home/claude/dl/missal/M39.pdf. Holy Saturday pp. 179-191 = pdf ~120-127 (2 printed pages per pdf page).
  Font blessing App. pp. 147*-150* = pdf 441-443. Preface tones App. pdf 446-463: solemn Paschal p. 10 = pdf 451.
- Triduum O.P. 1927 /tmp/dl/tri.pdf (2 printed pages per pdf page): fire blessing p. 257 (pdf 131); lessons and prayers
  pp. 268-276 (pdf 137-141, pointed with the flex sign and colons); Collect + Epistle p. 282; Gospel p. 284;
  Postcommunion p. 288. The Triduum has NO font blessing.
- Processionarium 1913 /home/claude/dl/proc/p.pdf (pdf = printed + 16): tone II pp. 404-406, tone III pp. 407-408,
  lessons pp. 408-413.

## Inventory (in order; already notated and left alone: Exsultet op-exsultet-1..5, Litany op-lit-*, 7309/7300, tracts, al 0, Ps 116, Magnificat, 7310)
The 1939 rite has no separate blessing of the incense grains or of the candle. The grains are fixed and the candle
lit inside the Exsultet (rubrics p. 180).
1. Fire blessing "Domine sancte": orationProc tone 'hours' (III, Proc. p. 407: "aliae Orationes quae non sunt de corpore
   Officii et Missae"), noOremus. Rubric p. 179 kept above: "absque Dominus vobiscum, et absque Oremus, legendo sine
   nota". Conclusion as Triduum p. 257 prints it: "Per eumdem Christum Dominum nostrum. R. Amen." G before "T: ^DOMINE sancte".
2-5. Lessons 1-4 (Gen 1-2; Exod 14-15; Is 4; Is 54-55): lessonProc, no title (Triduum p. 268: "absque titulo, et
   in tono Lectionis"; Missal p. 180: "legantur sine titulo"). All end by n. 11 (lesson 4 ends "Dicit Dominus
   omnipotens.", the very example on p. 413). Pointing: the Missal words with the Triduum flex signs and colons, as
   Good Friday did. The Triduum's punctuation differs a lot from the Missal's (e.g. "Dixit vero Deus. Congregentur"),
   so check each mark on the scan.
6-10. "Oremus" + the 5 prayers (Deus qui mirabiliter; Deus cujus antiqua; Deus qui nos ad celebrandum; Deus qui
   Ecclesiam; Concede): orationProc tone 'mass' (II), oremus:true, G before each "T: Oremus." line. Triduum p. 270:
   "sine Dominus vobiscum, et sine Flectamus genua, sed praemittatur tantum Oremus".
11. Mass: DV + Oremus + Collect "Deus qui hanc sacratissimam" (rubric p. 188 "dicat Dominus vobiscum"): tone II,
   dv:true, G before "T: Oremus." (line ~124). The ending is "Per eumdem." Check the Triduum p. 282 for the full form
   (with or without ejusdem).
12. Epistle Col 3: epistleProc with title "Lectio Epistolae beati Pauli Apostoli ad Colossenses." (T line ~130).
13. Gospel Mt 28: gospelProc({book:'Matthaeum', dv:true}). Rubric p. 188: "petatur benedictio, et alia fiant ut moris est".
14. Offertory "Dominus vobiscum. Oremus." (rubric p. 188): G: 7339 + G: op13-quad6f-oremus after that R line.
15. Vespers: DV + Oremus + Postcommunion "Spiritum nobis" (rubric p. 190), tone II, dv:true, G before "L: Postcommunio".
16. DV before the Ite (rubric p. 191): G: 7339 before G: 7310.
Not sung (said): the Deacon's blessing "In nomine Patris", the Secret, the Canon, Placeat, the blessing, the last Gospel.

## Font blessing (new section, App. pp. 147*-150*; put it in tools/hw39/Quad6s_font.src with one "INC: Quad6s_font" line after the 5th prayer, before "== Litaniae")
Rubric p. 147*: "Si Ecclesia nostra habuerit Fontem baptismalem, dicta post quartam Lectionem Oratione ... dum
incipitur Tractus Sicut cervus, pag. 185, fiat Processio ad Fontem". Then the Concede is said at the font. After the
font: "duo Fratres ... cantent Litanias, pag. 185", then the Mass ("Cetera fiant ut pag. 188").
Latin: read from the scan crops (pdf 441-443 at 200 dpi, legible); the m39lin text has no accents. English: St Dominic
Missal 1959 pp. 392-397, verbatim. The Concede's English is the one already used in Quad6s.src.
Blocks: Concede (rubric "absque Dominus vobiscum", Oremus) | "Deinde ... juxta fontem": DV, Oremus, Omnipotens ... respice
| "Postea procedit ...": DV, Oremus, Omnipotens ... adesto ... Deus : | "Prosequitur junctis manibus": Per omnia ...
Vere dignum ... de Spiritu Sancto | Qui hanc aquam ... corrumpat | Sit haec sancta ... consequantur | Unde benedico ...
ferebatur | Qui te de Paradisi ... Spiritus Sancti | "Mutat vocem et legendo dicit": Haec nobis ... aspira | "Halat
ter": Tu has simplices ... efficaces | Descendat ... Sancti (rubric on the 3 repeats) | Totamque ... effectu [Hic tollitur
Cereus] Hic omnium ... renascatur | "Sequentia dicit legendo": Per Dominum ... per ignem. R. Amen | the oil and chrism
formulas | closing rubrics. Skip the Pentecost Concede (Holy Saturday only).

## Answers from main (27 Nov)
- Q1: tone III for the font prayers "Omnipotens ... respice" and "Omnipotens ... adesto"; the Concede at the font stays tone II.
- Q2: SOLEMN Preface tone (App. p. 10: "cum cantu solemni dicatur in Vigilia et in die Paschae").
- Q3: "legendo" passages (Haec nobis ...; Per Dominum ... per ignem) are set in the same Preface tone, with the rubric kept above.
- Q4: Descendat gets one setting, with the rubric quoted; no invented transpositions.
- Q5: the oil formulas Sanctificetur / Infusio / Commistio ("intelligibili voce") stay text only.
- Q6: the Concede at the font prints "sitiamus : Dominum nostrum ... Filium..." as the book has it (with a short note
  that the book omits "Per"); it is sung "Per Dominum".

## Left to do (all of it)
1. Write tools/hw39/gen_quad6s.js (copy gen_quad6f.js; prefix op-hw-quad6s-NN), items 1-15 above. Transcribe the
   Triduum pointing for the 4 lessons + 5 prayers (OCR in scratch, proofread on the scan).
2. The font section .src (Latin + English) + INC line; build.py must still run.
3. Font chant: "Omnipotens ... adesto" through "Deus :" in tone III (cut the engine's conclusion after "Deus :"); then a
   Solemn Preface-tone setter for Per omnia ... renascatur and the "Per Dominum ... per ignem". The engine does not do
   prefaces. Derive the formulas from the Missal appendix SCAN, not from the op-m39-praef-*-solemn files (they are OMR):
   the solemn mediant is like "lau(h)dant(gf) An(fg)ge(g)li(g)" and the final like "tre(g)munt(fe) Po(ef)te(g)sta(fg)tes(f)".
   Check the cadence placement on the scan for several endings: in the ferial files the e-f-g figure falls 2 or 3 syllables
   before the final accent, depending on the words. The dialogue Per omnia ... Dignum et justum est is copied note by note
   from the solemn tone (App., e.g. p. 10, pdf 451).
4. gregorio-compile each file (cd /tmp && gregorio -o x.gtex /abs/file), insert the G: lines (re-read the file first;
   W-B6 edits Quad6s.src), python3 tools/hw39/build.py, headless Chrome holyweek.html#Quad6s&d=2027-03-27 with
   localStorage hwRite=1939: no console errors, nothing undrawn. Check against the scans before handing up.
