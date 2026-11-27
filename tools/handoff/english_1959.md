# English of the Mass prayers from the St Dominic Missal (1959), verbatim: handoff

Status (27 Nov 2026): stopped partway. **No data file and no js file has been changed.** The only new files are the
scripts and caches in `tools/orat39/dm1959/` and this note. Nothing is committed.

## Goal (owner's choice)
Use the St Dominic Missal (1959) English verbatim for every Collect, Secret, Postcommunion and Oratio super populum in
`data/orations.js`, `data/addiv.js` and `data/memoriae.js` wherever the 1959 Missal has the same Latin. This also replaces
the Divinum Officium English. Keep the DO English only where there is no DM match, and label it 'Divinum Officium'. Keep
the AI English where there is nothing else, and label it 'AI translation'. Match by the Latin. If the Latin differs
(a revision, a different name, N. in place of a name, singular/plural), do not use the 1959 English. Fix only clear OCR
damage, and never reword.

## Source
`/tmp/en_sources/dl/musicasacra/dm.pdf` (77 MB, 1341 pages; from https://media.musicasacra.com/dominican/dm.pdf).
Each page prints the English in the top half and the Latin in the bottom half, line for line in the same order.
The old parse `tools/orat39/dm_prayers.json` is unreliable: it has junk tails, cut-off Latin and margin notes inside the text.

## Pipeline so far (`tools/orat39/dm1959/`; the scripts still use /tmp/dmv paths, so adjust them)
1. `extract.py` / `cache.py`: PyMuPDF line geometry of every page -> `cache/rows.pkl.gz` (gunzip to /tmp/dmv/rows.pkl).
   Fonts in the text layer are unreliable. Line pitch is about 13 pt for English and 11.4 pt for Latin.
2. `seg.py`: splits each page into its English and Latin halves. The split is the cut, at a vertical gap of 14 pt or more,
   that best separates the English and Latin function words. It drops margin notes ("Creed, p. 621.", "Offertory Prayers, p. 623.":
   objects at x>110 that are italic or match a p.-number rubric) and finds the labels with fuzzy matching (Collect/Secret/
   Postcommunion/Prayer = Oratio/Secreta/Postcommunio/Oratio). Note: the Prayer over the People is labelled "Prayer." in the
   English and "Oratio." after "Humiliate capita vestra Deo" in the Latin.
3. `pair.py`: on each page, aligns the sequence of English labels with the sequence of Latin labels, then pairs the leftovers
   on the same or the next page. Result: 1336 Latin-English pairs (or 542, se 412, pc 379) -> `cache/pairs.pkl.gz`.
4. `match.py` + `lex.py` + `cmp.py`: finds the DM candidate for each prayer on the site (8-gram index), cuts the conclusion,
   and compares word by word. OCR confusions (rn/m, li/u, i/l, c/e, split words, garbage words not in a Latin lexicon
   built from bible/la and data/office) count as equal. Any other difference counts as a real difference.
   First count on orations.js (1452 parts): 935 match, 387 with real differences, 130 with no DM candidate.
   Many of the 387 are OCR damage in the PDF text layer ("ang lorum", "queswnui", "nec"/"ne"). The others are real:
   N. for the saint's name, other names, other words ("propensius"/"propitius", "jugiter" added).
5. `tess.py` (started, then stopped): Tesseract (eng, psm 6, 300 dpi) gives **much cleaner** text than the PDF layer
   (see page 29: "prayers", "O God", "John" all correct). Plan: use the Tesseract text for both the English and the
   Latin of each paired prayer, then match again. `need.txt` lists the 926 pages that hold candidate prayers. 26 pages are done
   (`cache/tess_tsv.tgz`). The machine is shared and slow: about 10 s per page with 2 processes and OMP_THREAD_LIMIT=1.
   It is better to OCR only the cropped rows of each paired prayer: the y-ranges are known from rows.pkl, and crops are about 10x faster.

## What is left
- Run the OCR: crops (or the pages in need.txt), with tesseract TSV. Map the words back to page coordinates. Keep only the words
  inside the kept objects (this drops the margin notes). Rebuild the pairs from the Tesseract text.
- English cleanup, OCR only: join hyphenated line ends (keep the hyphen when both parts are words: "Only-begotten");
  "0 Lord" -> "O Lord"; "Y ou" -> "You"; remove · ~ | _; cut after the conclusion ("through our Lord." / "who live and reign." ...)
  and drop the "Amen." that follows.
- Write `tools/orat39/dm_verbatim.py`. Run it after tools/requiem/build.py, tools/orat39/conclusions.py and tools/g28/apply.py,
  and only touch the English. It should:
  - orations.js / memoriae.js: [la, en] with the DM conclusion as printed, plus per Mass `en_src: {or:'dm'|'do'|'ai', ...}`;
    do = src is a DO path (and, for memoriae, English equal to a DO oration's original English); otherwise ai.
  - addiv.js: split en (body) / ec (the DM conclusion, capitalised) and set s = 'dm' | 'ai' (the old s:'dm' was wrong for 17 of 18).
  - In src strings, replace "English after the St Dominic Missal (1959), checked against the Latin" with an honest note.
  - Idempotent: keep an existing en_src when there is no match.
- js/app.js, small changes:
  - drawOratio: a tr-src span from `ORATIONS[state.key].en_src[it.k]` in its three en-text places.
  - drawMore: the label for 'dm' becomes 'St Dominic Missal (1959)'; add 'do' -> 'Divinum Officium'.
  - **Also needed** in prayerOf: `p.s = (x.en_src||{})[k]` for 'm:' and `r.s = (Mm.en_src||{})[k]` for 'x:'. splitConcl sets s:'or',
    so the commemorations show no label otherwise. This one change falls outside drawOratio/drawMore.
- Check that the DM conclusions still match CONCL_EN in app.js ("through ...", "who live(s) ..."), since splitConcl uses it.
- Report the counts: verbatim / no match / Latin mismatch (the N.-only cases separately).
- Test: `python3 -m http.server 8793`, then Playwright with /usr/bin/google-chrome on #S0307&d=2027-03-07, #Adv1&d=2026-11-29 and
  #C114s&d=2026-11-30. Then `timeout 590 python3 tools/check/mass_sweep.py` must report "flagged 0".

## To resume
```
mkdir -p /tmp/dmv && cd /tmp/dmv && cp /home/claude/dominican-liturgy/tools/orat39/dm1959/*.py . \
 && cp /home/claude/dominican-liturgy/tools/orat39/dm1959/dmv_load.py /tmp/ \
 && gunzip -c /home/claude/dominican-liturgy/tools/orat39/dm1959/cache/rows.pkl.gz > rows.pkl \
 && gunzip -c /home/claude/dominican-liturgy/tools/orat39/dm1959/cache/pairs.pkl.gz > pairs.pkl \
 && tar xzf /home/claude/dominican-liturgy/tools/orat39/dm1959/cache/tess_tsv.tgz \
 && python3 lex.py && python3 seg.py && python3 pair.py
OMP_THREAD_LIMIT=1 python3 tess.py 0 2 & OMP_THREAD_LIMIT=1 python3 tess.py 1 2 &   # or write the crop version
```
Note: other sessions commit to this repo while this work goes on, so read each data file again just before writing it.
