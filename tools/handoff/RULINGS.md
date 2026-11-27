# Joseph's rulings (27 Nov 2026), for every agent

## Prefaces and calendar
- **Prefaces:** use the proper Prefaces on the inserted leaves of the 1939 Missal: St Thomas, p. 137; Sacred Heart, p. 135. Do this even where the Ordo 1944 gives the Lent or Nativity Preface.
  - The inserted Sacred Heart rubric applies literally. Where it is silent, follow the Ordo 1944: the Vigil of St John takes the common Preface, and the Sunday in the Sacred Heart octave takes the Nativity Preface.
- **Rubr. VI.2:** when a week has no free day for the weekly Requiem, add Omnipotens on the lowest-ranked weekday (the first one if two tie). This is Lead F's rule; keep it.
- **Paschal ferias:** alternate the two Alleluia verses as the Ordo 1944 does: Tuesday takes the 1st verse, Wednesday the 2nd, and so on.

## Saints' Masses
- **28 Apr:** the Mass is B. Louis Grignion de Montfort, Os justi. St Paul of the Cross has only a Memoria in the 1939 Missal (pp. 420-421).
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
- **Spelling (coordinator, after the audit):** convert consonantal i → j in data/orations.js (and addiv/memoriae) to the 1939 Missal's spelling (ejus, Jesum, cujus, majestas…), taking each word's form from the Missal, by script.
- **Holy Saturday Sanctus (Joseph):** Sanctus I, by the first-class rule, is correct.

- **Standing instruction (Joseph, 27 Nov):** whenever a corrected text can easily be set to chant (Collects, Introits and the like), set it straight away; no need to ask.
