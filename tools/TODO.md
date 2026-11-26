# Whole-site TODO (2026-11-26 12:50, live sw propria-v89). Rule: pre-1955 Dominican rite only; Dominican sources only; no inferred chant.

## A. 1909 Office — live errors (fix first)
DONE 2026-11-26 sw v90: A1 (first prayer after the heading; 'Oratio,' accepted; vigil prayer → oratio_v1; running heads cut by
  offices.text_sancti), A2 (no run-ons: build.clean_prayer/final_prayer), A3 partly (drop-caps, æ, OCR confusions vs DO word counts
  tools/b09/latcount.py, conclusion restored). LEFT in A3: Bl. Lucy 11-16 'Luriam', Jerome Emiliani 07-21 garbled middle, Aug 8
  'Kcdesise/intercessitine', Bl. Clare 04-17 'Tribus … pœniténtia … beáta:', Bl. Albert 05-13, Bl. Giles 05-14, St Alexius 07-17,
  Bl. Jordan 02-15 → check scans; and the Temporale Matins lessons (≈530 Hours >4% unknown words, e.g. 05-05 Matins).
1. Saints' prayers: offices.py takes the wrong "Oratio" (accept "Oratio," and drop-cap glitches; take the FIRST prayer after the heading);
   build.py san_oratio: refuse a prayer that doesn't name the saint (or N.) unless verified. Known wrong: 11-20, 12-02, 01-19, 07-21, 07-24,
   08-08, 11-30 (feast got vigil prayer) + ~22 more of 115.
2. Run-on prayers into the next Office's OCR: 11-20, 03-20, 04-05, 05-28, 10-24.
3. OCR garbage in prayers/lessons (566 Hours on 371 days): repair vs DO Sancti/SanctiOP + latdict; scan check for the rest.
4. Test, bump sw, push.

## B. 1909 Office — finish
5. Commons (archive/1909-commons-2026-11-26.json) on a branch: saint's name for N. (declined), proper Offices before the Common (Dec 8 …),
   proper responsories (St Andrew), Paschaltide Commons with 7 responsories, 24 doubtful readings vs scans, Commons' Matins lessons;
   live only when clean.
6. Holy Week + Triduum line by line from the scans (must be perfect).
7. Christmas–Epiphany (v1 pdf 284–373), Sundays after Epiphany, Septuagesima–Lent, Paschaltide, Ascension–Corpus Christi.
8. Summer 'historiae' (ferial lessons after Trinity), Advent Matins lessons/responsories left, St Thomas 21 Dec ant., Christmas Vigil.
9. Exact precedence from the Rubricae generales (v1 pdf 40–70): concurrence, octaves, Saturday BVM Office, simplex/memoria, transfers.
10. Office of the BVM, Office of the Dead, Officium S. P. Dominici (v1 1433–1510).
11. Remove the 406 'in preparation' placeholders as each part lands.

## C. 1954 Office
12. Rubric engine with pre-1955 ranks replacing the 1962-based data (Totum Duplex/Duplex/Semiduplex/Simplex, octaves, commemorations,
    preces, Compline psalms by rank, Rosary on 1st Sunday of Oct., Te lucis by rank).
13. Matins frame from Matutinum 1936 Toni communes (Domine labia, invitatory tones I, II, IV B, V–VIII; versicles; blessings; lesson tones).
14. Matins of the 14 solemnities (Matutinum 1936, ~250 pieces).
15. ~29 Matins hymns without chant (only from a printed Dominican source).
16. Compline leftovers: Te lucis of St Antoninus, St Augustine, St Rose, St Louis Bertrand, St Teresa alt.; Septem Fundatores Nunc dimittis ant.;
    Our Lady in Lent / Paschaltide hymn stanzas; Sancta Dei Genitrix, Virgo Maria non est ulla; Good Friday Ps 50 without chant; Salve/O lumen check.
17. Lauds, Vespers, Little Hours audit against AM 1933; Office of the Dead melodies.

## D. Chant for both Offices
18. Nocturnale S.O.P. (n1, n2, na, nc in Drive) decoding → ordinary Matins chant.
19. Jandel 1862 Antiphonary (GB 35/36 + transcription) for the 1909 Office; 1933 books where texts are identical.

## E. Mass
20. DONE 2026-11-26 (Mass chat): orations from Missale O.P. 1939 for all Masses that have a pre-1955 Dominican source; the 26 left
    are listed in tools/orat39/MISSING.md (no source). Oratio super populum added on the 36 Lenten ferias.
21. DONE 2026-11-26: every Divinum Officium oration checked (tools/orat39/do_check.json); 63 Masses replaced by the 1939 text (Commune Doctorum, Compassion, All Souls x3, Octave of Christmas, Vigil of SS. Peter & Paul, Commons...). Left from DO: C1s, S0501 (1956), S1003 (not in M39).
22. DONE 2026-11-26: AUDIT.md items checked vs M39 (Januarius, Pius V votive fixed; 28 'Os justi ut in Communi' confessors fixed; rest already right).
23. DONE 2026-11-26: S0915 sings Alleluia 'Stabat sancta Maria' in place of the Tract (M33 p.381 / M39 p.313: one verse; 'O vos omnes' is only the Tract's verse). Roman melody (GR 1961 p.596, GregoBase 853, badge): no O.P. melody on GregoBase. Open: the Sequence's added 'Alleluia' on that day is not notated.
24. Calendar on pre-1955 ranks (now 1960 classes shown); remove/replace the 'Reformed 1959' Holy Week toggle per the rite rule (ask Joseph).
25. Options Mass list blank on the last Sunday after Trinity.
26. Mass prayers from the 1933 Missal (needs page images).

## F. Holy Week page
27. Good Friday Office (Tenebrae, Hours, Vespers, Compline), Holy Saturday Office, Holy Saturday tracts vs Triduum 1927, Sanctus/Ite,
    Palm Sunday procession chants (Processionarium 1913) last.

## G. Booklets
28. Priest booklet: Ite/Benedicamus, Gloria/Credo intonations, oration tones, Epistle/Gospel tones (Missal appendix).
29. Booklet polish.

## H. UI / site
30. UI clean-up (17 small fixes proposed 2026-11-26, dropped — re-propose).
31. Site-wide check script for the Office (like tools/check/year.py for Mass): unknown words, run-ons, wrong prayers, placeholders.
