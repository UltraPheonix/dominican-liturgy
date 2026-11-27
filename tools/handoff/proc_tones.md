# Processions: tones for versicles and prayers (handoff)

## Status
Done. Every item below has been compiled (gregorio), built (`python3 tools/proc/build_proc.py`) and checked in headless Chrome (all 46 chant blocks draw, no console errors). Nothing is half done and there are no drafts. Nothing is committed.

## Files
- `tools/proc/gabc/tone_*.gabc` (13 files). Each header names the rule and pages it applies.
  - ascensio: `tone_asc_versus`, `tone_asc_oratio`
  - purificatio: `tone_pur_omnipotens`, `tone_pur_versus`, `tone_pur_erudi`
  - salve: `tone_salve_dignare`, `tone_salve_concede`, `tone_salve_dominice`, `tone_salve_dominici`
  - lauretanae: `tone_lor_genitrix`, `tone_lor_gratiam`, `tone_lor_postpartum`, `tone_lor_protege`
- `tools/proc/proc_data.py`: the block `# tones (prayers and versicles)` at the end (10 `_at` lines). Each chant goes just before its text item.
- Generator: `/tmp/gen/gen_tones.js`. It is outside the repo and may be lost. It is node: it loads `js/psalm.js` (OPPsalm.analyse) for syllables and accents, and it checks every sung text against the text items of proc_data.py, dumped to `/tmp/gen/texts.json`.

## Rules transcribed
The book is the Processionarium O.P. 1913, `/home/claude/dl/proc/p.pdf`. The pdf page is the printed page + 16 (not + 15 as the proc_data.py comment says). Both tones use the F clef on the 3rd line as printed (gabc `f3`), with the reciting note on h.

### Versicles: Art. II § IV 3°, pp. 395-396
The rule: "Subscripto modo dicantur Versiculi ad Memorias et ante Laudes, et in Processionibus, et quotiescumque dicitur ℣. a Sacerdote".
- Measured example: Di(h)gná(h)re(h) me(h) lau(h)dá(h)re(h) te(h) Vir(h)go(h) sa(h)crá(h)ta.(f) ℟. Da(h) mi(h)hi(h) … ho(h)stes(h) tu(h)os.(f)
- The syllables after the last accent fall to f. The book marks this place with the flexa sign.
- Words accented on the third-last syllable drop both following syllables (flexa, p. 402 "geminatur nota re").
- With alleluia, following the example "Dícite in natiónibus, allelúia" (p. 396): the words before stay on h, then a half bar `(;)`, then al(h)le(h)lú(h)ia(f).
- Same tone, a different ending (not used here): the "alia differentia" on p. 396, Angelis suis … ℟. Vitam æternam. Amen.
- p. 395 also has 1° (the melismatic versicle after hymns) and 2° (Triduum and the Office of the Dead). Neither applies to processions.

### Prayers: Art. III § III, pp. 407-408
The rule: "Orationes ad Horas, et quotiescumque aliae Orationes quae non sunt de corpore Officii et Missae". The Candlemas rubric on p. 66 also says "eo modo quo dicuntur Orationes ad Horas".
- **Dóminus vobíscum:** Dó(h)mi(h)nus(h) vo(h)bís(h)cum(f) ℟. Et(g) cum(g) spí(g)ri(g)tu(g) tu(g)o(h). This is the same as pur_dominus, which was already on the site.
- **Orémus:** O(h)ré(h)mus(f).
- **Body:** recited on h.
  - **Flexa** (the book's flexa sign): the syllables after the last accent go to f, e.g. tri(h)stí(h)ti(f)a(f).
  - **Metrum** (colon): the two syllables before the last accent go to g, the last of them to f; the accent and the rest are on h. It is three syllables when the third belongs to a word accented on its third-last syllable (count rule from p. 405 2°, the Mass tone).
    - Measured on p. 407: sa(h)lú(h)te(g) gau(f)dé(h)re(h); pér(h)fru(g)i(g) læ(f)tí(h)ti(h)a(h).
    - Conclusion on p. 408: san(g)cti(f) De(h)us(h).
- **Conclusions (p. 408):**
  - Per Christum Dóminum nos(h)trum(f)
  - Per Dóminum … Fílium tu(h)um(f) ‡ qui tecum … sancti Deus : per ómnia sǽcula sæculó(h)rum(f)
  - ℟. A(g)men(h), also given on p. 401 VII 2°.
- **The Mass tone is different** (Art. III § II, pp. 404-406): its flexa goes to g (mi), and its metrum puts every lowered syllable on g. Do not mix the two tones.
- Where to put the inflexions: follow the signs printed on the procession page itself (flexa sign and colon), not the site's punctuation. Their order follows p. 405 2° (metrum, flexa, metrum; with a longer prayer, flexa first).

### Paschaltide
Where the text says "(T. P. Allelúia.)", the file adds a second ℟ marked `<i>T. P.</i>` that ends ", allelúia" in the p. 396 manner. The ordinary ℟ ends without its own `(::)`, so that `stripTP` in js/chant.js still works. Adding the alleluia to the ℟ only is my reading of the book's line "Temp. Pasch. additur: Allelúia", which stands after the ℟.

## Open points (not mine to change)
1. **Ascension prayer text in proc_data.** It reads "…largiátur et nobis, Jesus Christus … Dóminus noster: Qui tecum vivit et regnat…". The book (p. 50) reads "…et nobis : Jesus Christus … noster, qui tecum vivit, et regnat … sæculórum ‡". The chant puts the metrum at "nobis", as the book does. The text line should be corrected to the book's punctuation.
2. **proc_data has ":" or "," where the book prints the flexa sign** (præsentásti, dignéris, venerári, tristítia, prémimur, cognóvimus, confidéntes). This is punctuation only; the chant follows the book.

## How to resume
Nothing is left in this scope. To notate further prayers or versicles in processions (e.g. those in the extraordinariae section, pp. 131-134, which belong to the litany agent):
- Apply the same two tones.
- Read the flexa signs and colons on the printed page.
- Note that versicles there that end on a one-syllable word are marked with ":" rather than the flexa sign (e.g. "Exsúrge, Dómine, ádjuva nos :", p. 133). The book gives no example of their ending, so leave those as text unless a rule is found.
