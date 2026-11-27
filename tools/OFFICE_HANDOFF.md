# OFFICE HANDOFF — the Office chat is closed; one chat now owns Mass + Office (2026-11-27)

Read this file first, then tools/HANDOFF.md (running log; Office sections from "B5 IN PROGRESS" on), tools/TODO.md,
tools/b09/fix/REPORTS.md, tools/b09/EYEPASS.md, tools/ENGINE.md.

## 0. Where everything is
- LIVE (main): 1954 Office; 1909 Office behind the switch (localStorage officeRite=1909) with saints' prayers and lessons fixed
  (sw v97, v99). Nothing newer of the 1909 work is live.
- BRANCH `commons1909-v2` on origin = ALL later 1909 work, with origin/main (2026-11-27 17:10) already merged in, so it
  fast-forwards/merges cleanly: `git fetch origin && git merge origin/commons1909-v2`. NOT yet published — see §3 step 1.
- From now on the old ownership rule is void: this chat owns data/office*, tools/b09/, js/office.js, js/tones.js,
  data/chant/office.json, office.html as well.

## 1. Goal and Joseph's standing rules
- GOAL: the user can chant and say the entire 1909 Office and the 1953/54 Office, incl. Tenebrae and special services.
- Quality over speed. Traditional pre-1955 Dominican rite only; Dominican sources only; no inferred chant (printed melodies only).
- 1909 texts: the PAGE IMAGE is the only authority. Eye-checked text follows the page as printed (æ unaccented, no accent on
  y or on capital initials). References (Divinum Officium, Vulgate) lend only spelling/accents to machine text — never wording.
- VERIFIED-ONLY: for Sanctorale feasts the build shows only eye-verified text (fix files). Unverified machine text is never
  shown (falls back to the Common or "in preparation"; a feast's own unverified lesson is never replaced by the Common's).
- Publish checked days as they are done. Status message to Joseph after each day checked / each substep. Terse; he is on mobile.
- No subagents unless Joseph asks.
- Every push: bump sw.js VERSION, headless Chrome test with no console errors, commit as
  UltraPheonix <UltraPheonix@users.noreply.github.com>, push with tools/push.sh.

## 2. The 1909 pipeline (tools/b09/)
- Sources: Breviarium S.O.P. 1909 (Cormier), 2 vols. Scans = CMAA "Breviarium-1909-1/2-optimized.pdf" (same pagination as
  Joseph's text PDFs; vol. 1 = 1577 pdf pages). They lived at /tmp/b09/b1.pdf, b2.pdf — NOT in the repo (320 MB each):
  fetch again from the CMAA Dominican page or ask Joseph to attach. Vol. 1 Sanctorale: book page = pdf page − 86.
  Render a page: `pdftoppm -f N -l N -r 110 -gray -png /tmp/b09/b1.pdf out` (110–120 dpi is readable).
  Sanctorale pdf ranges: v1 769–1577 (11-29…06-15), v2 477–1369 (04-13…12-02). Rubricae generales: v1 pdf 40–70.
- Text layers: text/v1,v2.txt.gz (old, poor); ocr/v1,v2.txt.gz (tesseract lat-best re-OCR of the Sanctorale only; restore to
  /tmp/b09/ocr with the command at the foot of reocr.sh).
- ref/latdict2.json.gz, ref/latcnt3.json.gz = caches for latdict.py / latcount.py: gunzip to /tmp/b09/latdict2.json,
  /tmp/b09/latcnt3.json (else they rebuild from a Divinum Officium clone at /home/claude/divinumofficium/divinum-officium).
- calendar1909.txt (eye-transcribed calendar; use this, NOT calendar1909.json) → proper.py (`python3 proper.py v1; … v2`,
  ~5 min each) → propers1909.json (241 feasts, machine reading, never shown) → show.py 'MM-DD' --full (machine text + pages).
- Eye-verified fix files (key = calendar title): propers_fix.json, fix/a00.json (main session), fix/b00…b05.json (helpers).
  Keys are listed in EYEPASS.md and in HANDOFF.md ("2026-11-27 morning"). 60 feasts done, Nov 27 – Feb 23 with gaps.
- build.py → data/office1909/YYYY/MM-DD.json + common.json (426 days, 2026-11 … 2027-12). `cd tools/b09 && python3 build.py`.
- scratch/: chk.py (are each fix entry's pieces in the built day and the eve's Vespers?), audit.py, aud2-4.py (run-ons, "N.",
  empties), t1909.py (playwright: http.server 8768, officeRite=1909, office.html#Hour&d=DATE), batches.json (28 helper
  batches, 0–5 done), pshow.py, poll.py. Paths inside them point at /tmp — adjust.

## 3. TO DO for the 1909 Office, in order
1. FIRST MERGE TO LIVE (Joseph has said: publish). Normalise my own entries (propers_fix.json, fix/a00.json) to page spelling
   (ǽ→æ; no accents on capital initials where the page has none); rebuild; scratch/chk.py + audits; browser test on sample
   days of every month, both rites; merge the branch to main; tools/push.sh.
2. SAINTS — finish the eye check.
   - Gaps in Nov 27–Feb 23: Desponsatio B.M.V. (02-11, full, from v1 pdf 983); Septem Fundatores (02-17, full + T.P. form,
     pdf 1002–1011); B. Aimo (02-21, pdf 1015–1016); S. Matthias (02-24, full, from pdf 1025); B. Zdislava (11-28, v2 ~pdf 1100);
     12-31…01-14 (Sylvester, octave days of Stephen/John/Innocents, etc.); octave of St Raymond and other infra-octave days;
     St Andrew (lessons, prayer, I Vespers), St Nicholas (lessons), St Francis Xavier (homily lessons).
   - ~185 feasts 02-25 → 11-26 (22 batches in scratch/batches.json; ~60 with a full Office). Unsplit stretches: after 03-25,
     v1 after 06-11, v2 after 12-02. ~15 feasts where only a prayer was found.
   - Sample helper files b01, b03, b04, b05 against the page (b00 Barbara and b02 Agnes sampled: matched).
3. SAINTS — transcribed but not placed (in each entry's `note`): Little Hours chapters/short responsories/versicles; proper
   Compline antiphons (Conception, Loreto, Purification); proper blessings; proper Lauds chapters/versicles; hymns only noted
   (Gundisalvus, Catherine de' Ricci, Raymond, Peter's Chair); extra strophes in the Conception octave; prose Inviolata at the
   Purification; T.P. second forms; printed commemorations (ant., V., prayer); rubrics that change an Office (I-nocturn
   lessons from the Common only after Ash Wednesday; no Te Deum on Holy Innocents unless Sunday).
4. COMMONS: eye check of every Common (built from the old layer, machine-corrected only); Common of several saints for the
   two days still showing "N." (06-09, 06-15); 24 doubtful readings; Matins lessons and homilies; English for the new lessons.
5. PROPER OF THE SEASON: re-OCR the Temporale pages; re-check the LIVE Advent Matins lessons/responsories (the old method
   sometimes substituted Roman wording); then eye pass: Advent (O antiphons, Christmas Vigil) → Christmas–Epiphany → after
   Epiphany → Septuagesima–Passiontide → Holy Week and Triduum with Tenebrae, line by line → Easter–Rogations →
   Ascension–Corpus Christi → Sundays after Trinity with summer/autumn lessons → Ember days and vigils.
6. PSALTER AND ORDINARY: eye check of the weekly psalter (never checked); preces; suffrages; Prime's chapter office
   (Martyrology, Pretiosa); Marian antiphons by season.
7. OTHER OFFICES: Little Office B.V.M.; Saturday Office B.V.M.; Office of the Dead; St Dominic and octave; penitential and
   gradual psalms, litanies, blessings, special services.
8. RANKING ENGINE (tools/ENGINE.md; the Office chat had taken steps 4–5): read the 1909 Rubricae generales (v1 pdf 40–70) and
   write each rule with its page; data/kalendar09.js from calendar1909.txt; '1909' rule set in js/rank.js; transfers,
   octaves, vigils, commemorations; Vespers concurrence (both rule sets); the 4 additive interface fields agreed in the LOG
   (vespers {psalms, fromChapter, commems}; celebration.lessons 3|9; paschal flag; commemoration `at` Hours); wire into
   build.py / office.js; test whole years. The '1939' precedence is still blocked on a 1930–1952 Dominican Breviary or Ordo
   from Joseph. Until the engine exists these CHECKED texts cannot show: Christmas-octave feasts, Holy Name, Gundisalvus,
   Simplex feasts (Blaise, Martina), octave days, Vespers shared between two feasts.
9. CLEAN-UP: drop each "in preparation" note as its part lands; automatic full-year check (nothing empty, no "N.", no
   unverified text shown, uniform spelling); a read-through of sample days by Joseph.
10. CHANT: match antiphons/responsories/hymns to the Jandel 1862 Antiphonary and the 1933 books (printed melodies only);
    decode the Nocturnale for Matins; tones for psalms, lessons, prayers, versicles, preces.

## 4. Known traps
- Both text layers can drop the same word; only the eye pass settles a text.
- The machine reading misfiles Offices (Scholastica←Desponsatio, Gregory X←Seven Founders, Blaise←Corsini): never trust
  propers1909.json placement without the page.
- A printed hymn doxology must not be swapped by the 'bvm' rule (FIXHY skip in build.py).
- If a build is interrupted, `git checkout data/office1909` before anything else.
- pip install of pycollatinus is blocked by the sandbox; do not work around it.
