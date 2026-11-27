# Mass chat — where to resume (27 Nov 2026, after v184)

Standing rules: pre-1955 Dominican rite only; never infer chant; terse; status after each substep; `git pull --rebase`,
bump sw.js, headless Chrome test, commit as UltraPheonix, `bash tools/push.sh`; do not touch the Office files.
**New (Joseph, 27 Nov): after every step, one quality run and one clarity run before moving on.**

## Done this session
- rubrics.html: every rubric of the Missale O.P. 1939 (De defectibus, Praeparatio, Modus et Ritus, genuflexions, Sacrament exposed /
  tabernacle, before a prelate, Masses for the dead, voice, servers, De officio ministrorum, De sacra Communione, general rubrics),
  Latin + English (AI, labelled), prayers bold. Built by tools/rubrics/build_rubrics.py (modules ritus_*.py); writes data/rubtext.js.
- Mass page: Basic / Full rubrics switch. Basic = only the rubrics of the Ordo Missae (M39 pp. 191-193). Full = the Ritus step by step,
  forms Low/Sung/Solemn/Conventual, conditional lines (prelate: Pope / Bishop / Master of the Order; Sacrament: tabernacle / exposed;
  servers; rank of the day, incense days, Requiem, Flectamus, etc.). Source: tools/rubrics/ordo_directions.py -> data/ordo.js
  (texts in tools/rubrics/ordo_texts.json). Day rank = KAL39 + heuristics (approximate until the day-classification engine exists).
- prayers.html: vesting prayers, prayers before and after Mass. Published PD English where found (tools/prayers/prayers_published.py:
  1905 reprint of Oakeley 1848 for vesting; Manual of Prayers, Baltimore 1889 for St Thomas, St Ambrose, Ad mensam, St Bonaventure;
  Hopkins for Adoro te; [brackets] = ours). Remaining AI-labelled: Augustine/Ambrose readings, confession prayers, O sancte N.,
  O serenissima, Pater caelestis, Anima Christi (Dominican form), In nomine.

- v169 chant English (#46): tools/check/trans_source.py relabels English that is really Douay-Rheims ('douay' verbatim, 'dra' adapted
  to the chant); 410 remain AI ('own'). Each chant's English shows its source on the Mass page (Douay-Rheims / adapted / AI).
  Decision taken without Joseph: the 1959 St Dominic Missal English was NOT restored for the AI chants (easy to do if he asks:
  tools/sources/dm_trans.json).
- v170 2nd and 3rd prayers (#40): data/addiv.js (tools/addiv: parse.py, fix.py + la_fix.json proofed from page images of M39.pdf
  pp. 100*-113*, tern.py, en.py, build.py). Selector under the Collect (state.o2/o3, hash o2=,o3=): of the season, Orationes ad diversa
  1-38, or 'm:KEY' commemoration from data/orations.js. Hint + "Use" for the season (Rubr. gen. X). Hidden at Requiem / Holy Week.
- v171 error check (#41): see tools/g50/REVIEW.md (Statuit Communio, Commons' Tracts, St Margaret of Hungary, Octave of Peter & Paul).

- v173 processions (#42, started): processions.html built by tools/proc/build_proc.py from tools/proc/proc_data.py (SECTIONS: items
  'rub' / 'txt' / 'scan' [printed pages] / 'lit' rows). Source: Processionarium O.P. 1913 (Cormier), CMAA scan
  media.churchmusicassociation.org/dominican/processionarium-1913-Cormier.pdf -> /home/claude/dl/proc/p.pdf; pdf page = printed page + 15.
  Page images: art/proc/<page>.png (1-bit PNG, ~25 KB; script in the v173 session: render 2.1x gray, trim, threshold 150).
  OCR: tesseract -l ita --psm 4 on 3x renders, then proof against the image. Done: Ascension pp. 46-51, Purification pp. 66-72, Salve Regina procession pp. 89-91 (+ O lumen p. 76),
  Litany of Loreto + Inviolata pp. 91-95, Rogations pp. 124-126, Litany of the Saints pp. 126-130, extraordinary processions p. 131. Index of the book: pdf pages 459-461 (printed index).

## Joseph, 27 Nov 07:47-07:58 (most recent; overrides the order below)
- Work was too sloppy: do a real quality + clarity run (screenshots) after every step; never push before the full sweep finishes.
- Processions: EVERY chant must be typeset in GABC (no scans). Page is out of the menu (v180) until done. Transcribe by eye
  from the 1913 scan (crops at 3x with line labels; the OMR in tools/pdfomr reads only the first staff of a page here), then
  render the GABC beside the scan and compare note by note.
- 2nd and 3rd prayers: catch EVERY one the Missal sets. v182 = the seasonal rule (Rubr. gen. X.1) in js/app.js prescribed();
  the 2nd has no ending, only the last (3rd) does (XI.1); sung in the tone (v181). STILL TO DO, in tools/addiv (new fixed.py):
  a complete table key -> prescribed prayers from tools/orat39/m39lin.txt, each checked against the page image (M39.pdf):
  * temporal 'Secunda Oratio' (28) and 'Secunda et tertia Oratio, ut in ... / pag. 40 / 47 / 63 / 287' (48): map to keys by
    position (the Masses of the Time in order), NOT by collect prefix (Advent collects all begin 'Excita');
  * 'Memoria' + 'Oratio' blocks printed inside feasts (lines ~44977, 52758, 53431, 58688, 59769, 65260, 67035: split over two lines),
    with their Secreta and Postcommunio: new texts -> ADDIV sets with English;
  * 'Et fit Memoria ...' (Epiphany octave, Sunday in the octave of Ascension, Corpus Christi, SS. Cordis, Christ the King with the
    Sunday, S. Irenaeus with the octave of St John and the vigil, S. Silvester with the Nativity, Christmas 2nd Mass of St Anastasia,
    Ember Wednesday of Advent 'Festina', the octave day of St Lawrence, Rogations in all Masses, 7-8 Mar.), and rule 8898
    ('semper fit Memoria de Feria majori Adventus, Quadragesimae, Quatuor Temporum et Rogationum').
  * DONE 1a (v184): all 76 printed/referred temporal 2nd/3rd prayers checked (by collect text and position): every one fits the
    seasonal rule in prescribed(); the Epiphany's 'Infra Octavam additur Secunda Oratio Deus qui salutis' = rule X.1 b.
    Holy Week Mon-Wed print 'Secunda et tertia Oratio, pag. 63' but render via the Holy Week text (data/holyweek_text.js):
    the two prayers must be inserted there (not yet).
  * Joseph: the day-ranking engine is to be built twice, one for the Missal, one for the Breviary (the Office chat owns the Office files).
  * then prescribed() uses the table first, the seasonal rule second; KAL39 Memoriae without prayers in the data need their
    orations (from M39). Footnotes 39623-39631 (Saturday BVM, votive BVM, Joseph/Peter-Paul/Dominic omitted from A cunctis).

## Next
1. Processions (#42) continued, in this order: Palm Sunday (20, compare with Holy Week page), Easter (34, 42), Corpus Christi (51, 55),
   Assumption (77), St Dominic (73, 97), processions of the Order's saints (97-110), Te Deum (120), Asperges (2), then the rest.
   Chant: GregoBase source 20 has only 11 chants of this book; transcribe to GABC only from the page, never by analogy.
2. Open from the review: 168 'inferred' chants in data/masses.js to check against the Graduale; 43 orations without Latin conclusion.
3. Booklets (js/booklet.js) do not yet print the 2nd/3rd prayers.

Sources: M39 PDF = archive.org/download/m-39_20261122/M39.pdf (download to /home/claude/dl/missal/M39.pdf for page images).
Graduale O.P. 1950 scan is not reachable (archive.org copy is loan-only); OCR in tools/g50/ocr.tgz, GregoBase pages in tools/gregobase/gb.sqlite.

Test helpers (recreate if /tmp was cleared): local server `python3 -m http.server 8768`; sweep of Masses x forms x rubrics
is tools/check/mass_sweep.py (load index.html?n=<i>#<key>&ordo=<f>&rub=<full>&sac=..&prel=.., check pageerrors, duplicate rubric lines,
empty sections, Canon present).
