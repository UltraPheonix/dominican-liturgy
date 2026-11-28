# Joseph's rulings (27 Nov 2026), for every agent

## Prefaces and calendar
- **Prefaces:** use the proper Prefaces on the inserted leaves of the 1939 Missal: St Thomas, p. 137; Sacred Heart, p. 135. Do this even where the Ordo 1944 gives the Lent or Nativity Preface.
  - The inserted Sacred Heart rubric applies literally. Where it is silent, follow the Ordo 1944: the Vigil of St John takes the common Preface, and the Sunday in the Sacred Heart octave takes the Nativity Preface.
- **Rubr. VI.2:** when a week has no free day for the weekly Requiem, add Omnipotens on the lowest-ranked weekday (the first one if two tie). This is Lead F's rule; keep it.
- **Paschal ferias:** alternate the two Alleluia verses as the Ordo 1944 does: Tuesday takes the 1st verse, Wednesday the 2nd, and so on.

## Missing English (Joseph, 27 Nov 22:05)
- Where the Missal's Latin is on the site but the St Dominic Missal 1959 has no English for it: an AI translation of the Missal's Latin, labelled "AI translation".
- C76s (Cum sanctificatus, p. 54*, "Cetera ut supra, excepto quod nullum allelúia dicitur"): search G28/G50 for a Dominican non-alleluia Offertory and Communion first; report before deciding.
- Joseph's standing goal: no errors on any day in the text or the choice of Mass (rubrics and readings); every prayer, reading and proper the Missal prints must be on the site.

## Conclusions and named Introits (Joseph, 27 Nov 22:15)
- "Qui tecum" conclusions (Rubr. gen. XI.2, p. 52): follow the Missal's printed pointing, "Fílium tuum; qui tecum" (';' = flexa), in the text and the sung tone. **Joseph 22:35: ';' everywhere**, also in every conclusion the site expands from a bare "Per Dóminum". Done by canon() in tools/audit/apply_fixes.py (runs on every apply). The 110 ", qui tecum" (mostly after Per eúmdem) are left as the auditors find them printed.
- Ember Saturday of Pentecost Alleluias (pp. 254-256): read from the G28 (pp. 261-262), fetched from Joseph's Drive.
- Introit Gaudeamus with a saint's name (M39 pp. 485, 502, 508, 36*; G50 p. 509 "cum nomine"): print the Missal's text with the name; use notated chant only where a Dominican book prints the melody with that name (never adapt it ourselves).
- Coordinator's application of the rubric (no question needed): Dedication Secret "Extra ecclesiam dedicatam" (p. 3*) for S1109 and S1118; S1113 is dated by the Kalendarium (10 Nov), handled in the calendar step.

## Answers 27 Nov 22:25 (Joseph)
- G385 and G505 (Graduale-page copies of St Stephen and of the Commemoration of St Paul): keep them, and fix their reading references to the Missal.
- S0529b and S0602b: switch the readings by season as their rubric says (Sancti tui p. 15* in Paschaltide; Salus autem p. 13* outside it).
- S0904b: the readings of the Mass the Missal names (Gaudeamus, Common p. 30*), not the proper ones.
- Dedication Secret for S1109 and S1118: the "extra ecclesiam dedicatam" form (p. 3*), confirmed.

## Answers 27 Nov 22:45 (Joseph)
- Step 2 (calendar/selection logic, ordo44_diff.md) starts NOW, in parallel with the text audit; the coordinator fixes js/ rule by rule, quoting each rubric.
- Dec24 Gospel: "desponsáta" (the Vulgate); the Missal's "deponsáta" (p. 17) is a printer's slip.
- After this round: an independent checker re-reads a random 1-in-10 sample of the audit fixes on the scan.
- Conclusions: the whole printed pointing of the full conclusion is applied everywhere by canon() in apply_fixes.py: "Fílium tuum; qui tecum", "cum Deo Patre; in unitáte", "Spíritus Sancti Deus: per ómnia" (M39 p. 16 and passim), and no comma in "Jesum Christum Fílium tuum;" (pp. 472-475, 516, 545).
- Coordinator under these rulings: where no Dominican book prints a named Introit melody, the notated chant is hidden and the Missal's text (masses.js parts.in[0].m39text) is shown; the votive "per annum" forms (pp. 492, 503, 547) get a selector in the app; C39s's "Aliud Evangelium" (p. 23*) is shown as an alternative Gospel.

## Answers 27 Nov 23:00 (Joseph)
- C76s Communion (p. 54*, "nullum allelúia dicitur"): stop before the alleluias, as the Offertory's printed Septuagesima ending (G50 p. 251), with a note citing p. 54*.
- C104s Gradual (p. 90*, "Misit Dóminus … de morte eórum"): read this Mass's own Gradual from G28/G50 (pp. 104*-105*) first.
- Readings whose Latin departs from the Vulgate (e.g. Sap 10 pp. 539, 541; Hebr 11 p. 526): the English follows the Missal's Latin, labelled "AI translation".
- Coordinator under the rulings above: S0113 (13 Jan "Commemoratio Baptismatis", not in the 1939 Missal, duplicates EpiOct, unused by the calendar) is dropped like C1s; Gospel English gets "At that time Jesus said to his disciples" etc. wherever the Latin has the incipit (follow the Latin).

## Answers 28 Nov 08:10 (Joseph)
- EmbSatSeptS ("Sabbato IV Temporum, forma brevior", from the 1959 Missal; the 1939 Missal pp. 291-296 prints only the full Mass): dropped from the menu.
- Pent23 Epistle (p. 303): show the asterisk before "Itaque fratres mei caríssimi" as printed.
- Coordinator: the Gospel-opening script (scripts/C0/incipits.py) now replaces only reviewed Douay lead-ins; its first run's damage was corrected in v246.

## Saints' Masses
- **28 Apr:** the Mass is B. Louis Grignion de Montfort, Os justi. St Paul of the Cross has only a Memoria in the 1939 Missal (pp. 420-421).
- **C1s "Commune Apostolorum" (Joseph, 27 Nov 21:40):** drop it. The 1939 Missal has no such Mass; "only use the Missal".
- **All Souls Masses II and III (S1102_2, S1102_3) (Joseph, 27 Nov 21:40):** "use whatever is in the Missal": the Gradual Requiem with V. Animae eorum, as printed on M39 pp. 610-612 (G50 p. 115*), not In memoria.
- **St Raphael:** the chant follows the Graduale (Alleluia In conspectu … Domine Deus meus). The note says that the Missal p. 596 prints a different verse.

## Chant: which book's pointing, which tone
- **Pointing:** where a Dominican book prints a text pointed for singing, follow that book's pointing. This covers the Processionarium (e.g. the Palm Sunday Gospel, pp. 23-24) and the Triduum 1927 (e.g. the Good Friday lessons and solemn prayers). Keep the Missal's words.
- **Monosyllable endings:** a versicle that ends in a monosyllable followed by ':' (e.g. "líbera nos :") is recited through: recto, no fall.
- **Good Friday:**
  - Respice goes in the Hours tone (Proc. pp. 407-408), ending on the flex as the Triduum prints it.
  - Libera nos stays as text; no Dominican book notates it.
  - The third solemn prayer is sung as printed, "in unitáte Spíritus", without ejúsdem.
- **Holy Saturday font blessing:**
  - The prayers Omnipotens… respice and Omnipotens… adesto go in tone III. The Concede at the font goes in tone II.
  - The Preface uses the SOLEMN tone. The "legendo" passages go in the same Preface tone, with the rubric kept above them.
  - Descendat is set once, with the rubric quoted.
  - The oil formulas stay as text.
  - The Concede: print it as the book has it, and sing "Per Dóminum".
- **Rubrics that say "sine nota" or "humili voce":** still give the chant in its proper tone, and keep the rubric quoted above it.
- **Holy Week Postcommunions:** each one carries its own sung Dóminus vobíscum and Orémus, hidden when the Order of Mass is shown.
- **Maundy Thursday:** the Prime prayers and the Tenebrae lessons IV-IX are in scope for chant.
- **Passion tones:** every Chronista final cadence takes the B flat, as Fr Innocent Smith does.
- **Passion tones, C.md questions (Joseph, 27 Nov 21:50):**
  1. Chronista final on a dactyl ("Dóminum"; Proc. p. 436 prints only spondees): Dó(g) mi(f) num(ed).
  2. Christus (Proc. p. 437): always the full incipit (Scitis) for every sentence; do not use the alternative incipits Opus / Jam / Mittens.
  3. Chronista B flat (pp. 435-436): flat in every final and in the cadence before Christ; natural in the mediation.
  4. "nisi in brevioribus" (p. 435): no mediation when the member has fewer than 6 syllables.
  5. The short stroke inside melismas (Voce ma-|gna, Trá-|didit, Con-|tra, Scitis|): a divisio minima, as Fr Smith.

## Litanies
- **Litanies:** Sancte Joseph takes the general formula. Keep "Regina in caelum assumpta" and "Ut omnes errantes", labelled as added after 1913.

## Booklets and English
- **Booklets:** the choir and priest booklets include the Asperges (or the Vidi aquam) with its versicles and prayer in chant on Sundays.
- **1959 English:** copy the 1959 St Dominic Missal verbatim, but correct obvious spelling typos ("spirtual", "sactifices"). Never change the wording.

## Open task found by Lead H (27 Nov)
- **Divinum Officium punctuation in orations.js:** 163 of 472 Masses (src "Tempora/…", "Sancti/…", "Commune/…") still carry Divinum Officium punctuation, not the 1939 Missal's.
  - Proc. p. 405 makes the Missal's ';' the flexio and ':' the elevatio, so these prayers are sung by the alternation rule, not the book's pointing.
  - To fix: re-punctuate their Latin against the M39 scan. This is a text job for Lead E's area.
  - Example: Adv1 should read "quǽsumus Dómine … erípi; te liberánte … Patre; in unitáte Spíritus Sancti Deus :".
- **Convention from W-B6 for Holy Week day workers:** put the Postcommunion's sung Dóminus vobíscum·Orémus G: line right next to its "L: Postcommunio" line, and give it an id containing dv, vobiscum or oremus (e.g. op-hw-quad6m-pc-dv). app.js hides such blocks when the Order of Mass is on.
- **Spelling: CANCELLED by Joseph (27 Nov 21:46, "don't worry about the i to j"). Do not run it.** (Was: convert consonantal i → j in data/orations.js (and addiv/memoriae) to the 1939 Missal's spelling (ejus, Jesum, cujus, majestas…), taking each word's form from the Missal, by script.
- **Holy Saturday Sanctus (Joseph):** Sanctus I, by the first-class rule, is correct.

- **Standing instruction (Joseph, 27 Nov):** whenever a corrected text can easily be set to chant (Collects, Introits and the like), set it straight away; no need to ask.
