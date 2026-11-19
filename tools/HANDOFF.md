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

## NOW: orations (tools/orat39)
lin.py: Missale OP 1939.pdf -> m39lin.txt (in repo, clean text layer). seg.py -> m39masses.json (month 0-based, day, title,
pr{or,se,pc}, comm=Common page). match.py -> matched.json (124/183). accent.py (accdict.json in repo; from DO+site texts).
build_or.py -> new_or.json + report.json: accented Latin (Missal j-spelling kept, no accent on initial capital), full conclusion,
English from St Dominic Missal 1959 (dm_prayers.json) if same prayer (ratio>=.8), You-style conclusions.
Status: 106 complete-ish (new_or_draft.json is BEFORE last fixes). ocr_fix/word-join/running-head removal just added to
build_or.py, UNTESTED (was slow: get_close_matches over 75k keys -> restrict/cache). Then: manual_acc.json for rare names/words
(see report.json unk); ~111 prayers need English (translate faithfully, You-style like DM); 14 incomplete (read pages);
4 "ut in Comm. pag N*" (take Common prayers, insert saint's name, decline it); 59 not in 1939 (post-1939 Blesseds etc:
ask Joseph / current Dominican Proper / O26 Ordo text tools/sources/ordo_op_2026.txt). Proof each vs Missal page image,
then merge into data/orations.js (format {"KEY":{"src":..,"or":[la,en],"se":[..],"pc":[..]}}; site Latin uses I not J,
conclusions "Per Dóminum nostrum Iesum Christum, Fílium tuum: qui tecum vivit et regnat in unitáte Spíritus Sancti Deus,
per ómnia sǽcula sæculórum."). S1112 already done by hand. Missal is DIFFERENT from DM 1959 sometimes (S1112 Secret).

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
