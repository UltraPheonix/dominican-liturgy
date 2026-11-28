# Auditor brief: Phase 1 step 1, text audit of the Masses (coordinator, 27 Nov 2026 21:45)

You are auditor <G> (one of A1-A5). Your Masses are the list `groups.json["<G>"]`, in that order.
Resume where your report tools/audit/<G>.md says you stopped. Do not redo Masses already marked FIXED/OK on the scan.

## 0. Read first (mandatory, before touching any Mass)
1. tools/handoff/README.md ("THE ORDER OF WORK", "RUBRICS FIRST", "Standing rules") and tools/handoff/RULINGS.md.
2. **The rubrics, in full:** the *Rubricae generales Missarum* of the Missale O.P. 1939
   (text layer tools/orat39/m39lin.txt, `@@PAGE 25`-`@@PAGE 33`; scan /home/claude/dl/missal/M39.pdf, pdf page = @@PAGE+1).
   Read in particular the titles on the Orations and their conclusions, and on the Epistle, Gradual, Alleluia/Tract,
   Sequence and Gospel. Also read the rubrics printed inside each Mass you audit.
3. Your own report and fixes file, and your scripts in tools/audit/scripts/<G>/ (copy them to /tmp/<G> if their paths are hard-coded).

**Every decision cites its rubric or Missal page.** In each fix entry put the Missal page in "src". Where a fix rests on
a rubric (e.g. the type of conclusion, whether a verse is said), quote the rubric's words and page in "why".
**Where the rubrics or the book are silent or unclear, do not guess: list it under "QUESTIONS FOR JOSEPH" in your report.**

## 1. What to check, for every Mass, against the M39 scan (the scan wins over the text layer, which is often garbled)
- **Title:** only wrong words; keep the calendar style.
- **Orations** (or/se/pc and any extra prayers): word by word, with the Missal's punctuation (`;` = flexa, `:` = elevatio,
  Proc. 1913 p. 405, so punctuation matters for the chant). Keep the expanded conclusions, but check their type against the
  Rubricae generales. Fold i/j when comparing (the i→j conversion is a separate script later; do not do it now).
- **Readings:** full text (look for cuts at page breaks and missing endings like "In Christo Jesu Dómino nostro"),
  punctuation and the reference.
- **Chants:** that each chant id is the right chant for this Mass, as the Missal prints its incipit and verse.
  Do not read new chant here. If an id is wrong, propose the right existing id (gabc/ or tools/gregobase/gb.sqlite, Dominican
  sources 11, 12, 13, 14, 20, 21, 35, 36 only) with its book page, or mark "needs reading from G28" in the report.
- **English:** only that it matches its Latin (a missing clause, a wrong reference). Do not restyle it.

## 2. Output (the only files you may write)
- tools/audit/fixes/<G>.json: entries in the format of the apply_fixes.py docstring, each with "src" (page) and "why".
  Add only differences you have seen on the scan crop.
- tools/audit/<G>.md: one line per Mass (KEY | Missal page | result), a "Where I stopped" line at the top, and
  a "QUESTIONS FOR JOSEPH" section.
- tools/audit/scripts/<G>/ for your scripts; scratch in /tmp/<G>/.
- **Never** edit data/*, js/*, gabc/* or any other file. Never run apply_fixes.py without --dry (the coordinator applies).
  Never commit or push. Run `python3 tools/audit/apply_fixes.py --dry` before you finish: 0 CONFLICT / MISSING.
- **Save your report and fixes after every Mass**, so nothing is lost if you are stopped.

## 3. Rules (Joseph)
- Dominican books only (Missale O.P. 1939/1933, Graduale O.P. 1928/1950, Processionarium 1913, Ordo 1944). Never Roman books,
  never Divinum Officium as an authority.
- Never infer chant. Never invent a reading or a prayer.
- Be terse.

## 4. When you finish (or after about 40 Masses, whichever is first)
Reply with: Masses done (keys), number of fix entries added, open items, and the QUESTIONS FOR JOSEPH, each with the rubric/page it concerns.

## 5. Lessons from 27 Nov (coordinator, 28 Nov 07:20). These override anything above.
- **Never edit an entry that may already be applied.** To correct yourself, add a NEW entry whose "old" is the current data.
- **Re-read every "new" value for OCR junk** (¿, "., ", stray running heads, split words) before saving. Junk went live once.
- **Conclusions are normalised centrally** by canon() in apply_fixes.py ("Iesum Christum Fílium tuum; qui tecum … cum Deo Patre;
  in unitáte Spíritus Sancti Deus: per ómnia"). Write no conclusion-pointing entries. The mark BEFORE the conclusion
  ("mente : Per Dóminum") is yours to check.
- **English:** never from memory. Douay verbatim from bible/en/<Book>.txt (tab-separated chapter, verse, text). The St Dominic
  Missal 1959 for prayers: tools/orat39/dm_prayers.json and tools/orat39/dm1959/ (check there BEFORE using AI). AI translation,
  labelled (en_src "ai"), only where no 1959 text exists, or where the Missal's Latin departs from the Vulgate.
  Do not add Gospel incipits ("Jesus said to his disciples"): the coordinator does that by script.
- **Accented capitals:** the Missal prints none ("Angelus", "Anima"); write capitals without accents. The coordinator normalises the rest.
- "op": "add" (old: null) adds missing readings/keys; copy the shape of existing entries exactly.
- Ember days: collects between the lessons go in ORATIONS[key].inter (see A1.md / A2.md for the shape).
- Joseph's goal: every prayer, reading and proper the Missal prints must be on the site, word and mark as printed.
