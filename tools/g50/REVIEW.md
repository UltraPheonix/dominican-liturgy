# Review of tools/g50/check_report.txt (Mass chat, 27 Nov 2026)

The checker splits the Graduale O.P. (1950) OCR at each "Die N ..." heading; most flags come from a block taking in the next
feast's references or printed chants (fixed for "Die 24 vel 25 ..." headings). Each flag was read against the OCR and the
Missale O.P. (1939). No page scans of the Graduale are reachable here (archive.org copy is loan-only).

## Fixed (tools/check/fix_statuit.py, tools/check/fix_g50_review.py, G515 in place)
- Common Statuit (Conf. Pont.): Communio is Beatus servus in both books (M39 18*, G50 32*), not Fidelis servus. Fixed in C32s and
  16 Masses that take it whole (Corsini, Norbert, Patrick, Remigius, Gregory Thaumaturgus, Benedict XI, BB. Franchi, Augustine of
  Lucera, John Dominici, Innocent V, James of Voragine, Bartholomew of Braganza, and the later beati that copy it).
  S. Gregory Nazianzen keeps Fidelis servus (printed in M39); Masses marked m39 left as they are.
- Septuagesima Tracts of the Commons (both books agree): Sacerdotes tui Desiderium; Statuit, Justus ut palma, Os justi Beatus vir;
  Loquebar, Gaudeamus (Virgin), Dilexisti Qui seminant. Added to C30s, C32s, C39s, C42s, C45s, C51s, C55s.
- S. Andrew Corsini (4 Feb.): Tract Beatus vir (was Qui seminant). S. Scholastica (10 Feb.): stray Tract Tu gloria (11 Feb.) removed,
  Tract Qui seminant (was Veni sponsa, which is the holy women's). BB. Sibyllina (23 Mar.) and Margaret of Castello (13 Apr.):
  Qui seminant (G50: the Common whole). NB the Missal prints a proper Tract for each (Ave Maria; Beatus vir): the Graduale is followed.
- S. Margaret of Hungary (19 Jan.): her own Mass from G50 pp. 398-399 (was the Common of a Virgin after the St Dominic Missal 1959).
- Octave of Ss. Peter and Paul (6 Jul., G515): Responsorium In omnem, Alleluia Isti sunt, Offertorium Exsultabunt (were
  "inferred" chants of other Masses); now linked in the calendar.

## False positives (no change)
S1208, S1213, S0118_2, S0130b and S1008 (holy women: the site's chants match M39's Common nec V. nec M.; widows keep Veni sponsa),
S0212, S0223, S0405, S0429 and S0503 (always in Paschaltide), S0505, S0517b, S0524, S0530b (apart from the Communio, fixed), S0704b,
S0620b, S0804, S0806, S0815, S0822, S0829, S0908, S0910, G566, S0920, S0930, S1030b, G502.

## Still open
- 168 chants in data/masses.js are marked "inferred" (assigned by rule or by text, not read from the page of that feast).
  Many are the Lenten ferial Tract or Common references and are likely right, but each should be checked against the Graduale.
- 43 orations in data/orations.js lack their Latin conclusion (e.g. Pasc1, Pasc4 se, Asc pc, Pent0m se).
