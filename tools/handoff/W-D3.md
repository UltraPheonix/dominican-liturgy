# W-D3: St Albert the Great (15 Nov, S1115). Stopped 27 Nov on the coordinator's order

## Source
- The S.R.C. supplement leaf bound into the G28 scan, dated 9 June 1933: /home/claude/dl/grad351/x/graduale_juxta_ritum_1928_paredes.djvu
  - Leaf p. 1 is djvu 314 (right half). It holds the Responsorium.
  - Leaf p. 2 is djvu 315 (left half). It holds the Alleluia.
- The leaf's heading: "Missa In medio, in Festo unius Doctoris, pag. 35*, praeter sequentia".
- Staff line y-values (full-resolution pnm from `ddjvu -page=N`):
  - 314R: 1376, 1706, 2062, 2394, 2724, 3056, read at x 3300.
  - 315L: 558, 906, 1253, read at x 1400.
- The Graduale O.P. 1950 prints the same two chants in its body, pp. 616-617 (OCR in scratch/g50all.txt, line ~10023). They are not in the G50 GABC set.

## Done (both files compile with gregorio)
- **tools/g28/albertus_gr.gabc:** Resp. "Ecce sacerdos magnus ... V. Inventus est justus ... reconciliatio", mode V, complete.
  - The respond is in c4. The verse changes to c3 (`(::c3)`).
- **tools/g28/albertus_al.gabc:** "Alleluia. V. Vere magnus est in caelis Albertus ille fidelis qui fecit quod decuit", mode VIII, c4, complete.
- **Passes:**
  - First pass: read by eye at 1.25-3x zoom.
  - Second pass: only an automatic note-head cross-check with tools/g28/blobs.py, which agrees.
  - **Still to do:** a full visual second pass by the D-checker.
- **Bar rule used:**
  - (;) for bars of 1.3-1.7 staff gaps.
  - (:) for bars of about 1.8-2.1 gaps and for full-height bars.
  - (::) for double bars. This includes the double bars inside the verse where the choir comes in.
- **Points for the checker:**
  1. The custos at the end of Resp. staff 3 stands at e, but staff 4 begins with the clivis hg (c3 confirmed). The notes are followed and the header records this. It looks like a misprint in the leaf.
  2. Syllables in "i-ra-cún-di-æ" (staff 5) are squeezed. Notes were assigned by neume spacing: i(hf/h/h) ra(h) cún(hfh) di(h) æ(...).
  3. Readings of neume groups:
     - "re(jh/jki/h/hv/fgf)": virga h, then torculus fgf. teresia_gr has the same formula written as "h/hf/gf".
     - "bér(ed/dc~)" is read as a liquescent.

## Not done: the 1939 Missal
- M39 calendar (m39lin.txt line 3091): "S. Alberti Magni Ep., Conf. et Eccl. Doct. O. P. Totum Duplex I classis."
- I did not find the Mass text itself yet. Search the Proprium for 15 Nov to see whether it says "Missa In medio" with proper Resp./Alleluia or refers to the Common of Doctors.
- The site (masses.js S1115) currently gives:
  - in 6549 In medio
  - gr 4733 Os justi
  - al 6959 Posui
  - of 7170 Veritas mea
  - co 5425 Domine quinque talenta
  - lent tr 7081
  - It is marked "Chants as assigned by the St. Dominic Missal (1959)".

## Proposed corrections.json entry (once the checker passes the two files, and after the M39 check)
```
"S1115": {
  "src": "G28 suppl. S.R.C. 9 June 1933 (bound leaf pp. 1-2) = G50 pp. 616-617: Missa In medio, in Festo unius Doctoris, pag. 35*, praeter sequentia (Resp. Ecce sacerdos magnus, V. Inventus est justus; Alleluia V. Vere magnus est in caelis Albertus)",
  "set": { "gr": ["g28:albertus_gr|Ecce sacerdos magnus|suppl. 1933 p. 1"],
           "al": ["g28:albertus_al|Vere magnus est in caelis|suppl. 1933 p. 2"] },
  "ok": { "in": "35*", "of": "31*", "co": "39*" }
}
```
- Copy the exact `'g28:file|incipit|page'` form from an existing `set` entry, such as teresia or bertrand, if one is wired by then.
- in/of/co stay those of the In medio Mass of Doctors, as on the other Doctor feasts in corrections.json, e.g. co 5425.
- **Paschal-time Alleluia:** not applicable on 15 Nov.
- **Open question for main:** 6549's G50 title is "In medio Ecclesiae all. all." Check whether it is the Paschal form. If it is, the non-Paschal In medio Introit should be used.
