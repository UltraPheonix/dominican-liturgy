# Triduum Office (Triduum O.P. 1927) -> gabc/op-ten-<day>-<code>.gabc + tools/hw39/Quad6<day>_ten.src
Day h = Maundy Thursday: Matins (Tenebrae) pdf pp. 2R-17R, Lauds 17R-24L.
- Staves: /home/claude/build/tri_staves.pkl (tri_read.py PG0 PG1); pieces.py = (code, name, first staff, last staff, text).
- build.py (OMR + fix.json) -> res.pkl; assemble_ten.py h -> final_h.json (GB merge: Lamentations = Off. Hebd. Sanctae O.P. 1965,
  GB 8261-3, same tone as 1927 EXCEPT the refrain Jerusalem, Jerusalem (book notes kept); Lauds antiphons = Antiph. O.P. 1933,
  GB 7158 5691 5695 4698 5605 6734, identical to 1927). Kyrie/Christe written by hand (k01, k07).
- writeg_ten.py h -> gabc; gen_h.py -> src (psalms la/en from data/office via psalms.py; lessons 4-9 typed from the 1927 page,
  English mine in lessons_h.json; responsories = op-abl-r01..r09, the same chant as the Tenebrae printing).
- Matins antiphons t01-t09 + versicles proofed on the scan (full.py/zz.py). Benedictus is notated in full in the book: shown as text.
- Psalms are sung: gen_ps.js sets each psalm to the Dominican tone with js/psalm.js (same engine as the Office tab). Tone + ending
  per psalm (gen_h.py TONE) chosen by matching the book's notated first verse (pieces p68..p53, OMR) against every tone/ending
  (/tmp/match.js logic): N1 VIII c; Ps71 VII d, Ps72 VIII c, Ps73 I a; Ps74 VII d, Ps75 VIII c, Ps76 VII a; Lauds 50 VIII G,
  89 II D, 62 VIII G, Cant. Moysis IV A, 148 II D, Benedictus I g solemn (every verse intoned). Ps 50 after the Kyrie is said
  (mediocri voce) -> text only. Known small difference: the book's mediant in Ps 71 v.1 ("regi da") differs from the 1965 rules.
