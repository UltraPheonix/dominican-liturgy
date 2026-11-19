# Triduum Office (Triduum O.P. 1927) -> gabc/op-ten-<day>-<code>.gabc + tools/hw39/Quad6<day>_ten.src
Day h = Maundy Thursday: Matins (Tenebrae) pdf pp. 2R-17R, Lauds 17R-24L.
- Staves: /home/claude/build/tri_staves.pkl (tri_read.py PG0 PG1); pieces.py = (code, name, first staff, last staff, text).
- build.py (OMR + fix.json) -> res.pkl; assemble_ten.py h -> final_h.json (GB merge: Lamentations = Off. Hebd. Sanctae O.P. 1965,
  GB 8261-3, same tone as 1927 EXCEPT the refrain Jerusalem, Jerusalem (book notes kept); Lauds antiphons = Antiph. O.P. 1933,
  GB 7158 5691 5695 4698 5605 6734, identical to 1927). Kyrie/Christe written by hand (k01, k07).
- writeg_ten.py h -> gabc; gen_h.py -> src (psalms la/en from data/office via psalms.py; lessons 4-9 typed from the 1927 page,
  English mine in lessons_h.json; responsories = op-abl-r01..r09, the same chant as the Tenebrae printing).
- Matins antiphons t01-t09 + versicles proofed on the scan (full.py/zz.py). Benedictus is notated in full in the book: shown as text.
