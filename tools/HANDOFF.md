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
