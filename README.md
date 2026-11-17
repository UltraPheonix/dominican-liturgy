# Propria Missae O.P.

The sung propers of the **Dominican Rite Mass**, drawn in square notation for any day of the year, from the
*Graduale juxta ritum Sacri Ordinis Praedicatorum* (1950). It is a Dominican version of the Propers tool of
[bbloomf/jgabc](https://github.com/bbloomf/jgabc).

- Pick a date (or *Today* / *Next Sunday*) to get that day's Temporale Mass and the feasts of the Dominican calendar.
- Or pick any Mass: Proper of the Time, Proper of the Saints, Dominican Blesseds, Commons, votive Masses and the Requiem.
- Swap any chant for another from the Graduale, edit its GABC live, add chants, and share the result as a link.
- *Print / PDF* gives an A4 choir sheet.

## Run it

It is a static site with no build step and no server code.

```sh
python3 -m http.server 8000     # then open http://localhost:8000
```

**GitHub Pages:** Settings → Pages → *Deploy from a branch* → `main` / root. The site appears at
`https://<user>.github.io/<repo>/`.

## Layout

| Path | What it is |
|---|---|
| `index.html`, `style.css`, `js/app.js` | The page: Mass selection, date lookup, chant rendering, editing, print |
| `js/exsurge.min.js` | The chant engraver used by jgabc |
| `data/masses.js` | Every Mass and the GregoBase IDs of its chants (generated) |
| `gabc/<id>.gabc` | The 975 chants of the Graduale O.P., from [GregoBase source 14](https://gregobase.selapa.net/source.php?id=14) |
| `tools/` | The scripts that build `data/masses.js`, with their sources |

## How the data was built (`tools/`)

```sh
cd tools && sh build.sh
```

1. `build_temporale.py` groups the Graduale's chants into Masses (each Introit starts one) and aligns them with
   jgabc's Roman Temporale by Introit. Days where the Dominican Mass differs are listed by hand in `MANUAL`.
2. `parse_calendar.py` reads the *Calendarium O.P. reformatum* (1960): date, feast and rank.
3. `align_sanct.py` matches the proper Masses of the Sanctorale to dates in the *Missale O.P.* (1939, OCR text).
4. `build_masses.py` assembles each Mass:
   - For a Common, it takes the Missal's *Officium …, ut in Communi* reference.
   - Failing that, it chooses a Common from the saint's title.
   - It finds chants the Graduale only refers back to by their incipit.

Each Mass records how its chants were found (`conf`), and the site shows this as a badge.

**Corrections:** fix the rule or add a line to `MANUAL` / `GUESS`, run `build.sh`, and commit `data/masses.js`.

### Known gaps

- 129 saints' days take a Common chosen from the saint's title. These are marked *Common: check Ordo*.
- Proper chants a saint shares with a neighbouring feast appear under *Other chants printed on these pages*, not
  in the Mass itself.
- The Alleluia *Laetatus sum* (p. 5) has not been transcribed on GregoBase.
- Holy Saturday chants are not in the GregoBase source.
- Precedence (Sunday vs. feast) is not computed.

## Credits and licence

- The code is released into the public domain (see `LICENSE`), as jgabc is.
- exsurge © Fr. Matthew Spencer, MIT licence.
- Chants transcribed for GregoBase by the volunteers named in each file.
- Source books: [Dominican Liturgy](https://dominican-liturgy.blogspot.com/).
