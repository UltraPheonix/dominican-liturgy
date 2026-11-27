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
  * 1b inventory: 'Memoria' + 'Oratio' blocks in M39 (m39lin.txt lines) = commemoration-only saints with their own prayers:
    44977 Vedast & Amand (6 Feb), 52758 Medard (8 Jun), 53431 Quiricus & Julitta (16 Jun), 58688 Tiburtius (11 Aug),
    59769 Timothy & Symphorian (22 Aug), 65260 Crispin & Crispinian (25 Oct), 67035 Four Crowned (8 Nov). Make ADDIV sets
    (or, se, pc; proof from M39.pdf page images; English) and link them to the KAL39 Memoria entries of those dates.
    KAL39 has 75 Memoria entries: find where M39 gives the prayers of the other 68 (search the feast of the same day,
    the Commons 'ut in Communi', or the supplements); list any not in M39.
  * then prescribed() uses the table first, the seasonal rule second; KAL39 Memoriae without prayers in the data need their
    orations (from M39). Footnotes 39623-39631 (Saturday BVM, votive BVM, Joseph/Peter-Paul/Dominic omitted from A cunctis).

## Day-by-day audit of the Mass (Joseph, 27 Nov 08:13): tools/check/day_audit.py START END > /tmp/year.json (about 10 min a year),
then tools/check/day_report.py /tmp/year.json. First run 2026-11-29..2027-11-27: no page errors, all propers/orations/readings present
except Paschaltide ferias (one Alleluia: correct, XIII.1) and the Vigil of Pentecost (no Introit: correct). The real problem is the
choice of the day's Mass: massesOf() in js/app.js uses the 1960 class scheme (feastClass/temporalClass I-IV) and treats every
Dominican Blessed as ad libitum, so e.g. BB. Alphonsus Navarrete (1 Jun), Innocent V (22 Jun), Benedict XI (7 Jul), Mannes (30 Jul)
lose to ferias, the Saturday Mass of Our Lady beats Ss. Philip and James (1 May 2027) and falls within the Epiphany octave (9 Jan),
St Thomas Becket / St Silvester lose to the Christmas octave. M39 Rubr. gen. (m39lin.txt 6290-6460): 'Missa quotidie celebrari debet
secundum ordinem Officii, de quo fit illo die' -> the Mass follows the Office of the day (Breviary precedence); tit. III Sunday,
tit. IV ferias and vigils: in Lent ferias, Ember days, common vigils with a feast, TWO conventual Masses (in choir: the feast for
Totum Duplex I/II cl. and the privileged octaves of Epiphany and Corpus Christi, otherwise the feria); private Masses ad libitum.
To build: the Missal ranking engine (Joseph: separate engines for Missal and Breviary).

## Missal ranking engine (BUILT 2026-11-27): js/mrank.js, window.OPMissalRank(KAL39, masses).day(date)
Joseph: separate engines for Missal and Breviary (this one is the Missal's; tools/ENGINE.md shared plan superseded for the Mass).
Decisions (Joseph 27 Nov): 1939 calendar + supplements to 1954, Polish provincial feasts ignored; on Lent ferias / Ember days /
vigils / Rogations with a feast the page shows the choir conventual Mass first (feria; the feast for I and II class).
Rules: precedence values in mrank.js read from the Ordo O.P. 1944 (cited per rule); M39 Rubr. gen. I-VIII; Christmas Sunday (p. 28);
Holy Family (p. 39); vigils on Sunday anticipated (27 Jun., 14 Aug.); leap year; transfers (I/II class, displacing lesser II class);
Requiem conventual on the week's first free feria (VI.2); the four Anniversaries; BVM Saturday; commemorations with VIII.2 limits.
app.js: massesOf/temporaleKey/memoriasOf now from the engine; header and pills print the 1939 rank; "Also today" line under the
date (other Masses, and Masses the Missal sets that the site lacks). rubricsOf (Gloria/Credo) still uses feastClass/temporalClass.
Test: node tools/ordo44/engine_dump.js 1944 > /tmp/e44.json; tools/ordo44/compare_engine.py (office: 33/324 differ, all explained:
Polish feasts, post-1944 supplements, parse) and compare_mass.py (conventual Mass named in the Ordo: all agree except resumed Sundays).
Ordo re-read from the PDF text layer: tools/ordo44/parse2.py -> ordo1944b.json (324 days; 42 still to read from page images).
OPEN:
 - DONE (v189): Joseph supplied the Breviarium S.O.P. 1924 (Theissling; Drive '346_Breviarium...zip', djvu, text via djvutxt ->
   /tmp/b24.txt; /home/claude/dl/brev346). Its Rubricae generales (§ II, VII, XXI, XXVIII-XXX) now ground mrank.js: classes of
   Sundays/ferias/vigils, occurrence within octaves, transfers (to a day free of I/II class, Sunday, privileged vigil), feasts of
   the Lord on minor Sundays, All Souls, Circumcision, Saturday of Our Lady (also in Advent), and the resumed Sunday: the least
   solemn vacant day (§ VII.2); tools/b24/homily.py lists the Saints' Offices with a proper III-Nocturn Homily or Responsories
   (homily.json, 123 days not vacant). Matches the Ordo 1944 (2 May, 15 Jul, 9 Aug, 25 Oct, 30 Oct, 14 Nov).
 - Still wanted: more Ordos 1939-54 (non-Polish) to test; a Graduale O.P. scan (chants of the missing Masses).
 - Vigils (v190): the Missal prints Masses for 9 common vigils only (Andrew, Imm. Conc., John Bapt., Peter & Paul, Laurence,
   Assumption, Matthew, Simon & Jude, All Saints); the Kalendarium's Vigils of Matthias, James, Bartholomew, Thomas are fasts
   with no Mass (Ordo 1944 24 Jul., 23 Aug., 20 Dec.) -> mrank.js VIGIL_MASS. Added S1129v S1207v S0809v S0920v S1027v S1031v
   (tools/m39/new/spec_b6.json, or_b6.json; English orations AI, marked in src). Introits of S0920v (Ego autem sicut oliva,
   p. 564) and S1031v (Timete Dominum, p. 603) not in the Graduale GABC set (Joseph's Drive zip) -> masses.js 'pending': words
   shown with a note, no chant. NB add_masses.py re-applies ALL specs and regresses later fixes: restore other keys after running.
 - v191-192: Quad5fe = Friday in Passion Week (feria); Quad5f = the Compassion (its feast); Quad5s given Jer 18 / Jn 12.
   EpiOct = In Octava Epiphaniae (own orations and Gospel Jn 1:29-34); PurCordisBMV = Purissimi Cordis (pp. 316-318): no
   chant of it in the Graduale GABC set -> all five parts 'pending' (words only). S0910_2 has no Introit/Gradual.
 - Gloria/Credo now by M39 IX.2 and XIV with the day from the engine (app.js teDeumDay/credoDay/CREDO_FEAST/ownFeriaMass);
   Te Deum per Brev. 1924 (3L never; Simplex/Semid. not Septuagesima-Palm Sunday; Duplex+ always); checked against the Ordo
   1944 Mass lines (/tmp/gc.py style: remaining differences are Polish feasts, later supplements, or parse noise).
   Prefaces still by the old seasonPreface/keyPreface logic: to check against M39 XV next.
 - Gloria/Credo/Preface by the 1939 rank (rubricsOf still 1960-based); Saturday commemoration of Our Lady (Missal p. 40).

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
