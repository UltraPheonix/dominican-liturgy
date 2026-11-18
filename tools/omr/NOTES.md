# Reading the Antiphonarium O.P. (1933) scan

- `staves.py PAGE` finds the four-line staves of a page (0-based pdf index) and the note heads (x, staff position).
- `read33.py PAGE "text"` reads one antiphon: staff lines removed by vertical run length, heads by opening,
  stacked heads read upwards (pes), small descending heads as inclinata, clef from the two clef blobs,
  bars by vertical runs (double bar = `(::)`, full `(:)`, half `(;)`), lyric band OCR'd with tesseract
  (psm 7, char boxes) and aligned to the syllabified text, notes given to the syllable whose start precedes them.
- `batch33.py` locates each Roman-fallback antiphon in the OCR (dl/op1933/ocr/NNNN.txt, NNNN = 1-based page)
  and writes `cand33.json`; `cmp.py KEY...` stacks scan crop over the rendering for checking by eye.
- Checked readings (`ok: 1`) go into tools/gregobase/manual.json as `OP33-*` (src AOP1933) and win over the
  Roman fallback in build_chant.py.
- Typical faults to check: notes below the staff (c), a clivis read as diamonds, the clef or "Ant. VII b"
  label caught in the first syllable, a responsory or a psalm incipit chosen instead of the antiphon.
- Still Roman (not found or not yet checked): Office of the Dead, Holy Week Matins responsories, feasts newer
  than 1933, Quærite primum (b-flat pes to check), Spiritus Sanctus in te, In voce exsultationis, Cognovit.
