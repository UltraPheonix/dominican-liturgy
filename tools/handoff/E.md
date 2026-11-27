# Lead E (Texts): paused 27 Nov 2026, 17:07, at Joseph's request

Goal B, the cut readings, belongs to worker W-E3 (tools/m33/**, data/readings33.js); see W-E3.md. This note covers
Goal A only: the 1959 St Dominic Missal English, verbatim. Background: english_1959.md.

## State
- **No data file has been written.** data/orations.js, data/addiv.js and data/memoriae.js are untouched by Lead E.
  addiv.js shows as modified in git, but another job made that change.
- **js/app.js, prayerOf only:** `p.s = (x.en_src || {})[k];` on the 'm:' line and `r.s = (Mm.en_src || {})[k];` on the 'x:'
  line. This is harmless now. Before, splitConcl set s:'or', which shows no label; with no en_src, s is undefined, which also
  shows no label. Once the data carries en_src, commemorations show their source.
- **OCR:** 584 of about 2000 needed crops are done (Tesseract eng, psm 6, 300 dpi). The run was stopped because the machine
  load was 40-55 on 2 cores.
- **Partial result:** with OCR for 232 of 1336 DM pairs, 241 site prayers match the 1959 Latin exactly:
  - orations: 232
  - memoriae: 6
  - addiv: 3

  The table is in `tools/orat39/dm1959/cache/dm_en_partial.json`. Key: `file|id|field`. Fields: s, en, p (DM pdf page),
  i (pair index), flags. 47 of the matches are flagged for review:
  - `no-concl`: the cleaner found no conclusion with a full stop.
  - `concl-split`: js splitConcl would cut the English somewhere other than at its printed conclusion.
  - `alts:N`: the DM prints the same Latin with N different English texts.
  - `unk:`: a word not in the lexicon.
  - `len`: the English length is implausible against the Latin.

## Files (all in tools/orat39/)
- `dm1959/dmpaths.py`: paths. The scripts no longer use /tmp/dmv. Scratch goes in `dm1959/work/`, which has its own .gitignore `*`.
  The PDF is `/tmp/en_sources/dl/musicasacra/dm.pdf` (override with the DM_PDF environment variable).
- `dm1959/seg.py`, `dm1959/pair.py`: now keep line geometry (`erows`/`lrows`) and line text (`elines`/`llines`) for each pair.
- `dm1959/ocr.py PART N [jobs.txt]`: Tesseract on the cropped rows of each pair half, cut at its conclusion (at most 14 rows).
  Output: `work/crops/<i>_<e|l>_<k>.tsv` plus a .json with the rectangle and the kept boxes.
- `dm1959/readocr.py`: reads the crops back. It keeps only the words inside the kept text boxes, matched by the line centre,
  so margin notes ("Creed, p. 621.") drop out.
- `dm1959/need.py`: writes `work/jobs.txt`, the halves still to OCR:
  - English: every DM pair near a site prayer (1235).
  - Latin: only where the text layer is not clean (677).
- `dm1959/dmrec.py`: builds `work/dmrec.pkl`, the cleaned English.
  - Strips the label and joins hyphenated words using a lexicon (the site's English, the Douay text and the DM text layer).
  - Applies noise rules for scan specks ("we.receive", "-deliverance", "with. fitting", "OQ").
  - Merges with the PDF text layer as a second witness: an unknown OCR word is replaced by the layer's word when that is a known word.
  - Cuts after the conclusion ("through our Lord." / "who live and reign.").
- `dm1959/cmp.py`: compares the Latin word by word. OCR confusions are tolerated, and spelling variants (intelleg/intellig,
  mihi/michi, nihil/nichil, cotidie, genetrix) count as equal.
- `dm_verbatim.py`:
  - `--table`: matches every site prayer and writes `work/res.pkl`.
  - With no option: classifies the matches and writes `dm1959/dm_en.json`.
  - `--write`: writes the 3 data files. orations/memoriae get `en_src {or:'dm'|'do'|'ai'}`. addiv gets en/ec split and `s`.
    The src notes become honest.
  - Run it only after tools/requiem/build.py, conclusions.py, g28/apply.py, addiv/build.py and memoriae_build.py, because they
    rewrite these files.
- Cache, so a reset machine can resume:
  - `dm1959/cache/rows.pkl.gz`
  - `dm1959/cache/pairs.pkl.gz` (new, with geometry)
  - `dm1959/cache/crops.tgz` (the 584 crops)
  - `dm1959/cache/dm_en_partial.json`

## Findings
- Tesseract English is much cleaner than the PDF layer, and wins on punctuation. Checked on the scan: pair 7 has "mystery, and"
  where the layer reads "mystery;".
- Some crops make Tesseract psm 6 fail badly, although the image is clean. Pair 62 (the Postcommunion "Increase within us") is
  one: psm 11 reads it perfectly.
  - **TODO:** find these crops (low letter agreement between Tesseract and the text layer, ratio < 0.93) and OCR them again
    with `--psm 11`, sorting the words by line y.
- The DM has misprints: "spirtual" (pair 187), "sactifices" (pair 221). Joseph has to decide whether to keep them verbatim
  or correct them. The default is verbatim.
- **Bug to fix:** `is_do()` in dm_verbatim.py finds only 36 'do' prayers, but 163 Masses have a DO src. Most likely cause:
  operator precedence in the final `any(...)` condition. Fix it, then check the result on a DO Mass (for example Adv1 se/pc
  against DO Tempora/Adv1-0.txt).
- The kinds of 'differs' seen so far (do not use the DM English for any of these):
  - N. for the name (C7s).
  - Real one-word variants: Quad1h se propensius/propitius; Quad5s se consortes/participes; Pent13 pc caelestibus/salutaribus;
    Quad6t pc sempiterna/aeterna.
  - Different prayers altogether (Pasc0 se/pc).
  - Single-letter cases need a look at the scan before deciding: tuae/tua (Nat1, Jan5a), Iesum/Iesus (Dec24), populus/populis
    (Quad5t sp), appetimus/appetamus (Epi6).
- **Main-prayer labels:** the brief allowed only prayerOf, so these need the coordinator or another lead:
  - drawOratio needs a tr-src span from `ORATIONS[state.key].en_src[it.k]`.
  - drawMore's 'dm' text should be 'St Dominic Missal (1959)', and 'do' → 'Divinum Officium' should be added.

## Resume
```
cd /home/claude/dominican-liturgy/tools/orat39/dm1959
mkdir -p work && printf '*\n' > work/.gitignore
gunzip -c cache/rows.pkl.gz > work/rows.pkl; gunzip -c cache/pairs.pkl.gz > work/pairs.pkl; tar xzf cache/crops.tgz -C work
python3 lex.py                     # work/lex.pkl (Latin lexicon for cmp.py)
python3 need.py                    # work/jobs.txt (skips crops already done); about 1500 jobs, roughly 0.5-1 s each on an idle machine
cd /tmp && for k in 0 1; do OMP_THREAD_LIMIT=1 nohup python3 /home/claude/dominican-liturgy/tools/orat39/dm1959/ocr.py $k 2 /home/claude/dominican-liturgy/tools/orat39/dm1959/work/jobs.txt & done
# when done: TODO psm-11 retry pass (above); then
cd /home/claude/dominican-liturgy/tools/orat39 && python3 dm1959/dmrec.py && python3 dm_verbatim.py --table
# review the flagged matches and the 'differs' cases against the scan (render: fitz page.get_pixmap(dpi=150, clip=rect from crops/*.json))
python3 dm_verbatim.py --write
# test: playwright /usr/bin/google-chrome on #S0307&d=2027-03-07, #Adv1&d=2026-11-29, #C114s&d=2026-11-30 (port 8765)
# then on port 8768: timeout 590 python3 tools/check/mass_sweep.py  -> must print "cases 224 flagged 0"
```
