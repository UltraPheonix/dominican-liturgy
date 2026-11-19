# Holy Week transcription — where it stands (2026-11-18 17:10)

Goal (user): two complete options, Traditional (Missale O.P. 1939) and Reformed (St Dominic Missal 1959),
each with ALL text, rubrics and chants of every day, verbatim from its own book, styled like the site.
Latin j -> i (site style). English: 1959 missal's where the text is the same, otherwise ours
(Passions: Douay-Rheims verses from site/bible, paired by mkpassion.py).

## Files (tools/hw39 in the repo; work copy /home/claude/build/hw39)
- <Day>.src = 1939, <Day>_59.src = 1959.  Days: Quad6 Quad6m Quad6t Quad6w Quad6h Quad6f Quad6s
- Tags: == section | H heading | I italic | L label ("Officium | Ps. 34") | R rubric | T text | C: part idx (chant)
  F/F/ tap-to-open fold | P: name (paired <name>_parts.txt / <name>_en.txt) | INC: fragment.src
  X: start, ky, gl, cr, gradualEnd, gospel, afterGospel, offer, offertory, offertoryEnd, pref, sa, canon, post,
     postEnd, dismiss, end  (Ordinary chants + Order of Mass go there; js/app.js massSequence)
  Markup: {red}  *black in rubric*  ^Initial ; " = " line = English of the line above.
- build.py -> site/data/holyweek_text.js (window.HW_TEXT[rite][day]).
- Pipeline for a 1939 day: draft39.py bp0 c0 bp1 c1 DO-ref > X.draft ; resolve.py X.draft | fixsp.py | clean.py
  then hand-write X.src from it.  Column OCR: /home/claude/build/m39hw/p<bp>.json (ocr39.py <bp> to add pages).
  Page images for proofing: m39hw ocr39.spread/render (see /tmp/cols code in history).
- 1959: dmsplit.py LINE0 LINE1 splits /home/claude/dl/txt/dm.txt into English/Latin labelled sections.
  dm.txt lines: Mon 13428, Tue 13551, Wed 14015, Thu 14587, Fri 15367, Sat 16483.

## UI (2026-11-18 evening)
- holyweek.html = own tab (body data-page="hw"; app.js HWP branch: day list #hwDays, rite switch #hwRite, rite kept in localStorage hwRite).
- Mass page shows a card linking to holyweek.html on Holy Week days. Sidebar: date + one <details class="opts">. EN switch .en-toggle (ui.js).
- "Report an error" button on every page (ui.js, mail jcampion@friars.providence.edu).

## Word-by-word proof of 1939 (tools: /home/claude/build/proof/proof.py DAY BP0 BP1; crop.py BP COL Y to view)
- Mon–Sat: every word matches the Missal OCR except OCR noise. Fixed: Good Friday Agios rubric split into the book's 3 paragraphs
  and the added "Sanctus Deus" line removed; "in unitáte Spíritus" (no ejúsdem). Kept on purpose: full texts where the book
  gives only an incipit (Panem de cælo, Tantum ergo stanza, 2nd/3rd orations of p.63); "Per Dóminum" where the book misprints
  "sitiámus : Dóminum" (Sat). Punctuation not yet checked automatically.

## Done (1939)
- Quad6 Palm Sunday (pp.137-146) — proofread against the scan.  (TODO: add X: markers to its Mass section)
- Quad6m Monday, Quad6t Tuesday (Passion of Mark), Quad6w Wednesday (Passion of Luke), Quad6h Thursday (absolution p.54, Mass, procession, Vespers) — OCR+reference repair, not yet proofread line by line.
- Lenten 2nd/3rd orations: lent_or/lent_se/lent_pc.src (M39 pp. 63, 65).

## In progress
- Quad6w Wednesday (154-160): draft Quad6w.r2; lucas_parts/en ready; lesson Is 53 punctuation checked
  against the scan (see image p.155): "nostræ super eum", "Dóminus in eo", "ipse vóluit", "apériet os suum. De",
  "sublátus est : Generatiónem", "sua : eo quod", "ore ejus. Et Dóminus vóluit contérere eum", "Si posúerit pro
  peccáto ánimam suam, vidébit semen longǽvum, et volúntas Dómini in manu ejus dirigétur." Rubric after Introit:
  R "Post Kyrie eléison, non dicatur" + "Dóminus vobíscum, sed Orémus. Flectámus génua. Leváte." DM English in dm_wed.json.

## To do
- 1939: all seven days transcribed (Holy Saturday via mksat.py). Next: Palm Sunday procession from Processionarium O.P. 1913 (/home/claude/dl/proc, pdf pp. 35-48 = book pp. 20-33), Triduum chants from Ecclesiasticum Officium Triduo ante Pascha 1927 (/home/claude/dl/tri), then proofreading, then 1959.
- 1959: all seven days from the St Dominic Missal (*_59.src); until then the 1959 option shows the old data/holyweek.js.
- Palm Sunday X: markers; check chants exist for every C: (parts in data/masses.js).

## 2026-11-18 late: Exsultet done (Triduum O.P. 1927 pp. 258-268), site/gabc/op-exsultet-1..5.gabc
- Split at the Missal's rubrics (grains of incense / lighting the candle / acolytes' candles / lamps). Chant text follows the
  Triduum book (e.g. "íntonet", "divísos"), the Missal text above it keeps the Missal's wording.
- Page files + NOTES.md in tools/chant/exs; checked against the note reader (vcheck.py): no pitch disagreements except
  known reader noise (porrectus gfg read as fg/h).  N. placeholders = 3 notes each (book).
- Still to do (order agreed with user): Litany + Mandatum, Triduum Office, Palm Sunday procession chants (last), then 1959.

## 2026-11-19 morning: Mandatum done (Triduum O.P. 1927 pp. 112-123) -> Quad6h_mand.src (INC at end of Quad6h)
- 13 antiphons transcribed: site/gabc/op-mand-01..13 (tools/chant/mand, NOTES.md). Clefs: II = f3, VI = c2, VII (Diligamus, Maneant) = c2.
- Sermo Domini = John 13:1-17:26 from site bible (la + Douay), folded.
- NEXT (user agreed): UI overhaul (settings/Options panel, English placement, general tidiness) -> ask user questions first.
- Still open for Holy Week 1939: Ablutio altarium on Thursday (Triduum pp. ~95-111, antiphons at each altar), Triduum Office,
  Palm Sunday procession chants, check Holy Saturday tracts vs Triduum book; then 1959.

## 2026-11-19: UI overhaul (user choices: split options by purpose, English under Latin, top bar, content first)
- All pages: <header class="top"> (brand, tabs, EN, gear) + <aside class="sheet" id="sheet"> (Options: Day/Chants/Show/Advanced),
  day bar + tools (Share/PDF) at head of .inner. Old sidebar (.frame/.side) gone. tools/restructure.py did the HTML move.
- English: always below the Latin, smaller italic grey (no more two columns).
- Holy Week: rite switch + day tabs at the head of the page.

## 2026-11-19 07:30: Booklets (user: "steps 1 2 3 asap" = Choir Book, Congregation Booklet, Priest Missal)
- Priest chants read from the All Saints priest PDF (tools/pdfomr/omr.py, head splitter for joined neumes):
  site/gabc/op-pater-solemn, op-pax-domini, op-praef-dominic-solemn (f3). tools/chant/resyl.py = liturgical re-syllabifier.
- NEXT: booklet.html + js/booklet.js (browser print, A4), Choir Book -> Congregation -> Priest.

## 2026-11-19 08:30: Booklets working (booklet.html?b=choir|priest|cong#<mass hash>)
- js/booklet.js lays out A4 pages itself (units -> columns -> pages; page numbers known for contents/footers).
  Choir Book (1 col, chants only + Modus respondendi), Priest's Missal (2 cols, Canon in border pages), Congregation (Latin|English).
- booklet.html is lang="en": EB Garamond's Latin locl turns u into v!  J() gives the Missal's j-spelling.
- Ordinarium X: Gloria/Sanctus/Agnus = Vatican VIII melodies (gabc/opX-*), added to D.kyriale in app.js.
- A Credo chosen under Options is now sung even when the rubrics don't require it.
- Orations added for S1112. ~180 Masses still lack orations (fill from dm.txt) -> next.
- Test: python3 tools/booklet/book.py choir "S1112&d=2026-11-12&ord=X&credo=I" out.pdf (server on :8768 in site/).

## 2026-11-19 07:50: Orations (IN PROGRESS, nothing merged into site/data/orations.js yet except S1112)
183 Masses lacked orations. Pipeline in tools/orat39:
1. lin.py   : Missale OP 1939.pdf -> m39lin.txt (text layer, blocks by column, drop caps joined). Clean!
2. seg.py   : -> m39masses.json (455 Masses: month(0-based), day, title, pr{or,se,pc}, comm = Common page if "ut in Comm.")
3. match.py : site Mass -> 1939 Mass (date +-2 days, name, saint's name in the Collect) -> matched.json (124 of 183)
4. accent.py: accent dictionary from Divinum Officium + site texts (accdict.json, rebuilt automatically)
5. build_or.py: Latin accented + full conclusion; English from St Dominic Missal (dm_prayers.json) when same prayer
   -> new_or.json + report.json (unknown Latin words, English spelling fixes). 106 Masses complete.
TODO: (a) finish OCR fixes (build_or.py ocr_fix just added, untested; run python3 build_or.py)
      (b) manual_acc.json {flat word: accented} for ~100 rare words/names; (c) ~111 prayers need English (translate);
      (d) Masses "ut in Comm. p. N*": take the Common's prayers and put the saint's name in;
      (e) 59 not found: post-1939 Blesseds (need the current Dominican Proper), votives/commons, moved dates;
      (f) proof every prayer against the Missal page, then merge new_or.json into site/data/orations.js.
See tools/orat39/MISSING.md for the per-Mass list.
