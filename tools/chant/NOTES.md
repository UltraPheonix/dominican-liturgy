# Chant for the Office: state of work (18 Nov 2026)

## Live on the site
- Office page: **Chant** switch (`#chant`, localStorage `officeChant`). Antiphons, hymns and short responsories
  are drawn from `data/chant/op/<gregobase id>.gabc` via `data/chant/office.json`
  (`{key: [id, mode, keepTP, wholeHymn]}`; key = letters-only lower-case text, `hy`/`rb` prefixes;
  same function in `js/chant.js` `OPChant.key` and `tools/gregobase/build_chant.py` `key`).
- Renderer: `js/chant.js` (exsurge, same context as the Mass page).
- Hymns whose GregoBase GABC has only the first stanza: that stanza is notated, the rest stays as text.

## Sources, in order of priority (user's decision)
1. **GregoBase** Dominican books (dump: github.com/gregorio-project/GregoBase, `gregobase_online.sql`):
   AOP1933 (Antiphonarium, Gillet), MOP1936, COP1949, POP1913, HSOP1965, GOP1950, Jandel 1862.
   `tools/gregobase/load.py` → gb.sqlite; `index.py` → gb_op.json; `build_chant.py` → site/data/chant.
   Coverage (day hours): antiphons ~60%, hymns ~95%, short responsories ~73%.
2. **Fr Thompson's Antiphonale** (Drive folder "Antiphons": a1, a2a, a2b, a3, a4). Typeset with chant
   fonts → decoded straight to GABC, no OCR:
   - `gtable.py` (all glyph outlines, all volumes) → `glyphs_all.json`
   - `gclass.py` + `ganalyze.py` (outline → notes/clef/flat/bar by geometry; staff lines at y=0,168,336,504,
     pitch = round((y-5)/84), 0 = gabc d) → `gclass.json`
   - `decode.py <book>` → items_<book>.json (systems + text lines; not in repo, ~50 MB each, regenerate)
   - `assemble.py <book>` → `pieces/pieces_<book>.json` (6,300 pieces: ctx headings, mode label e.g. "VIII b",
     GABC). Hollow notes = `r`, accent marks = `'` (psalm-tone first verses after `<i>Ps.</i>`/`<i>C.</i>`).
   - NB: Thompson is laid out for the post-1970 Liturgy of the Hours; use it for melodies/tones only.
3. Uploaded scans (image only): Antiphonarium 1933 (1,290 pp: Toni communes pp. 1–17: incipit, Gloria
   Patri of responsories, versicles, solemn canticle mediations, Benedicamus by class, Alleluia per mode,
   hymn-tone rules p. 14–15), Matutinum 1936, Hebdomada Sancta 1959.
4. **Regulae Cantus O.P. 1965** (uploaded, OCR'd): THE source for psalm tones and their adaptation
   (Solesmes accent method: preparatory notes, accents ', one superveniens hollow note after a dactyl),
   differentiae and the rules for choosing them from the antiphon's first note, versicle/chapter/oration/
   lesson tones, and Compline fully pointed (pp. 65–102).

## Psalm tones transcribed so far (Regulae Cantus pp. 13–29; c4 unless noted; ' = accent, r = superveniens)
- I: inton `f gh`, tenor h, flex `'h gr g.`, med `'ixi hr h 'g hr h`;
  D `g f 'gh gr gFED.`; g `g f 'gh gr g.`; a `g f 'g hr h.`
  Usage: D if ant. begins on c grave, or on f moving below; g if it begins on d, or f→c→d→a; a if on a, or f then e d / leap to a.
- II (f3): inton `e f`, tenor h, flex `'h fr f.`, med `'i hr h`; D `g 'e fr f.`
- III: inton `g hj`, tenor j, flex `'j hr h.`, med `'k jr j 'i jr j`; a `h 'j jr ih.`; a2 `ji hi 'h gr gh.`
  Usage: a unless the antiphon begins on e grave (then a2).
- IV: E and A (p. 20–21), V: a (p. 22), VI: F (p. 23–24), VII: a, d (p. 24–26), VIII: G, c (p. 26–27),
  peregrinus (p. 28–29), tonus in directum (p. 29): still to transcribe from the page images.

## Still to do
1. Finish the tone table above; write the pointing engine (accents from the acute marks of the Office text,
   rules art. I §§ II–V) and render: tone notated once (first verse), then pointed text (user's choice).
2. Differentia per antiphon from its first note (usage rules), unless Thompson/GregoBase gives one.
3. Fill missing antiphons (ferial psalter, Compline) from Thompson pieces (match by text) and from the
   Regulae Compline pages.
4. Incipit (Deus in adiutorium), versicles (tonus solemnis/simplex), chapter, collect (flexio/elevatio,
   conclusion), Benedicamus by class (AOP1933 I–VII on GregoBase ids 4206, 4227, 7984–7994; rubrics in
   Antiphonarium 1933 p. 11–13), Salve Regina etc.
5. Matins: everything but the lessons (invitatory with Venite tones, responsories, absolutions, Te Deum).
