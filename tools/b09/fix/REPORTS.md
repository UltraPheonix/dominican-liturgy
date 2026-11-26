# Eye pass — round 1 (2026-11-26 evening): helpers' reports, condensed. 46 feasts, fix/b00…b05.json. Nothing was illegible.

Done (key = title): b00 Margarita de Sabaudia (v2 pdf 1098-1100), Jacobus de Benefactis, Barbara, Sebastianus Maggi, Dominicus Sylensis,
Thomas Ap., Maria Mancini, Stephanus Protomartyr · b01 Joannes Ap., Innocentes, Thomas Ep. M., Gundisalvus, SS. Nomen Jesu ·
b02 Stephana de Quinzanis, Antonius Abb., Cathedra Romana, Fabianus & Sebastianus, Agnes, Vincentius, Raymundus ·
b03 Marcolinus, Conversio S. Pauli, Margarita de Hungaria, Chrysostomus, Translatio S. Thomæ, Franciscus Salesius, Octava S. Raymundi
(memoria only), Martina, Petrus Nolasco, Ignatius · b04 Purificatio, Blasius, Agatha, Dorothea, Romualdus, Joannes de Matha,
Bernardus Scammacca, Scholastica · b05 Catharina de Ricciis, Nicolaus Palea, Jordanus, Gregorius X, Laurentius a Ripafracta,
Octava S. Catharinæ, Cathedra Antiochena (extra T.P. form only), Petrus Damianus.

DECISIONS NEEDED (ask Joseph / decide once, then normalise all fix files):
1. Accents. This printing does NOT accent æ (sæculo, quæsumus, præmium), nor y, nor capital initials (Innocens, Ordinis, Angelus).
   Helpers typed as printed (some files mixed with ǽ / Ínnocens from the machine text). The site elsewhere uses ǽ and accented
   capitals. Choose: (a) as printed, (b) site convention (normalise with latdict). Either way make it uniform.
2. Prayer conclusions: 'Per.' expanded to 'Per Dóminum.'; printed full forms kept (Stephen 'qui tecum vivit', Holy Name 'Qui tecum').
3. Memoriae of the Christmas-octave feasts were put under v1.magn (+ versicle in the note); Octava S. Raymundi = memoria only,
   its antiphons under v1.magn / laud.bened / v2.magn → the build needs a proper 'memoria' shape.

MACHINE READING FAULTS FOUND (why unverified machine text is never shown — build.with_proper now uses verified text only):
- Offices missing from propers1909.json, their text merged into the feast before: 02-04 Andreas Corsini (in Blasius), 02-11 Desponsatio
  B.M.V. (in Scholastica), 02-17 Septem Fundatores (pdf 1002-1011, in Gregorius X; has a second T.P. form), 02-19 Alvarus (1012-1013),
  02-21 Aimo (1015-1016), 02-24 Matthias (from 1025, in Petrus Damianus), 11-28 Zedislava (in Margarita de Sabaudia, v2), 01-19
  Andreas a Piscaria (pdf 918-919). → transcribe these directly from the pages (no machine entry needed: fix key = calendar title).
- Lessons misnumbered or missed when the first lesson falls at a page foot (Stephana, Margarita de Hungaria, Franciscus Salesius,
  Petrus Damianus); responsories run into lessons; wrong 'pages' from show.py (Maggi, Stephen, Translatio) — trust the feast title on the page.
- Maggi: machine v1.magn/laud.ant/laud.bened/v2.magn belong to another Office (dropped: unverified machine text is not used).

NOT YET TRANSCRIBED (noted in each entry's 'note'): proper hymns (Gundisalvus 'Ad sacerdótis nova', Catharina de Ricciis, Cathedra
'Jam bone Pastor', Raymundus), Little-Hours chapters/responsories of full Offices, Lauds chapters and versicles, Purification's
Compline antiphons and the prose Inviolata, commemorations printed with a feast (Vedastus & Amandus, Apollonia, Timotheus, Polycarpus,
Julianus, Marcellus, Prisca, Emerentiana, Paulus Eremita, Valentinus…), 'Per Octavam' rubrics, the T.P. forms (Cathedra Antiochena,
Septem Fundatores), 'Post Cineres' rubrics for the I Nocturn lessons, Innocents: Te Deum not said (R. ix repeated) unless Sunday.
New key used by helpers: v1.vr (versicle after the hymn at I Vespers) — supported by the build.
Printed oddities kept as printed are listed in each entry's note (e.g. Margarita de Hungaria vj 'Póntifem', Catharina vi 'Extasum').
PDFs: /tmp/b09/v1.pdf, v2.pdf were symlinks to the uploads, now BROKEN (uploads gone after a container restart); the helpers read
/tmp/b09/b1.pdf, b2.pdf (CMAA scans of the same edition, same pagination — checked: 1577 pages, page 965 identical).
