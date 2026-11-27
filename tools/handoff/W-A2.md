# W-A2: extraordinary processions (Proc. O.P. 1913 pp. 131-134, pdf 147-150), stopped 27 Nov

## Done (compiled with gregorio; Latin read twice from the scan, at 300 and 500 dpi; nothing committed; build_proc.py NOT run)
- `tools/proc/gen_ex.js` (new). It copies the gen_tones.js logic: versicles in the tone of p. 395 3°, prayers in the tone of pp. 407-408 III, the dactyl rule of p. 405 2°. It holds the texts with the book's flexa signs (†) and colons. It checks that every text it sets stands word for word in a txt item of 'extraordinariae'. Run: `EX_MONO=recto node tools/proc/gen_ex.js` (or `EX_MONO=fall`; add `EX_MONO_FINAL=1` once the reading is decided, which removes "DRAFT" from the 4 headers). `--print` prints the site texts.
- `tools/proc/gabc/ex_*.gabc`: 10 files, all compiling.
  - Wired in: ex_versus (the 3 V/R pairs on p. 131), ex_orationes (Orémus, Concéde nos, Parce, p. 132), ex_pace, ex_pluvia, ex_serenitate, ex_papa.
  - DRAFT, not wired in: ex_ecclesia, ex_pestilentia, ex_turcas, ex_rege. Their monosyllable lines are currently generated "recto" as a placeholder.
- `tools/proc/proc_data.py`: the block `# extraordinariae (W-A2)` at the END.
  - pages = [131-134].
  - ex_versus goes before the ℣. Et ne nos text.
  - After the rubric "Póstea subjúngat álium": the rubric Deínde, ex_orationes, the Concede + Parce text, the rubric Demum, then for each of the 8 occasions its rub, gabc (except the 4 DRAFT ones) and txt (℣ ℟ Orátio … ℟. Amen) with English.
  - The Latin keeps the book's flexa sign as "†" inside a text, and its colons. A versicle-final flexa sign is written as ".". The English is the site's AI translation (the page-level note covers it).
- No typed slips are pasted on pp. 131-134.
- The 3 "Per Christum..." conclusions (Turcas, Papa, Rege) are expanded in full, as the rubric on p. 132 says: "eam terminando Per Christum Dóminum nostrum".

## Open question for Joseph/coordinator: versicles ending on a monosyllable
On these 4 lines the book prints ":" instead of the flexa sign. The tone of p. 395 3° has no example of this ending.
- p. 132: ℟. Et propter glóriam nóminis tui, Dómine, líbera nos :
- p. 133: ℣. Exsúrge, Dómine, ádjuva nos :
- p. 133: ℟. Et de Sion tuére nos :
- p. 134: ℟. Deus meus, sperántem in te :

The two readings (both are in gen_ex.js):
- **A, recto (`EX_MONO=recto`):** the whole line is sung on the tenor h, with no fall. This fits the book's choice of ":" over the flexa sign, and p. 402 (Capitula): "Non flectuntur verba monosyllaba aut hebraica".
- **B, fall (`EX_MONO=fall`):** only the monosyllable falls to f (…lí-be-ra(h) nos(f)). This is the simplest reading of the 3° example, where the last syllable is on f.

Not usable as a precedent: the p. 396 "Item alia differentia" ends mandá(h)vit(g) de(f) te(h), and the p. 395 1° example "Suscéptor meus es tu" is melismatic. Both are different tones.

The search for a notated precedent elsewhere in the book is unfinished. OCR reached pdf 17-93 plus part of the rest, and the OCR output is in /tmp/wa2. Pp. 135-159 (OCR) give these responses only as text, always with ":".

## Other notes
- The dactyl rule follows gen_tones.js. For "pervéniat sempitérnam:" it gives sem(g) pi(f), with the "at" of pervéniat left on h. A literal reading of p. 405 2° ("vel tres, si tertia ante accentum sit dactylica") could also lower "at". The site is consistent with gen_tones as it stands.
- ℟ of Papa: the book prints a flexa sign inside the ℟ too ("in terra †"). It is set as a fall plus a half bar.
- Rege: the alternatives "vel Dux, vel Princeps" and "vel Ducátus, vel Principátus" are shown in italics with no notes, as in op-exsultet-5.gabc.
- The existing Rogation text "Parce … castigátus, in tua" uses a comma where this section has † (item 9, punctuation, is not mine).

## Resume
1. Get the decision (A or B). Run `EX_MONO=<x> EX_MONO_FINAL=1 node tools/proc/gen_ex.js`, then gregorio-check.
2. In proc_data.py, empty `_EXDRAFT` so the 4 gabc are wired in.
3. Lead: run `python3 tools/proc/build_proc.py`, then headless Chrome on processions.html#extraordinariae. This has not been checked in Chrome yet.
