# Lead A (processions and litanies): state, 27 Nov 2026

## Done (built into processions.html, every gabc compiles, Chrome: 59/59 blocks drawn, no console errors)
- **Loreto litany, pp. 91-94.** `node tools/proc/gen_lit.js` writes lor_invocation_maria, _speculum and _regina, with every invocation. I checked them line by line against how the book lines its text up under the notes on pp. 92-93 (formula A f/g/h, B h/B-flat/g, C j/h/i). Regina in caelum assumpta is labelled "Added after 1913, typed into the scanned copy".
- **Litany of the Saints, pp. 126-130.**
  - Regenerated: lit_miserere (the ℟ repeats the whole invocation), lit_ora, lit_ora_michael, lit_orate, lit_libera, lit_rogamus.
  - New: lit_sancti (Joannes Baptista to Antoninus) and lit_sancti_dominice (after "Vox exaltetur", Dominic to Omnes Sancti).
  - lit_propitius now has its second line, Exaudi nos, sung to the same notes (both lines are printed under one staff).
  - Ut omnes errantes is labelled as added after 1913.
  - The text was checked against the book. Fixes: dǽmonum, Christiánum, origináli.
- **Rogations, p. 125.** tone_rog_versus and tone_rog_parce are made by gen_tones.js (the versicle tone of pp. 395-396, the prayer tone of pp. 407-408).
- **gen_tones.js** is now the only versicle/prayer engine; gen_lit.js makes only the litanies.
  - It reads the texts from proc_data.py and no longer needs /tmp/gen/texts.json.
  - It skips the † when it counts syllables.
- **Item 9 (punctuation).** The Latin of the prayers now follows the book exactly: its flexa sign (written †), its colons (including the colon before Per Christum) and its commas. These prayers are done:
  - Ascension p. 50, with the colon after "nobis" and ", qui tecum vivit, et regnat";
  - Omnipotens p. 67, including the book's "charitátis" and "eúmdem";
  - Erudi p. 72;
  - Concede nos pp. 90-91;
  - Concede (Dominic) p. 91;
  - Gratiam and Protege p. 95;
  - Parce p. 125.

  The versicles "Ora pro nobis beáte Pater Domínice" and "Ora pro nobis sancta Dei Génitrix" lose their comma, as in the book. I diffed the regenerated tone_* files: only the words changed, every note is the same.

## Open
1. **W-A2's extraordinariae block** (end of proc_data.py, gen_ex.js, ex_*.gabc) is in the current build but **I have NOT checked it against pp. 131-134**.
   - It sets the four versicles that end on a monosyllable followed by ":" (ádjuva nos, líbera nos, tuére nos, in te) all on h, with no inflexion. The book gives no example of this, so it is a guess. Joseph should decide, or they should stay as text.
   - ex_versus has "Ora pro nobis, sancta Dei Génitrix" with a comma. Check p. 131: p. 95 prints it without one.
   - Do not push processions.html before this check.
2. lor_agnus: the note on "qui" is hidden under the pasted slip on p. 93 (known, left empty).
3. Questions answered by Joseph: Sancte Joseph is sung to the general formula, and the post-1913 additions are kept and labelled.
