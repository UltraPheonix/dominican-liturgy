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

## Step 3 (propers audit) DONE 2026-11-25 (sw v62). All 43 lines + a stricter re-audit (propers_audit.py now checks in/gr/of/co by
words 2-6 of the gabc text) checked on the page images. Fixes: tools/m33/propers_fix.json -> propers_apply.py (patches data/masses.js,
idempotent; build_masses.py calls it before writing; '_add_chants' adds new chant entries, e.g. r3596 = Roman-melody Dilexisti gradual,
no OP melody in GregoBase). Fixed: Jan5a (Lux fulgebit, Benedictus qui venit), Quad1t gr Dirigatur, Quad2h in Deus in adjutorium,
Quad4h co Domine memorabor, Pent6 of Perfice gressus, AscVig of Ascendit Deus + co Pater cum essem, C11s C18s C30s C35s C39s C42s C45s
C48s C55s C76s(=Holy Spirit in Septuagesima, M33 p.43*) C82s C104s, G369 (Vigil of Andrew: of Gloria et honore, no Alleluia), G502_3
(no Alleluia). Afferentur (C45s/C48s) = r1107 Roman melody (none in Graduale O.P.). M33 anchors fixed in dpmap.json: G470 (=S. Pius V
p.478), G481 (=S. Philip Neri p.493), G502_3 (p.512), C79s (Mass III p.693), ChristusRex (p.618), C76s. absent.json = Masses not in M33
(C1s Commune Apostolorum: no such Mass in the 1933 Commune; chants kept from the Graduale, readings blank). run.sh: cmp.py optional.

## Step 2 leftovers (readings) DONE 2026-11-25 (sw v63). All in tools/m33/vfix.py (page images checked): Ecce sacerdos cento (C32s S0510 S0519
S0606 S1104 S1111 S1117 S0530b S0803b S1023b S1126b), Apoc 14:13 (S1102_3), S0914 S0919 S1002 G475(=B. Imelda, suppl. p.2) Quad6t, drop-cap
junk (Quad4w Quad4h Pent0m S0324/S0325 S0424 S0921 S1208), recurring scan words (GLOBAL list: Optávi, parábolam hanc, Jesus, Amen...;
vocabulary check = every la word must exist in bible/la), verses lost at column breaks (Epi Matt 2:5-9, Quad2s Luke 15:14-20, Quad4f John 11:7,
Quad6h 1 Cor 11:27-28, Quad6t Mark 14:5-8, Quad6w Luke 23:23-32), Matt 25:14-23 garbled (Statuit gospel), Quad1w = 3 Reg 19:3-8.
Anchors: sanct_entry.json (S-key -> M33 sanctoral entry line, for saints whose date moved: S0118 S0214 S0215 S0511 S0703 S1009 S1010b S0216b
S0503b S0819b) used by mapall.py; dpmap.json adds S0508 (= B.M.V. Mediatrix, suppl. p.4, dated 31 May in M33), S0703, S0910 (Navarrete 1 Jun),
S1003 (Thérèse, suppl. p. 782 "in Missionibus"), S1007 (Rosary = Dominica I Octobris p.595), S1102/_2/_3 (three Masses p.623-626), S1113
(anniversary = In anniversario defunctorum, pro pluribus), Pent23 (= Dominica XXI post Oct. Trin., p.375; Dominica XXII et ultima p.376 =
Col 1/Matt 24 has no site key). run.sh: sanctoral readings stop at the first Gospel (next undated Mass leaked in). absent.json: post-1933
Masses (titles with year >= 1934), S0501 Joseph Opificis, S0531 Regina, S0903 Pius X, S0428 Paul of the Cross, S0902b Ingrid, C1s.
js/app.js m33Readings: the M33 text now wins even when the book differs (Dominican readings), site ref only where M33 gave nothing.

## Step 3 Office audit — IN PROGRESS (paused 2026-11-25 14:25, sw v64). START HERE NEXT.
DONE (Compline): Te lucis tunes by rank/season, C49 pp. 9-17 = data/chant/op/C49-telucis-{adv,sab,dom,fer,i,tdii,td,d,sd}.gabc (melody =
GregoBase 9952 9951 9953 9954 9955 9956 9957 9958 9959, Antiphonarium 1933; spot-checked vs C49 p.16; stanzas 2-3 by tools/chant/hymn.py,
Amen = torculus/pes on the final as C49 prints). js/office.js teLucisTune(ctx, date): tempore Sat/Sun of Advent -> adv, Sat/Sun per annum
(Oct. Epiph.-Lent, Oct. SCJ-Advent) -> sab/dom, ferias -> fer; feasts: I cl -> i, Totum Duplex II cl/Apostles -> tdii, Totum Duplex -> td,
Duplex -> d, Semiduplex and below -> sd; reads old ranks from the title when the rubric engine supplies them, else 1960 class II->tdii,
III->d, IV->sd. Returns null (default C49-telucis-viii = GB 4779, Antiph. add. p.13) for Christmastide and Lent->Oct. SCJ: those seasons have
PROPER Te lucis tunes in C49 (Officium de Tempore from p.36: Christmas p.38-39, Holy Name p.40-41, ...) -> TODO transcribe/find in GregoBase.
Weekday Compline antiphons (C49 p.22-35) = Antiphonarium 1933 melodies: Mon 6965 (=Ta1-319 ok), Tue now 6718 (was Jandel 1862 18778, lacked
"in aeternum"), Wed 6087 (=Ta3-373 ok), Thu 6656 (=Ta2a-262 ok), Fri 5746 (=RC-voce-mea same melody), Sat now 9974 (Ta3-696 had junk text),
Sun 9950 (=RC-miserere same). TP at Compline: 'Alleluia, alleluia, alleluia' -> 6913 (C49 p.63), only in Compline (office.js).
NOTE C49 p.63: Saturday after Easter -> Sunday psalms; other TP days Sunday OR weekday psalms "juxta rubricam (pag. 7)" -> rubric engine.
NEXT in step 3: preces at Compline (C49 p.19-20: Kyrie, Pater secreto, Et ne nos, In pace in idipsum (GB 6043 = C49 p.46?), Credo, Carnis
resurrectionem, Dignare Domine... when "Preces dicendae fuerint") -> check common.json Compline preces block; then the other Hours against
Breviarium 1909 / Antiphonarium 1933 (GregoBase source 11 has the Antiphonarium 1933: query gb.sqlite by incipit, source=11), Little Hours
hymns/chapters/short responsories, Prime (Pretiosa, martyrology), preces at Lauds/Vespers/Prime. Then step 4 (GF Tenebrae), step 5 (plan only).
Test: python3 -m http.server 8768; /tmp scripts were: playwright page with localStorage officeChant=1, list .o-chant data-id per hour.

## Clean-up pass 2026-11-25 afternoon (sw v65-v70). START HERE NEXT (Joseph's list: Mass chants, tones, Office).
DONE: Mass: no Alleluia from Septuagesima (app.js massParts); Tracts infra Septuagesimam for Commons and saints Jan-Apr
(propers_fix.json 'lent_tr', from M33); Paschal Alleluias stripped outside Paschaltide incl. unmarked ones and E.T.P./Extra T.P. endings
(app.js seasonalGabc/stripAlleluia/etp; KEEP_AL for Epi2 of, CorpusChristi/C62s in, S0806 co, C75s); only one Alleluia outside
Paschaltide; Tract dropped outside Lent when an Alleluia exists (SCJ); Sundays always solemn Preface (Trinity on ordinary Sundays,
isSundayMass/keyPreface); a Mass picked from the list opens on its own next date (showMass -> nextDateOf). Chant layout: tidyGabc
(one clef per staff, no doubled double bars), fullIntroit no clef before the repeat. Reading titles in their own columns.
Office: tools/chant/office_audit.py (Antiphonarium 1933 replaces OMR/Roman melodies; Roman without OP source dropped; log
office_audit.txt). Compline: Te lucis tunes by rank/season + Christmas tune (C49-telucis-nat, transcribed from C49 p.38-39 and checked
by rendering), In manus with Alleluia and Verbum caro / Omnes de Saba in Christmastide (office.js complineSeason), Jesu nostra redemptio
split by period (5793-res/asc/pent), Preces (office.js complinePreces/PRECES; simple tone in tones.js).
CHECK: tools/check/year.py (Mass, every day of a year: Alleluia in Lent, missing Tract, Tract outside Lent, Sunday ferial Preface,
Alleluia left in in/of/co) — clean for 2026, 2027, 2029, 2032.
OPEN: S0915 Seven Sorrows: M33 sings 'Stabat sancta Maria' as an Alleluia (and 2nd Alleluia 'O vos omnes'), site has the Tract form only.
Seasonal Te lucis still missing: Epiphany octave, Holy Name, Ascension, Pentecost, Corpus Christi, SCJ, BVM (C49 pp.40ff); Office of the
Dead and other pieces left as text after dropping Roman melodies; Kyrie of the Preces not notated; Vespers/Lauds/Little Hours/Matins
audit (Joseph's Office list B-F); rubric engine (pre-1955 ranks) for Compline psalms, preces, Te lucis ranks.
GitHub Pages: a 'pages build and deployment' run can fail with a GitHub 500 ("Failed to create deployment") when pushes come fast;
the next push or `gh run rerun <id> -R UltraPheonix/dominican-liturgy` redeploys.

## Compline perfected against Completorium O.P. 1949 (C49) — 2026-11-25 (v72–v76)
Source scans: /tmp/c49/C49.pdf; OCR (tesseract ita) of pp. 1–119 in /tmp/c49/ocr/pNNN.txt (+ .png at 300 dpi);
/tmp/c49/clean.py A B prints the text of pages A–B. Page n ↔ pdf index (n-22)//2+18 (left half even, right half odd).
Done:
- Opening (pp. 1–4): Jube/Noctem, lesson, Adjutorium, Converte, Deus in adjutorium, Laus tibi/Alleluia measured (js/tones.js FIXED, f3).
- Prayer tone (p. 20): colon = metrum, semicolon = flexa, flexa at the last comma of a long member; simple conclusion ends
  sæculó(h)rum(f); Dominus vobiscum before Visita and Benedicamus (dvPriest in office.js); Benedicamus f3 h…f f / g g g g h.
- Psalm tones: III mediant 'k jr j 'i ir j, termination "'j ir h 'j jr ih" (p. 18, 26); Immittet = C49 variant (IIIb), Voce mea VII d,
  Adjutor meus mapped (6656), Holy Saturday/Easter Alleluias (6688, C49-alleluia1, ending G).
- Te lucis tunes: tools/chant/telucis_seasonal.py builds C49-telucis-{hn,hn2,hf,tri,cc,scj,bvma,bvmb,epi}: each feast's tune is the
  melody of its own hymn in the Antiphonarium 1933 (Jesu dulcis memoria, Jesu decus, O lux beata Caelitum, Adesto, Verbum supernum,
  4884, Aurora soli praevia); Sacred Heart transcribed (pp. 72–73). teLucisTune() chooses by date/title; teLucisText() swaps the
  doxology (Qui natus / qui apparuisti / Jesu tuis obediens / Qui Corde / Maria Mater gratiae + Qui natus).
- Lent (pp. 46–48): lentText() adds R. In pace (Sat, Sun, feasts) / In manus; Passiontide In manus without Gloria (C49-inmanus-pass).
- Holy Week (pp. 55–60): Wednesday without Salve; Thursday/Friday per C49 (Ps 50 on Friday); Holy Saturday = HOLYSAT rows;
  Easter–Friday four Alleluias; Spiritum nobis to Tuesday (xform() '@x:<hash>:<how>' rows).
- Our Lady (pp. 74–105): maryText(): Virgo Maria / Sancta Dei Genitrix / Ecce Virgo; Sub tuum on Compassion, Mediatrix, Assumption,
  Holy Name of Mary, Seven Sorrows; Ecce ancilla on the Annunciation.
OPEN (Compline):
- v78 saints' tunes done (crc tom pb mm spd domtr mdol ros ang fra ter ck os alb; keys must not clash with the rank keys
  dom/sd/d/td…). Still to do: St Antoninus (p. 90, VII), St Augustine (p. 99, VIII), St Rose (p. 100), St Louis Bertrand (p. 110),
  St Teresa alternative tune (p. 112, VI); Septem Fundatores' Nunc dimittis antiphon (p. 83); the Rosary is matched by title only
  (1954: first Sunday of October with octave — needs the calendar engine).
- Our Lady in Lent (Christe qui lux + 2 stanzas, p. 77) and in Paschaltide (Jesu nostra + 2 stanzas, p. 78).
- Proper antiphons without chant: Sancta Dei Genitrix (Ib, p. 81), Compassion/Seven Sorrows Virgo Maria non est ulla (pp. 86, 101).
- Good Friday Ps 50 should be said without chant; Christus factus est incipit only at the start of the Triduum psalms.
- Kyrie of the preces notated (p. 19); Salve/O lumen against pp. 118–122.
- v77: Preces fully chanted (Kyrie p. 19 = FIXED.kyrieC; Vitam aeternam. Amen = FIXED.vitamC; versicles 'h fr f').
  A rubric (<n>…</n>) before a hymn no longer stops the hymn being notated. Veni Creator (7240), Quicumque Christum (6903) mapped.
  Hymn audit (2026–27): every Compline hymn has chant. Still without chant: ~29 Matins hymns (Nocte surgentes, Summi largitor,
  Quem terra, Jam Christus astra, Pange lingua … lauream, Urbs beata, Huius obtentu, …): not in the Antiphonarium 1933 —
  take them from Matutinum O.P. 1936 (CMAA site) when doing Matins. Preces at Lauds/Vespers/Prime are not in the 1962-based
  data at all: they come with the pre-1955 rubric engine.

## PLAN — the 1909 Dominican Office (Breviarium S.O.P., Cormier 1909) as a second rubric set — 2026-11-25 (not started)
Research: the 1909 edition is the last printing of the medieval Dominican Office: its own psalter (e.g. Sunday Prime has
Ps 21, 22, 23, 24, 25 as of old + 53, 118; Matins, Lauds and the little hours by the old cursus), before the Order took the
Pius X psalter (Divino afflatu 1911) in the 1920s. Calendar with Totum Duplex / Duplex / Semiduplex / Simplex / iij lectionum,
Rubricae generales (pdf b1 pp. 40-70: occurrence, concurrence, octaves, commemorations), Psalterium per hebdomadam (pp. 85-),
Proprium de Tempore, Proprium Sanctorum, Commune; two volumes (b1 1577 pp., b2 ~1300 pp.), scanned, no text layer.
Sources: Breviarium-1909-1/2-optimized.pdf (CMAA site); Antiphonarium O.P. 1862 (Jandel, 2 vols) for the chant of the old
psalter (the 1933 Antiphonarium follows the new psalter); the 1933 books still serve for hymns, tones and common pieces.
OCR: tesseract 'lat' (tessdata_best, installed from raw.githubusercontent.com) on 300 dpi half-pages (two columns) works well.
Steps:
 1. OCR both volumes by column → tools/b09/ocr/*.txt; parser to blocks (rubric, antiphon, psalm ref, hymn, lesson, prayer).
 2. Ordinary + Psalter: every Hour for each weekday (1909 cursus), psalm texts reused from the current psalter data (same Vulgate),
    antiphons/versicles/chapters from the OCR; checked against the scans.
 3. Calendar 1909 (ranks, octaves, O.P. saints as of 1909) and a rubric engine: occurrence/concurrence per the Rubricae generales,
    translation, commemorations, 9 or 3 lessons, Vespers I/II split, preces, Te lucis/hymn tunes by rank. The same engine,
    with the 1954 rule set, then replaces the 1962-based data for the "1954" Office (the pending rubric-engine task).
 4. Proper of Time, then Sanctoral and Commons (OCR → data/office1909/), English from Divinum Officium where texts coincide.
 5. Chant: 1862 Antiphonarium (OCR of pages + GregoBase where present; transcription where not), tones from the 1933 books.
 6. UI: an "Office: 1909 / 1954" switch in Options; same pages, same chant rendering; checker for a whole year.
### 1909 — state at pause (2026-11-25 21:55)
- Done: Office switch in Options (#rite select, office.html; js/office.js BASES {'1954': data/office/, '1909': data/office1909/},
  state.rite in localStorage 'officeRite'; for 1909 rowsOf()/blockText() return the generated data untouched (no 1954 fix-ups)).
  The 1909 option is disabled ("in preparation") until data/office1909/ exists — remove `disabled` in office.html then.
- Psalm verses for all 150 psalms (Latin + English) can be rebuilt from data/office/psalter/*.json (<n>ps:v</n> lines).
- OCR route (if no text PDF): tools/b09/ocr09.py (tesseract 'latf' = tessdata_fast lat, psm 3, 250 dpi; ~2.5 s/page; both
  volumes ≈ 1 h on 2 cores). Started then stopped: Joseph is supplying a 1909 Breviary PDF with a text layer — use that instead.
- 1909 layout (vol. 1 pdf idx): 10-23 De anno, 24-37 Calendarium (ranks: Totum Duplex, Duplex, Semiduplex, Simplex, Tres Lectiones),
  40-70 Rubricae generales (+ Index rubricarum p. 40), 70 Modus terminandi orationes, 76 Index alphabeticus, 82 Psalmorum index,
  88- Psalterium (Dominica ad Matutinum p. 3 … Sabbato), then Proprium de Tempore, etc.

## MASTER PLAN (Joseph, 2026-11-25 22:10): chant everything possible in BOTH Offices; no inferred melodies in 1954
Rule: in the 1954 Office use only melodies printed in a Dominican book (AM 1933, C49, Matutinum 1936, GB 1950) — do not
reconstruct. (v81's tones for the chapter office of Prime were reconstructions and were reverted in v82: the AM 1933 prints
no melody for Pretiosa … Dirigere, the Rule or Ps 116.) Preces: Dominicans have them only at Prime and Compline (AM 1933
p. 147, C49 p. 19) — both done (v77, v79).
Sources (media.churchmusicassociation.org/dominican/):
- antiphonarium-1933-gillet.pdf (day Hours only; GB source 11), completorium-1949-suarez.pdf (GB 13),
  matutinum-1936-gillet.pdf (GB 12: 123 pp.; Toni communes pp. 1–21 = Domine labia, Invitatory/Venite tones I, II, IV A,
  IV B (Christmas), V, VI, VII, VIII…, Matins versicles, responsory rubrics, Benedictiones ante lectiones, lesson tones,
  Te Deum p. 230; then Matins of 14 solemnities only: Christmas 21, Epiphany 49, Ascension 61, Pentecost 78, Corpus 84,
  St Joseph 102, Immaculate Conception 124, St Thomas 133, St Catherine 147, Peter & Paul 152, St Dominic 173,
  Assumption 185, Rosary 198, All Saints 209). GB has 38 pieces of it (Venite IV A = 10539, Te Deum 4207).
- antiphonarium-1862-jandel-t1/t2.pdf (GB 35/36, ~125 pieces): the full Antiphonary incl. Matins, old psalter → 1909 Office,
  and the only source for ordinary Matins antiphons/responsories where the 1954 texts agree.
- Breviarium-1909-1/2-optimized.pdf (scans; Joseph is supplying a text PDF) → 1909 texts and rubrics.
Order of work:
 A. 1954 Matins frame from Matutinum 1936 Toni communes: Domine labia, invitatory + Venite in the tone of the invitatory
    (transcribe I, II, IV B, V–VIII; IV A = GB 10539), Matins versicles, absolutions/blessings, lesson tones, Te Deum (done).
 B. 1954 Matins of the 14 solemnities (≈250 pieces: GB 12 + transcription from the scans with /tmp/c49-style tools:
    notes2.py/staff measuring; see the C49 notes above).
 C. Missing hymns (~29 Matins hymns; tools/chant audit in HANDOFF v77 note): only from a printed Dominican source.
 D. 1909 Office: texts from Joseph's PDF → parser → data/office1909/ (format as data/office/; psalm verses from
    data/office/psalter); rubric engine from Rubricae generales; then chant: 1862 Antiphonary (GB 35/36 + transcription),
    tones/hymns from 1933 books where identical. Enable the switch (office.html: remove `disabled` on option 1909).
 E. Rubric engine with the 1954 rule set replaces the 1962-based data (Compline psalms by rank, preces days, Te lucis ranks,
    octaves, Rosary on the 1st Sunday of October, etc.).
Tools: OCR with tesseract 'latf'/'lat' (tessdata from raw.githubusercontent.com/tesseract-ocr/tessdata_fast|best into
/usr/share/tesseract-ocr/5/tessdata/), tools/b09/ocr09.py; screenshot/test helpers live in /tmp/pg (recreate: playwright +
/usr/bin/google-chrome, `python3 -m http.server 8768` in the repo).
- Extra source (Joseph's Drive "Dominican Chant Propers – Source Materials/Antiphons" = CMAA a1/a2a/a2b/a3/a4.pdf): the provisional
  O.P. Antiphonarium pro Liturgia Horarum (post-1970). Each chant carries a siglum: AG (AM 1933), AJ (Jandel 1867-70),
  MG (Matutinum 1936), AN (Nocturnale S.O.P., ed. Ammosaulicus, Bonn 2006 — traditional O.P. Matins; not yet obtained).
  Pieces with AG/AJ/MG/AN sigla and the same text may be used as printed Dominican melodies (transcribe from the scans).
- Joseph's Google Drive (Drive connector) has the 1909 Breviary as "cropped" PDFs (shared by olotac@gmail.com):
  prior pp. 1-768 = 1HRo3g0vtYa72N_ad4Nn50aIKH8HFVbnU (235 MB); prior pp. 769-1577 = 1Qd4tK1MbESCGPcrv_b4YiV2VmYmIJu0S (250 MB);
  posterior pp. 1-481 = 1tRQFd_fEUhJEJrulKKcuQXsVK2dF7sOT (141 MB); posterior pp. 482-end not found. Text layer not yet checked
  (too large for the Drive tool's base64 download: ask Joseph to attach them, or use the CMAA scans + tools/b09/ocr09.py).
  Also matutinum-1936-gillet (1).pdf = 1w2PdWfEHZACazKofEG8YlPY1C9wz73nd. No Nocturnale S.O.P. (2006) in the Drive.
- 2026-11-26: Joseph attached the 1909 Breviary with a text layer (vol. 1 1577 pp., vol. 2 1369 pp.; files in
  /mnt/user-data/uploads/Breviarium_Cormier_1909_*_text.pdf — re-request if the session is new). Their text layer was
  extracted column by column with tools/b09/extract.py → tools/b09/text/v1.txt.gz, v2.txt.gz ('\f### <pdf index>' per page,
  '||' between columns). Quality: an old OCR — accents often wrong (h6die, declindmus), some word order jumbled within lines.
  Plan: use it for structure/finding pages; restore wording by matching to known texts (Divinum Officium Latin, our 1962 data,
  Vulgate psalter) and re-OCR doubtful pages with tesseract 'lat' (tessdata_best) from the page images of the same PDF.
  Also in Joseph's Drive folder "Antiphons" (and on the CMAA site as n1/n2/na/nc.pdf): the NOCTURNALE S.O.P. (Ammosaulicus):
  n1 = front matter, n2 = Dominica per annum (Ordinarium of Matins), na = Proprium de Tempore, nc = Commune Sanctorum —
  born-digital PDFs whose notes are set in a chant font: decode the font glyphs to gabc → the Matins chant for both Offices.
### 1909 — progress 2026-11-26
- tools/b09/extract.py (column + line clustering; good reading order) → tools/b09/text/v1.txt.gz, v2.txt.gz.
- tools/b09/latdict.py: accent restorer — dictionary of accented forms from Divinum Officium Latin (clone:
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/DivinumOfficium/divinum-officium /home/claude/divinumofficium/divinum-officium);
  fix_line('nos h6die … declindmus') → 'nos hódie … declinémus'. DO also has the pre-1911 Roman psalter ('Daya…' sections in
  horas/Latin/Psalterium/Psalmi/*.txt) and pre-Urban hymn texts — use them to restore wording/accents.
- tools/b09/outline.py v1 86 246 → tools/b09/outline_psalter.txt: the psalter (vol. 1 pdf 86-245) with psalm verses skipped,
  accents restored. Proprium de Tempore starts pdf 246 (Sabbato ante Dom. I Adventus).
- 1909 cursus (= pre-1911 Roman distribution, confirmed from the OCR): Sunday Matins 12+3+3 psalms (1-3, 6-14 | 15-17 | 18-20);
  Lauds Sun 92, 99, 62+66 (no Gloria after 62), Benedicite (+Benedicamus Patrem, Benedictus es; no Gloria), 148+149+150;
  ferial Lauds Ps 50 + 5 / 42 / 64 / 89 / 142 / 91, 62+66, ferial canticle (Isaiae 12, Ezechiae, Annae, Moysis Ex 15, Habacuc?,
  Moysis Deut 32), 148-150; Matins Mon 26-37, Tue 38-51, Wed 52-67, Thu 68-79, Fri 80-96, Sat 97-108; Vespers Sun 109-113,
  Mon 114-120, Tue 121-125, Wed 126-130, Thu 131-136, Fri 137-141, Sat 143-147; Compline daily 4, 30(1-6), 90, 133 + Nunc dimittis;
  Prime 53 + 118 (1-32) (Sunday adds 21-25 in Septuagesima/Lent per 'Modus dicendi Primam', pdf 118), Quicumque on Sundays
  to check; Terce/Sext/None Ps 118 in sections. Prime antiphons by season pdf 115-117 (e.g. per annum Sunday 'Gloria tibi
  Trinitas', ferial 'Deus exaudi orationem meam'). Prime, in chapter: Pretiosa … Obitus/Anniversarium prayers (pdf 110-112).
NEXT: write tools/b09/psalter1909.json (per day/hour: antiphons, psalms, chapter, hymn, versicle, prayer, seasonal variants)
from outline_psalter.txt (fix wording against DO), then build.py → data/office1909/ for the date range, Ordinary first.
### 1909 — Ordinary LIVE (2026-11-26 08:40, sw propria-v83)
- tools/b09/make_psalter.py → tools/b09/psalter1909.json (the whole 1909 Psalter: invitatories, Sunday Matins 3 nocturns with
  pe/pt(leonine)/adv/pass antiphons, ferial nocturn 6 pairs, Lauds/Vespers per day, Prime (Sunday Sept.–Palm 21–25), Terce–None
  chapters + R.br. by season, Compline, memorials BVM/Cross). Checked doubtful lines vs page images (pdf 93–101, 113–121, 216–220).
- tools/b09/build.py → data/office1909/ (426 days 2026-11-01..2027-12-31; all blocks in common.json; psalm shards from DO
  Psalmorum Latin/English, keys '§NN.L118a'/'§NN.E…'; hymns + fixed texts (Compline, Pretiosa, Confiteor, Te Deum) reused from
  the 1954 data by id; English for antiphons/chapters via a DO Latin→English line map (fallback: Latin)).
  Seasons: adv, nat(proper), pe, sept, cin(Ash Wed–Sat), quad, pass, tri(Holy Thu–Low Sat: proper), pasch, pent(Ascension–
  Corpus Christi octave: proper), pt. Proper parts show "De Proprio de Tempore (in præparatione)".
- office.html: 1909 option enabled. Test: /tmp/pg/t1909.py (playwright, 18 dates × 8 hours × chant on/off, no errors).
NEXT (Joseph 08:13: Passiontide and Triduum must be perfect): Proprium de Tempore from v1 pdf 246 → tools/b09/tempora1909.json:
  Advent first (starts 29 Nov), then Christmas, Lent, Passiontide, Holy Week + Triduum (line by line vs scans), Easter…; then
  Sanctoral/Commons (vol. 2) + Rubricae generales precedence; then chant (Jandel 1862, Nocturnale).
### 1909 — Advent short propers LIVE (2026-11-26, sw propria-v84)
- tools/b09/make_tempora.py → tempora1909.json (keys 'adv<week>-<weekday>', 'pre-adv' = Saturday before Advent I): invitatories
  (Regem venturum on ferias, Prope est jam on the Ember days), Sunday Lauds antiphons (also Prime=1, Terce=2, Sext=3, None=5),
  Benedictus/Magnificat antiphons for every Advent day, Sunday prayers (said all week; Ember-day Lauds prayers), First-Vespers
  responsories (Missus est, Ecce Dominus veniet, Qui venturus est, Non auferetur), O antiphons from 17 Dec (no Vespers preces),
  Lauds antiphons of the six ferias before the Vigil, Prime R.br. verse "Qui venturus es in mundum". Source: v1 pdf 246–283.
- build.py: TP(d,key) reads tempora1909.json; Saturday-before-Advent Vespers = Advent chapter/hymn/R.
STILL MISSING in Advent: Matins lessons + responsories (Isaiah; Sunday sermons/homilies; pdf 246–283), St Thomas (21 Dec)
  commemoration antiphon "Nolite timere" (p273), Vigil of Christmas (p280–283). Sanctoral not yet (Dec 8 etc.).
NEXT ORDER: Advent lessons → Christmas–Epiphany (pdf 284–373) → Sundays after Epiphany (374–415) → Septuagesima–Lent → Passiontide
  + Holy Week + Triduum (Joseph: must be perfect; check every line vs scans) → Paschaltide → after Pentecost; then vol. 2.
