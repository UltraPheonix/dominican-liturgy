# Chant check against the Missale O.P. (1939) — resolved 2026-11-26

The 21 differences listed here earlier (site vs the St. Dominic Missal 1959, as read by OCR) were each checked against the
Missale O.P. 1939 (M39.pdf, text layer + page images). Fixes are in `tools/m33/propers_fix.json` (applied by
`tools/m33/propers_apply.py`, called by `tools/build_masses.py`).

## Saints

| Mass | Result |
|---|---|
| 6 Dec. S. Nicolai | site = M39 (gr Ecce sacerdos, al Justus germinabit, co Beatus servus); no change |
| G470 «Invocabit Dominum» (S. Pius V) | FIXED: gr Juravit Dominus (outside Paschaltide); Paschaltide: Alleluias Fortitudo mea + Angelus Domini (M39 pp. 432-434) |
| 24 Jun. Nativity of St John Baptist | site = M39 (gr Priusquam, al Inter natos, co Tu puer); no change |
| 10 Jul. Seven Holy Brothers | site = M39 (al Laudate pueri); no change |
| G555 «Adeamus» (Immaculate Heart) | site = M39 supplement pp. 4-6; no change |
| «Gaudeamus... assumptione» | no longer on the site |
| 19 Sept. St Januarius | FIXED: gr Gloriosus Deus, al Sancti tui Domine, co Dico autem vobis (M39 pp. 562-563) |
| 3 Oct. St Thérèse | not in M39 (no Dominican source); left |
| 19 Jan. B. Andrew of Peschiera | FIXED with 27 other confessors "Os justi, ut in Communi Conf. non Pont., pag. 23*": gr Domine praevenisti, co Amen dico vobis (M39 pp. 23*-24*) |
| 9 Jul. St John of Cologne, Gospel | site = M39 (Luke 6); no change |

## Proper of the Time

All site = M39, no change: Dec25_2 (gr Benedictus qui venit), Nat1 (al Dominus regnavit), 5af (gr Unam petii... Ut videam),
Quad4t (gr Exsurge... fer opem), Quad6h (gr Christus factus est, co Dominus Jesus), Pasc0m (gr Dicat nunc Israel),
Pasc0w (in Venite benedicti, gr Dextera Domini, al/co Christus resurgens), Pasc0h (gr Lapidem), Corpus Christi
(gr Oculi omnium, al Caro mea, of Sacerdotes Domini, co Quotiescumque), Sacred Heart (Cogitationes Mass of the M39
supplement; co Unus militum, in votive Masses Si quis sitit).
Epi2 Alleluia: the Graduale O.P. 1950 (p. 50) sings "Laudate Deum omnes Angeli ejus", the Missal prints "Laudate Dominum";
the site follows the Graduale for the chant.
Note: the 1939 Missal's own Sacred Heart Mass (p. 263ff.) is the older "Egredimini" Mass; the supplement's 1929 Mass is used.
