# HANDOFF (2026-11-19). Read fully, then continue at NOW. Older detail: tools/hw39/PROGRESS.md, tools/STATUS.md.

## Setup (new workspace has nothing)
git clone https://github.com/UltraPheonix/dominican-liturgy /home/claude/dl-repo ; site = repo root (index.html, js/, data/, gabc/, art/).
Old paths in scripts: /home/claude/build/site -> repo root; /home/claude/build/gb/gb.sqlite -> tools/gregobase/gb.sqlite;
/home/claude/build/orat39 -> tools/orat39; /home/claude/dl/missal/*.pdf -> attach or download (not in repo).
Commit+push: git -c user.name=UltraPheonix -c user.email=UltraPheonix@users.noreply.github.com commit -am "..."; git push origin main.
Bump sw.js VERSION (now propria-v40) when js/css/data change. Test: python3 -m http.server 8768 in repo; tools/booklet/book.py (playwright).
pip --break-system-packages: pymupdf playwright pyspellchecker brotli fonttools. playwright install chromium.

## User (Joseph, jcampion@friars.providence.edu, Rome tz)
Wants perfect/accurate, frequent short status updates, save+push often, PROGRESS notes. Strictly Dominican texts (no Roman Missal).
Don't say "abortion rights". He may do manual work: give him concrete lists.

## Order of work
1 NOW: orations for 183 Masses lacking them (list: tools/orat39/MISSING.md). 2 booklet polish. 3 Holy Week leftovers:
washing of altars DONE 2026-11-19 (tools/chant/abl/NOTES.md); Thursday Tenebrae (Matins+Lauds, psalms sung to tones) DONE (tools/chant/ten/NOTES.md) Thursday Hours, Vespers psalm tones, Compline DONE -> NEXT Good Friday Office (Tenebrae pdf 69L-90R, Hours 90R-, Vespers, Compline) then Holy Saturday, same tools (tools/chant/ten) (Tenebrae, Lauds, Hours, Vespers, Compline; Office tab AND
holyweek page) -> check Holy Saturday tracts vs Triduum book -> Holy Sat Sanctus/Ite -> Palm Sunday procession chants
(Processionarium 1913) LAST. 4 1959 rite. 5 Mass section: site-wide 1939/1962 switch ("both, switch everywhere"), strictly
Dominican texts, Dominican Sunday numbering, consistency, Compline/Hours fixes. NB orations.js came from Divinum Officium
(maybe Roman) -> eventually verify all against Missale OP 1939.

## NOW: orations (tools/orat39) — updated 2026-11-19 12:15
DONE + LIVE (30dd20a, sw propria-v41): 103 Masses merged into data/orations.js (353 total). Latin proofed word by word vs page
images (proof_done.txt lists all 103); English hand-checked vs Latin for all 309 prayers (en_final.json; en_common.py = recurring
Commons). proof_notes.md = 3 points for Joseph. Rebuild: build_or.py -> new_or.json; merge.py (j->i, src "Missale O.P. (1939), p. N"
from pages.json; never overwrites existing keys unless --force KEY).
Missal PDF: Joseph's Drive "Dominican Chant Propers – Source Materials/3 Missal/M39.pdf" (id 1oowwnWoHvX46HV82VFg2pN58gaEa67QW,
50 MB, private: ask him to set "anyone with link" briefly, curl drive.usercontent.google.com/download?id=..&export=download&confirm=t;
copy kept at /home/claude/dl_m39/M39.pdf only for the session). Each pdf page = 2 printed pages (4 columns).
M39.pdf ALSO HAS bound-in supplements after p. 638 (pdf 358+): S. Margarita ab Hungaria (19 Ian), Immaculate Heart (22 Aug),
Sacred Heart, S. Joseph Opificis (1 Maii), B.M.V. Regina (31 Maii), then Commune/Dedication (pages N*).
Hand-made inputs: ocr_sub.json, manual_acc.json (accents, override accdict), overrides.json (raw Latin), latin_fix.json (proof
corrections, applied to accented output), en_final.json. Fuzzy OCR OFF. REJECT: S0508b, S1119b, G481 (wrong date matches).
proofimg.py M39.pdf [KEYS] -> proof/KEY.png crops (prayers searched within the Mass's own pages).
PAUSED 12:20 (Joseph: UI + priest booklet first). 18 more merged (dfc4e8d, v42: extra_final.json read from page images -> extra.py
-> extra_or.json -> merge.py). WIP: manual_match.json (S0215 S0511 S0225b S0303b S0419b S0503b S1010b S1012b S1127b S1007
found under other dates; S0819b lacks pc; S0111b Scammacca at m39lin 45655 not segmented) built by build_or.py, crops made,
NOT yet proofed/English/merged. 4 unk: AEEmiliae dociles enutriamur invitantem. Still missing also: S0504 Monica, S0703, S0729,
S0812, S1202, S0903, S0910, S0428, S0508 Mediatrix, S0814, S0113, S1113, Pasc6s, Quad3h, Quad6s, votives C..s, G470/475/587.
OLD NEXT (80 Masses still without orations; MISSING.md): 15 "prayers incomplete" (read pages; usually "ut in Commune"),
4 "from Common p. N*" (S0122 S0411 S1211 S0928b: Common prayers + saint's name declined), 3 rejected + ~59 not found
(votives/Commons C..s, Holy Week Quad6f/Pasc6s, post-1939 Blesseds: supplements in M39.pdf, Commune section, then O26 Ordo
tools/sources/ordo_op_2026.txt; give Joseph a list of anything with no Dominican source).

## Booklets (done, live): booklet.html?b=choir|priest|cong#<mass hash e.g. S1112&d=2026-11-12&ord=X&credo=I>
js/booklet.js own paginator (units->cols->A4 pages), booklet.css; buttons on Mass page. html lang="en" (EB Garamond locl
turns u->v for lang=la!). J() = Missal j-spelling. Art in art/ (same every day). Gloria/Sanctus/Agnus X = Vatican VIII
(gabc/opX-*, registered in app.js). Explicit Credo choice now always sung. Priest chants transcribed by OMR from his PDF
(tools/pdfomr/omr.py): gabc/op-praef-dominic-solemn, op-pater-solemn, op-pax-domini (f3) -> flag "sing through".
Polish todo: consecration words set apart in Canon (inside Qui pridie line), congregation 17pp vs his 14, page fill,
Benedicamus heading, readings use Vulgate + standard openings (first words may differ from Missal). Reference: his 3 PDFs' text in tools/booklet/ref/, skill dominican-mass-books.

## Prefaces (DONE + LIVE 2026-11-19, sw propria-v48)
All 20 sung Prefaces of the Missale O.P. 1939 Appendix (pdf pp. 445-461) OMR'd -> gabc/op-m39-praef-<slug>-<solemn|ferial>.gabc:
tools/pdfomr/m39app.py (staves/heads; skew-fitted line removal, gutter-aware staff ends, THR 115) + m39pref.py (pieces, text from
data/prefaces.js, 1:1 note-to-syllable pairing per staff; hand fixes in m39pref_fix.json {title: {syllable idx: notes, "Nbar"}};
report m39pref_report.txt). Proof: proofstaff.py TITLE [idx,..] -> /tmp/cp/ps_N.png; /tmp-style checks: every shared formula
(dialogue, Et ideo, Per quem) cross-checked across all Prefaces, each disagreement looked at on the scan; the remaining ones are
real print variants (Habemus Ha(g) in Epiphany+Joseph; Paschal ferial vs Requiem endings). St Dominic: 294/297 vs the old
transcription, the 3 differences verified as the 1939 print. Requiem Preface = ferial tone. Sacred Heart + St Thomas: no chant in
the Appendix -> tools/pdfomr/adapt_pref.py fits them to the solemn tone (marked "adapted" on site + booklet).
St Francis Preface (Appendix p. 25-26) added to prefaces.js, S1004. BVM Preface text corrected to the Missal (exsultantibus
animis laudare; mundo lumen aeternum). app.js prefaceChant(): solemn tone on I/II class, ferial where the Appendix has one
(Lent, Cross, Paschal, Common); fixes the variable words (BVM feast word on h; Paschal hoc/hac..die/nocte; Spiritu Sancto hodierna
die only in the octave). Shown on the Mass page and in the priest booklet when sung.
Prayer + reading tones (DONE 2026-11-19, v49): js/mtones.js (OPMassTones.oration / reading / epistleTitle) after Harrison O.P.,
How to Sing Plain Chant (1920) ch. VI 2, 5, 6 (media.musicasacra.com/dominican/howtosing.pdf; = Regulae Cantus): prayers fa-mi
inflexion, fa-mi-fa mediation, long conclusion + termination per(h) om(i)...lo(hg)rum(g); Epistle mediation RE/FA/MI, termination
podatus FA-SOL ... RE ... MI, questions on MI, conclusion in two phrases; Gospel termination FA->MI at the last accent. Used in the
priest booklet when sung (Collect, Postcommunion, Epistle with its title, Gospel). The Office (js/tones.js) uses Regulae 1965 simple
body (fa-re) = Harrison's "prayers at all other times": consistent. Data gap seen: ORATIONS.S1004 has no Collect.
Pater solemn+ferial and Pax OMR'd from the Appendix too (gabc/op-m39-pater-solemn|ferial, op-m39-pax; the old op-pater-solemn
read from a booklet had ~10 wrong notes, e.g. lo(df) for lo(fe)); booklet: ferial Pater in 3-lesson feasts/ferias/Requiem (class 4).
NEXT for the priest booklet: Ite/Benedicamus, Gloria/Credo intonations, oration tones (Collect/Postc +
Secret ending), Epistle/Gospel tones, all from the Appendix (same OMR tools; pieces already split by m39pref.py: CANTUS
SOLEMNIS/FERIALIS, ANTE AGNUS DEI, TONI ITE MISSA EST, ...).

## Holy Week tooling
hw39/*.src -> hw39/build.py -> data/holyweek_text.js. Tags == H I L R T C G F: F/ P INC X; " = " English; G:/C: "id | label".
Chant OMR on scans: tools/omrtools (heads.py, zs.py, blobs.py, prep.py, rcheck.py on :8767). Clefs: zoom to decide
(mode II often f3). gabc letters are positions (d = bottom line). chant/hymn.py (stanzas to stanza-1 melody), gb2site.py.
Sources: all on musicasacra (dominican-liturgy.blogspot.com sidebar lists exact URLs: Triduum 1927 = media.musicasacra.com/dominican/officium-hedomadae-sanctae-1927-paredes.pdf, Processionarium 1913 = processionarium-1913-Cormier.pdf, Antiphonarium 1933, Matutinum 1936, M39.pdf); GregoBase sources 11-14, 20, 21, 35, 36 = Dominican books (gabc to cross-check). Earlier list: Triduum Paredes 1927, Processionarium, Hebdomada Sancta 1959,
Matutinum 1936, Antiphonarium 1933, Missale OP 1939/1933, St Dominic Missal 1959, Graduale OP 1950 Pars Prior/Posterior.

## M33 audit (Missale O.P. 1933) — IN PROGRESS (session handoff 2026-11-20)
Source PDF: https://media.churchmusicassociation.org/dominican/M33.pdf (download to /tmp/M33.pdf).
Tools in tools/m33/ (paths inside scripts point at /home/claude/m33 + /home/claude/dominican-liturgy; edit or symlink).
Pipeline: seg.py(PyMuPDF blocks→lines.json [pdfpage,'T'|'L',line]; gz copy here) → parse.py(norm, kind regexes) →
sanct.py(sanct.json date→page) → mapall.py(map.json, mass→M33 line ranges; PAGEMAP overrides) → readings.py(align to bible/la Vulgate:
prefix formula, omitted verses, insertions) → build_readings.py(readings33.json: type,ref,title,title_en,la,en,p33,flag,first) →
dofix.py(fix garbled openings vs Divinum Officium Latin missa texts, git clone DO to /home/claude/do; →readings33b.json, gz here).
State: 393/432 masses have readings; vs old site refs 606 agree/162 disagree — most disagreements = my mis-anchoring (collect/introit).
FIX IN PROGRESS: dpmap.py = order-based DP alignment of site sections (tempore/commune/votivae from data/masses.js) to M33 introit
headings in pdf ranges tempore 44–385, sanctorale 392–643 (keep date map), commune 645–677, votive 678–745, defunct 737–744, suppl 756+.
dpmap.json output; sim() threshold 0.55. Unmatched after DP (check page images / garbled OCR): Adv2 Adv3f Adv3s Dec25_1 Jan5a Epi1 6a
Quad1t Quad2h Quad2s Quad3t Quad3h Quad5m Quad5f Pasc0t Pasc0w Pasc2w Pent0s Pent2 Pent4 Pent12 EmbSatSeptS Pent18 Pent21 ChristusRex
AscVig Dedicatio C1s C28s C32s C51s C64s C114s. Fallback for these: introit_any fuzzy over whole range / PAGEMAP manual page.
Then: feed dpmap into mapall (replace anchor for those keys) → rerun build_readings + dofix → recheck disagreements → write
data/readings33.js {massKey:[{type,ref,title,title_en,la,en}]} → js/app.js drawReading/readingText + js/booklet.js use it (Missal
title + opening formula e.g. "In illo témpore", "Fratres"). Epi1 Holy Family introit CHECKED on the scan (pdf p. 81): "Exsultat gaudio pater Justi, gaudeat..." = site, correct (OCR had lost the drop-cap line).
Pending after: #9 propers audit vs M33 (intr/grad/all/tract/off/comm + orations; data/orations.js partly Roman DO i-spelling);
#10 full introits (ant+verse+full Gloria Patri in tone+ant repeat; no GP Passiontide/Requiem); #11 Office audit (Compline first:
"Jube domne", missing chants; then all Hours); #12 UI cleanup; #13 Good Friday Tenebrae (tools/chant/ten/fri/pieces_f.py; OMR via
tools/chant/ten). Masses not in M33 → leave blank + list for user. Every push: bump sw.js VERSION (now propria-v61), message user.

## M33 — STATE 2026-11-20 08:00 (LIVE, sw propria-v56). START HERE.
Rebuild everything with ONE command: `bash tools/m33/run.sh` (sets up /home/claude/m33, M33.pdf, PyMuPDF, DO clone; writes data/readings33.js).
DONE: all 34 unmatched dpmap keys fixed by hand (dpmap.json; gaps.py lists candidates between neighbours). mapall uses dpmap ('dp') for
tempore/commune/votive. parse.py introit regex accepts "Officium." readings.py: opening match must have a consistent gap (no stray
earlier verse, e.g. Pent8 no longer starts at Luke 15:31); word-for-word gaps keep the Missal's real words (Jesus vs eum).
build_readings.py clean_tokens repairs garbled words (Pha4risaeis, discij|L pulis); fix_prefix maps tokens correctly.
data/readings33.js (394 masses, readings flagged 'weak' left out) -> js/app.js m33Readings() (pairs by Epistle/Gospel order, only when
the book matches) -> drawReading shows Missal text + title (+ "Missale O.P. 1933"); js/booklet.js uses r.la/r.en when present.
cmp.py vs old site refs: 628 agree / 317 disagree (dis.json). KNOWN BUGS to fix next (step 1 not finished):
 a) stray first verse still in refs: 5as/5af "Isaias 57:21, 58:9-14" (formula "Haec dicit Dominus Deus" -> "Hæc dicit Dóminus: Deus."),
    Quad2t "Regum 3 16:1, 17:8-16" (drops "Eliam Thesbiten"), Quad4t "Exodus 31:12, 32:7-14" (drops "Descende"), Pasc2w "Lucas 2:1, 3:21",
    Adv3f "Isaias 10:24, 11:1-5" ("Dicit Dominus Deus egredietur" lost "Haec ... : Egredietur"), Quad6h 1 Cor 11:18. Cause: the pop-back loop
    and op block in readings.align when the Missal's incipit words differ from the Vulgate; fix = in the opening region use the OCR tokens.
 b) Ember Saturdays/Pent0s/Adv3s/Quad1s: "Daniel 3:49-52" lesson flagged weak (the Benedictus es hymn, not a reading) - drop it.
 c) check Dec25_1 (Isaias 9 lesson: Dominican prophecy, keep?), Dec25_3 gospel Matt 2 (= last Gospel, drop), Jan1 (Titus 3 / Luke 2:15 =
    Dawn Mass: wrong anchor), Epi1 gospel "Regum 2" (weak), ChristusRex/Pent23 swapped?, C1s/C51s/C55s/C79s commons, 246 sanctoral.
 Verify on the page: python3 -c "import fitz;d=fitz.open('/tmp/M33.pdf');d[PAGE].get_pixmap(dpi=110).save('/tmp/p.png')" then view.
Then steps (2) is done (switch live) -> (3) propers audit vs M33 -> (4) full introits -> (5) Office/Compline -> (6) UI -> (7) GF Tenebrae.
Masses with no readings in M33 (blank): Pasc6s Quad6f Quad6s S0115 S0205 S0421 S0524 S0618 S0727 S0805 S1121 S0113 S0915 G515 G555 G566
G587 + 18 "b" (2nd) Masses: S0110b S0111b S0130b S0303b S0401b S0409b S0419b S0422b S0521b S0528b S0708b S0727b S0811b S0905b S0907b
S1012b S1013b S1107b S1127b S1209b.
PROMPT TO CONTINUE (paste into a new Claude session): "Repo UltraPheonix/dominican-liturgy (add_repo push, clone /home/claude/dominican-liturgy).
Read tools/HANDOFF.md last section 'M33 — STATE'. Run bash tools/m33/run.sh, then fix KNOWN BUGS a-c, rerun, push. Same rules as before."

## M33 — 2026-11-25 (sw propria-v57). Step 1 (readings) DONE except the leftovers below.
run.sh no longer reruns dpmap.py (hand anchors in dpmap.json kept; Jan1 = line 9859, p.73). readings.py: stray short runs far away dropped;
opening = Missal's own words; hyphen/OCR junk repair ("civi4L tatem", "Ddmi< nus"); drop caps (Fratres, Hæc dicit, Caríssime).
build_readings.py: reading cut at Alleluia/Dominus vobiscum; same reading copied from a clean copy (by first words); scan-text mode for
centos when the scan is clean; English formula prefixes. vfix.py = hand-checked readings (page images) -> fixes.json (Dec24, Dec25_1/3,
Jan1, Jan5a, Epi1); run.sh runs it. run.sh drops any reading with scan junk (site shows the Vulgate there).
Leftover weak/dropped (show Vulgate): Ecce sacerdos cento (C32s S0510 S0519 S0606 S1104 S1111 S1117 S0530b S0803b S1023b S1126b),
Apoc 14:13 (S1102*), S0531 S0914 S0919 S1002 G475 Quad6t, and ~9 with scan junk (Quad4h Pent0m S0324 S0325 S0424 S0921 S1208 ...).
User order of remaining work: step 4 (full introits) -> 5 (Office, Compline first) -> 6 (UI) -> 3 (propers audit) -> 7 (GF Tenebrae).

## Step 4 DONE (sw v58): full Introits. js/app.js fullIntroit(body, header, key): antiphon + verse + whole Glória Patri in the mode's
Introit tone (data/introit_gp.js = Graduale O.P. 1950 pp. IX-XI, GregoBase 7600 7551 8211 7410 9643 7409 7848 8042, own clef) + clef
+ antiphon again. No GP for Quad5*/Quad6*, Requiem (C114*, S1102*); files that already print "sine Gloria Patri, sed repetitur" left as
they are. Applied on the Mass page (drawSlot) and in booklets (booklet.js chant(), old rubric line removed). Checked all 177 introits
(node) + rendered Epi1/Quad5/C114s/booklet in Chrome. Congregation text view now uses the Missal readings too.

## Step 5 (Office) — Compline DONE (sw v59). Source: Completorii Libellus O.P. (Suarez 1949) =
media.churchmusicassociation.org/dominican/completorium-1949-suarez.pdf (scan, no text; 78 pdf pages = 2 book pages each;
pdf idx 7-11 Ordo, 12-17 Te lucis tunes, 16-17 Custodi/Salva nos/Preces/Visita, 18-? weekday psalms, 66-67 procession).
tools/office/compline49.py rewrites the shared Compline blocks in data/office/common.json: Jube domne + "tribuat nobis omnipotens
et misericors Dominus"; Lectio 1 Petri 5 with Tu autem; Adjutorium, Pater secreto, Dominican Confiteor/Misereatur (Hebdomadarian +
choir, "et vobis fratres"/"et tibi Pater"), Converte nos; Capitulum Jerem. 14 + Responsory In manus (Dominican form, with/without
Alleluia); Visita with Dominus vobiscum/Domine exaudi; Benedictio by the Prior "super vos" (absent: super nos); procession: Salve
Regina (Dominican text, "salute"), Concede nos, O lumen, Ora pro nobis, Concede quaesumus, Fidelium animae, Pater+Credo secreto.
Chant: C49-inmanus.gabc (OMR by eye from C49 p.8, Gloria Patri added; = Gillet 5758 melody), C49-telucis-viii.gabc (Gillet 4779
st.1-2 + ordinary doxology Praesta Pater; 4779 has the Marian stanza Maria mater gratiae, which was shown EVERY day before).
tools/office/jspell.py: consonantal i -> j in all Office text (Vulgate j-words), js/tones.js regexes accept i/j.
OFFICE STILL TO DO (big): the Office data is Divinum Officium "Ordo Praedicatorum 1962" (classes I-IV, 1960 rubrics): pre-1955
ranks (Totum Duplex, Duplex, Semiduplex, Simplex), Compline Sunday psalms on Doubles I/II cl., feasts of the Lord, BVM, Apostles
etc. (C49 p.7), Preces at Compline/Hours, Te lucis tunes by rank/season (C49 pp.9-17), Marian Te lucis doxology on BVM feasts,
weekday psalm antiphons (C49 p.22ff) vs current. Needs either DO pre-1955 OP data or a rubric layer; then audit every Hour.

## Step 6 UI (sw v60): Report-an-error button hides while scrolling, smaller on phones (it covered the chant); Holy Week day tabs fade
at the right edge on phones (more days to swipe). FOUND, NOT DONE (needs a decision / big): the Mass calendar and the Office use the
1960 rubrics (I-IV class, "III class" shown in headers; data/ordo.js "Missale O.P. 1933, with the rubrics of 1960"; Office = DO
OP 1962), and Holy Week has a "Reformed 1959" toggle — all conflict with "pre-1955 OP rite only". Pre-1955 needs the old ranks
(Totum Duplex / Duplex / Semiduplex / Simplex, Sundays I/II class), octaves, commemorations, preces: a rubric engine of its own.
Remaining after that: step 3 propers audit vs M33, step 7 Good Friday Tenebrae.

## Step 3 started: tools/m33/propers_audit.py -> tools/m33/propers_audit.md = 43 possible Introit/Gradual/Offertory/Communion
mismatches site vs M33 OCR (after filtering drop caps / scripture refs). Many are OCR or anchoring noise (Commons share pages), but
some look real, e.g. Quad4h Communion: site "Lutum fecit" (= Wednesday's), M33 p.147 "Domine memorabor justitiae tuae solius";
Quad2h Communion site "Qui manducat", M33 p.121 "Justus Dominus..."; ChristusRex Communion; AscVig Communion. Check each on the pdf
page, then fix the chant id in tools/sources (masses.js is generated).
- Compline chant (v61): short lesson Fratres: Sobrii + Tu autem and the Adjutorium notated from C49 p.2 (js/tones.js FIXED.lectioCompl / adjutorium).
