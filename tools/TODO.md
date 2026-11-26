# Whole-site TODO (2026-11-26 12:50, live sw propria-v89). Rule: pre-1955 Dominican rite only; Dominican sources only; no inferred chant.

## A. 1909 Office — live errors (fix first)
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
21. Verify all orations from Divinum Officium against Missale O.P. 1939 (possible Roman forms).
22. AUDIT.md: 21 chant differences vs St Dominic Missal 1959 to check against the book (S. Nicolas, St John Baptist, etc.).
23. S0915 Seven Sorrows: 'Stabat sancta Maria' as Alleluia + 'O vos omnes' (M33).
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
