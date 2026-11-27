# Handoff: processions.html, setting every litany to chant in full

Status: **research done, generator drafted, nothing wired in.** I have not changed `proc_data.py`, `build_proc.py`, any existing `.gabc` or `processions.html`. `build_proc.py` runs cleanly (processions.html is 111790 bytes, the same as before).

## Files
- `tools/proc/gen_lit.js`: **DRAFT. Written but not yet run or tested.** It is a node generator that writes the full gabc files. It reads the litany texts from `proc_data.py` (LIT_LAUR, LIT_SANCT, through python3), so the chant and the text stay in step. Running it **overwrites** these existing files: `lor_invocation_maria`, `lor_invocation_speculum`, `lor_invocation_regina`, `lit_miserere`, `lit_ora`, `lit_ora_michael`, `lit_orate`, `lit_libera`, `lit_rogamus`.
  It also creates new files: `lit_sancti`, `lit_sancti_dominice`, `rog_versus`, `lor_ora_gratiam`, `lor_post_partum`, `ex_versus`, `ex_orationes`, plus `ex_ecclesia`, `ex_pace`, `ex_pluvia`, `ex_serenitate`, `ex_pestilentia`, `ex_turcas`, `ex_papa` and `ex_rege`.
- Source: `/home/claude/dl/proc/p.pdf`, where pdf page = printed page + 16 (checked: p. 91 = pdf 107). The note in the proc_data.py header that says +15 is wrong.

## Existing files checked against the scan (all correct, keep them)
lor_kyrie (p. 91), lor_invocation_miserere (p. 92, already all 4 lines), lor_agnus (pp. 93-94), lit_kyrie and lit_christe_audi (p. 126), lit_propitius (p. 128), lit_agnus (p. 130), lit_extra_kyrie and lit_extra_pater (p. 131). The model formulas in lor_invocation_*, lit_ora, lit_ora_michael, lit_orate, lit_libera and lit_rogamus are also correct.
gabc pitch letters: lines are d f h j, spaces c e g i k. The Loreto staves and the start of the Saints litany are c4. Propitius, Libera, Peccatores and Agnus are c3. The versicle and oration tones use an F clef on the 3rd line (f3). The extra square before the C-shape is what makes it an F clef.

## Formula and accent rules, read from how the book lines its own examples up under the notes
For each one I drew red guide lines at the note x-positions over the 600 dpi scans to check the alignment.
- **Loreto A**, p. 92 (Sancta Maria ... Virgo fidelis, c4): the recitation is on f. The last accent goes on g. A second post-tonic syllable also goes on g. The last syllable goes on h. ℟ o(f)ra(e)pro(d)no(e)bis(f). Notes the formula has to spare are simply not sung: the book's own lines show this (Ma-ter Chri-sti, Vir-go pó-tens, Ma-ter pu-rís-si-ma).
- **Loreto B**, pp. 92-93 (Speculum ... Auxilium): the recitation is on h. The last accent goes on (ixi), which is B-flat. Every syllable after it goes on g. ℟ g f g h h. The book shows this with Fœ-de-ris ar-ca, Re-fú-gi-um pec-ca-tó-rum and Vas spi-ri-tu-á-le.
- **Loreto C**, p. 93 (Regina Angelorum ...): the recitation is on j. The 2 syllables before the last accent go on h and then i. The accent and everything after it go on j. ℟ h g f g h. The book shows this with Re-gí-na Már-ty-rum, San-ctó-rum óm-ni-um, and li-con-cép-ta for "originali concepta". "Regina in caelum assumpta" is a typed slip pasted into the scan (1950).
- **Saints, Trinity**, p. 126 (c4): every syllable is on g except De- (of Deus), which is on h. Then (;) and mi(g)se(g)ré(e)re(f)no(g)bis(g). The book prints "℟. Pater., etc.", meaning the choir repeats the whole invocation. The draft writes that repetition out in full.
- **Saints, Sancta Maria**, p. 126 (c4): the recitation is on g. The last accent goes on h. Every syllable after it goes on g (Gé-ni-trix, Vír-gi-num). ℟ g e f g g. The plural formula on p. 127 (Omnes sancti Angeli ... Archángeli) has the same invocation notes, with ℟ Oráte g g e f g g. The plain-text list on pp. 127-128 ("ora." and "oráte.") is set to these. "Vox exaltetur" comes before Sancte Pater Dominice, and the book gives no other notes for it.
- **Michael, Gabriel, Raphael**, p. 126: every syllable is on g except the last, which is on h. *Uncertain:* the draft gives Joseph the general formula (Jó-seph), not the Michael one. The book does not say which.
- **Libera**, p. 128 (c3): the recitation is on h. The 2 syllables before the last accent go on g and then f. The accent and everything after it go on h (A dam-na-ti-ó-ne per-pé-tu-a). ℟ Lí(g)be(h)ra(f)nos(e)Dó(f)mi(e)ne(d).
- **Te rogamus**, p. 129 (c3): Pec(h)ca(g)tó(i)res(i). The general rule is a recitation on h, the syllable before the last accent on g, and the accent and everything after it on i. ℟ te(h)ro(g)gá(f)mus(e)au(f)di(h)nos(h). "Ut omnes errantes" is typed below p. 129 in the scan.
- **Versicle tone**, p. 395, IV 3o ("in Processionibus, et quotiescumque dicitur ℣. a Sacerdote"), f3: every syllable is on h and the last syllable is on f. The book gives no proparoxytone example, so the draft lowers only the last syllable, as all 3 printed examples do. The T.P. form is on p. 396 (al-le-lú-ia, with ia on f).
- **Oration tone**: use **p. 407-408, III** ("Orationes ad Horas, et quotiescumque aliae Orationes quae non sunt de corpore Officii et Missae"). It differs from pp. 404-406 (tone II) and from Harrison/mtones.js, so follow p. 407. It is given only by example, with Concede nos as the example:
  - Dominus vobiscum: h h h h h f. ℟ Et cum spíritu tu-o is g g g g g g h. Orémus is h h f.
  - Flex at the book's flexa sign (✝ in the texts; † in the draft): the syllables after the last accent go on f (tri-stí-ti-a, Fí-li-um tú-um).
  - Mediation at a colon: the syllable just before the last accent goes on f. The one before that goes on g. If the third syllable before the accent ends a dactyl, it goes on g too, following the 2o rule on p. 405 (pér-fru-i læ-tí-ti-a). The accent and everything after it go on h. Examples: sa-lú-te gau-dé-re, sanc(g)ti(f) Dé(h)us.
  - Conclusion: Per Christum Dóminum nos-trum, with trum on f. ℟ A(g)men(h). The long form is on p. 408.
  - Commas carry no inflexion.

## Left to do (how to resume)
1. Run `node tools/proc/gen_lit.js` and fix any errors. Watch the `syls()` and `wordsOk()` accent checks: Raymúnde has a hyphenation fix, and the texts contain "áëris" and "N.". Then check every file with `cd /tmp && gregorio -o x.gtex FILE`.
2. Do a second checking pass: compare 3-4 generated lines per block against the alignment of the scan.
3. Wire the new files into `proc_data.py` with `_at`:
   - lauretanae: change the heading "Tonus Litaniarum" to the full litany. Add `lor_ora_gratiam` before the ℣. Ora pro nobis text, and `lor_post_partum` before the ℣. Post partum text.
   - litaniae: after `lit_orate` add `lit_sancti`, then a rub "Vox exaltétur", then `lit_sancti_dominice`. Update the rubrics that say "et sic de céteris".
   - rogationes: put `rog_versus` before the ℣. Osténde text. The rogation litany is the Saints litany (pp. 126-130), so nothing separate is needed for it.
   - extraordinariae: put `ex_versus` before its ℣ text. Then add the pp. 132-134 texts, which are not in proc_data yet. They are the rubric "Deinde absque Dominus vobiscum ... Oremus", Concede and Parce (`ex_orationes`), the rubric "Demum subjungat ...", and the 8 occasions, each with a rub, a gabc block and a txt with an English translation. The Latin is in OCC in gen_lit.js. Section pages become [131, 134].
4. Run `python3 tools/proc/build_proc.py`. Serve with `python3 -m http.server 8765`. Check processions.html in headless Chrome (playwright, /usr/bin/google-chrome): no console errors, and the chant is drawn.
