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
washing of altars (Triduum Paredes 1927 pp~95-111) -> Triduum Office (Tenebrae, Lauds, Hours, Vespers, Compline; Office tab AND
holyweek page) -> check Holy Saturday tracts vs Triduum book -> Holy Sat Sanctus/Ite -> Palm Sunday procession chants
(Processionarium 1913) LAST. 4 1959 rite. 5 Mass section: site-wide 1939/1962 switch ("both, switch everywhere"), strictly
Dominican texts, Dominican Sunday numbering, consistency, Compline/Hours fixes. NB orations.js came from Divinum Officium
(maybe Roman) -> eventually verify all against Missale OP 1939.

## NOW: orations (tools/orat39) — updated 2026-11-19 11:50
Missal PDF: Joseph's Drive "Dominican Chant Propers – Source Materials/3 Missal/M39.pdf" (id 1oowwnWoHvX46HV82VFg2pN58gaEa67QW, 50 MB,
private: ask him to set "anyone with link" briefly, then curl drive.usercontent.google.com/download?id=..&export=download&confirm=t).
Pipeline: lin.py -> m39lin.txt; seg.py -> m39masses.json; match.py -> matched.json; build_or.py (15 s) -> new_or.json + report.json.
build_or.py inputs (hand-made, all in repo): ocr_sub.json (garbled -> right word), manual_acc.json (accents; overrides accdict),
overrides.json (raw Latin per KEY/kind when the text layer is broken), en_final.json (hand-checked English BODY, conclusion is
added from the Latin). Fuzzy OCR matching is OFF (it changed right words: trahant->trahat, Guala->gula). REJECT in build_or.py:
S0508b, S1119b, G481 were wrong date matches -> 103 Masses. DM English is often the WRONG prayer/saint even at ratio 1.0 -> every
English is written/checked by hand into en_final.json. Done: 27 Masses (S0118..S0711, file order). report.json r='final' marks them.
proofimg.py M39.pdf [KEYS] -> proof/KEY.png (crops of the 3 prayers; proof/ not committed) + proof/where.json (pdf pages).
TODO: fix crops S0804 or, S0512b se/pc, S0205 pc, S1015 or; proof all 103 Latin vs images; English for the other 76;
merge (J->I, site conclusions "Per eúndem ...") into data/orations.js, bump sw.js; then the other 80 Masses:
14 incomplete, 4 "ut in Comm.", ~62 not in 1939 (O26 Ordo text tools/sources/ordo_op_2026.txt; list for Joseph).

## Booklets (done, live): booklet.html?b=choir|priest|cong#<mass hash e.g. S1112&d=2026-11-12&ord=X&credo=I>
js/booklet.js own paginator (units->cols->A4 pages), booklet.css; buttons on Mass page. html lang="en" (EB Garamond locl
turns u->v for lang=la!). J() = Missal j-spelling. Art in art/ (same every day). Gloria/Sanctus/Agnus X = Vatican VIII
(gabc/opX-*, registered in app.js). Explicit Credo choice now always sung. Priest chants transcribed by OMR from his PDF
(tools/pdfomr/omr.py): gabc/op-praef-dominic-solemn, op-pater-solemn, op-pax-domini (f3) -> flag "sing through".
Polish todo: consecration words set apart in Canon (inside Qui pridie line), congregation 17pp vs his 14, page fill,
Benedicamus heading, readings use Vulgate + standard openings (first words may differ from Missal), other Prefaces only
dialogue+text (generate tone later). Reference: his 3 PDFs' text in tools/booklet/ref/, skill dominican-mass-books.

## Holy Week tooling
hw39/*.src -> hw39/build.py -> data/holyweek_text.js. Tags == H I L R T C G F: F/ P INC X; " = " English; G:/C: "id | label".
Chant OMR on scans: tools/omrtools (heads.py, zs.py, blobs.py, prep.py, rcheck.py on :8767). Clefs: zoom to decide
(mode II often f3). gabc letters are positions (d = bottom line). chant/hymn.py (stanzas to stanza-1 melody), gb2site.py.
Sources Joseph uploaded earlier (ask him to re-attach when needed): Triduum Paredes 1927, Processionarium, Hebdomada Sancta 1959,
Matutinum 1936, Antiphonarium 1933, Missale OP 1939/1933, St Dominic Missal 1959, Graduale OP 1950 Pars Prior/Posterior.
