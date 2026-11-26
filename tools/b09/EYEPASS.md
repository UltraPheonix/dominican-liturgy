# Eye pass of the 1909 Dominican Breviary Sanctorale — instructions for a helper

Goal: for each feast in your batch, make the texts of its proper Office exactly what the PRINTED PAGE says. The page image is the
only authority. Never write a word from memory, from a reference text (Roman Breviary, Divinum Officium) or by guessing: if a word
cannot be read on the image, say so (see `not_ok`). Dominican texts often differ from the Roman ones.

## Per feast
1. `cd /home/claude/dominican-liturgy/tools/b09 && python3 show.py 'MM-DD' --full`
   shows the machine reading (two OCRs merged): pieces by section, lessons (L4…), responsories (R4…), `Q` = doubtful words,
   `pages` = pdf pages of the volume (`v1` → /tmp/b09/b1.pdf, `v2` → /tmp/b09/b2.pdf; the v1.pdf/v2.pdf symlinks are broken) where the feast was found. The feast may start on the page before and end on
   the page after: read those too if the Office is cut.
2. Render and read the pages (120 dpi is readable; go to 160 for a doubtful word):
   `pdftoppm -f N -l N -r 120 -gray -png /tmp/b09/b1.pdf /tmp/b09/eye/<yourfile>-N` then Read the PNG.
3. Compare EVERY piece with the page: the prayer (Oratio), antiphons, versicles, responsories (with their printed repeats after
   the verse and after Glória), lessons word by word. Both OCRs can drop the same word (e.g. "quem vocávit" read as "vocávit");
   lessons may be interleaved across a column or page break.
4. Write the result for the feast into YOUR fix file (JSON object, key = the feast title exactly as after the `|` in show.py's
   header, e.g. "S. Bárbaræ Virg. et Mart."). Use these keys (all optional; give what the page prints for THIS feast only —
   what the page says to take "de Communi" is not written):
   - "pages": "v1 pdf 782 (book p. 696)"
   - "oratio": the prayer, ending with the conclusion as printed expanded only to "Per Dóminum." / "Per eúndem." / "Qui vivis." / "Qui tecum."
   - "v1.ant" (one antiphon super psalmos) or "v1.ants" [5]; "v1.cap" [ref, text]; "v1.resp" [a, b, verse, repeat after verse, repeat after Glória]; "v1.magn"
   - "mat.invit" (with " * " where printed); "mat.nants" [[3],[3],[3]]; "mat.nvr" [[V,R],[V,R],[V,R]]
   - "resp": {"1": [a, b, [verse], gloria], …} — a = text before the *, b = text after it; gloria = false (no Glória),
     true (Glória, repeat = first words of b), or [repeat after the verse, repeat after the Glória or false] when the printed
     repeats ("— Xxx. Glória. Yyy.") are not simply the first three words of b.
   - "al" [V, R] = the versicle "Ante Laudes"; "laud.ant" [5]; "laud.bened"; "v2.ant"; "v2.magn"
   - "lessons": {"4": "full Latin text of lesson iv", …} — retype or paste the machine text and correct it; no heading, no
     "Tu autem". For a homily lesson (vii) give only the homily text; put the Gospel incipit in "gospel7": "In illo témpore: … Et réliqua."
     and the heading in "homily7": "Homilía sancti Gregórii Papæ."
   - cheaper alternative for lessons that are nearly right: "sub": [[wrong, right], …] exact-string replacements applied to the
     machine reading of the whole feast, plus "ok": true ONLY if after those replacements every machine piece of the feast
     equals the page. "not_ok": ["lectio 8", "resp 3", "mat.nants", …] lists pieces you could not verify (they stay unused).
   - "note": anything odd (feast shares a page with another, rubric that changes the Office, Office not found on the pages, …).
5. Spelling as printed: æ œ ligatures; accents as printed (ǽ for accented æ); j and v as printed; capitals as printed.
   Drop-capitals and small-capital first words are written normally ("Deus", "Francíscus").

## Rules
- Write ONLY your own fix file `tools/b09/fix/<name>.json` (valid JSON; save after every feast so nothing is lost).
- Do not edit any other file, do not run build.py or proper.py, do not use git, do not install anything.
- Examples of finished entries: `tools/b09/propers_fix.json` (S. Andréæ Apóstoli, S. Nicolái Ep. et Conf. = full Offices;
  B. Joánnis a Vercéllis = "sub" + "ok"; S. Francísci Xavérii = "lessons").
- If you run short of room, stop cleanly: finish the feast in hand, save, and report which feasts are done and which are not.
- Final report (short): feasts done, feasts not done, anything you could not read, anything odd.
