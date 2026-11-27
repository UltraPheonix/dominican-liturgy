# Lead F (Site QC + Ordo 1944): stopped 27 Nov 2026 ~17:05, on main's order

Nothing committed. Every edit below is finished and was checked in headless Chrome (no console errors, nothing "could
not be drawn"). The full mass_sweep was NOT completed: the run on port 8768 stopped with a Playwright `Page.goto` timeout
(30 s) at case 147, `index.html?n=147#S0804&ordo=low&rub=full&sac=exp&prel=pope&serv=one`. Many agents were loading the
servers at the time. The same URL loads cleanly on 8765. **Re-run `timeout 590 python3 tools/check/mass_sweep.py` before
pushing.** It must print `cases 224 flagged 0`.

## Done (files)
- **W2, C1, C3: prayer labels.** In `js/app.js` `prayerOf`, only the ADDIV title line was changed. The label now names
  the intention in lower case, with no incipit and no "(n. 38)", e.g. "2nd prayer · of Our Lady" and "3rd prayer · for
  the living and the dead". The lines for commemoration titles (`m:`/`x:`, owned by Lead E) were not touched.
  `moreText`/`drawMore` now take the ordinal from `NTH`, so a 4th prayer is no longer called "3rd".
- **W3: solemn Requiem entrance.** In `tools/rubrics/ordo_directions.py` (which rebuilds `data/ordo.js`), the two
  "Gloria Patri of the Introit" lines are now `!req`. Two `req` variants were added: "When the choir begins the verse Te
  decet of the Introit (there is no Gloria Patri)…". Ministri III.3 says "vel Versu, si Gloria Patri non dicitur".
- **W4: verified, not a bug.** The Missal, Ritus "De his quae omittuntur in Missa pro Defunctis" (m39lin ~5190), omits
  only the priest's "Dominus sit in corde meo" and says "Alia omnia serventur, ut in aliis Missis". The deacon's Jube
  domne and Dominus sit in corde tuo therefore stay.
- **W15: "server" at Low Mass.** In `ordo_directions.py`, the Confiteor repeat, "alternately with the server" and "The
  server answers Gloria tibi Domine" now have `m:'l'`, and the "ministers" forms have `m:'smc'`. The exposition line
  now reads "(the server or ministers with him)".
- **W17 and C9.** In `js/app.js` `drawPreface`, there is no "tono feriali/solemni" label when `state.ordo==='low'`, and the
  line "Sanctus, Sanctus, Sanctus…" shows only when the Order of Mass is off (`!state.ordo`). W-F2 knows that these are
  done.
- **W7: one name for the Requiem.** `tools/requiem/build.py` now titles C114s "Missa pro Defunctis (conventualis)" /
  "Conventual Requiem for the brethren, relatives and benefactors". The build was re-run, and in `data/masses.js` only
  the C114s title and en changed. The booklet picks up the new name.
- **W5: the four Anniversaries (S1113), three prayers** by Rubr. XII.7, confirmed by the Ordo 1944 on 4 Feb, 12 Jul,
  5 Sept and 10 Nov (o44.txt lines 946, 5876, 7046, 8732). The 1st prayer is Deus indulgentiarum (pl.) and the 3rd is
  Omnipotens (d38). The 2nd varies:
  - February (Patrum et Matrum): `defPM`, Deus qui nos patrem.
  - July (sepultorum in Coemeteriis): `defMis`, "Deus, cuius miseratióne", Orationes diversae pro Defunctis n. 9, p. 124*
    (M39.pdf page 430, left page). Latin read from the scan, including "benígnus oblátam" in the Secret. The English is
    labelled as an AI translation.
  - September and November: `defFr`, Deus veniae largitor in the Order's form, from "In Missis quotidianis, Secunda
    Oratio", p. 119*.
  - Files:
    - `tools/requiem/build.py` adds the ADDIV sets `defFr` (no longer popped) and `defMis`, and the build was re-run
      (`data/addiv.js`).
    - `js/app.js`:
      - `moreAllowed` allows S1113.
      - `prescribed0` has an S1113 branch, using the new `annivOf(d)`.
      - The Mass header shows the Kalendarium's own Anniversary title, with English such as "Anniversary of our fathers
        and mothers".
      - `drawDayAlts` shows an anniversary chip's own title.
  - The ruling taken: XII.1 ("una tantum Oratio") gives way to XII.7, because the Ordo 1944 gives three prayers.
- **C10: the second conventual Mass chip.** In `js/mrank.js`, the anniversary labels are now "Second conventual Mass
  (sung)" and "The one conventual Mass", with `title:` set to the Kalendarium title. Before, the label ran on as
  "…sung: Anniversarium…: Anniversarium Omnium…".
- **W6: Omnipotens when no Requiem day.**
  - `js/mrank.js`:
    - `requiemDay` is split into `requiemExempt(ws)` plus `requiemDay`.
    - The new `omnipotensDay(d)` is exported. When the week is not exempt and has no free day, it returns the weekday
      (Mon–Sat) with the lowest office pv.
  - `js/app.js`: `prescribed()` appends `d38` on that day, to the day's conventual Mass (`mr().day(d).win`).
  - **Open question for Joseph:** Rubr. VI.2 says only "alia hebdomadae die, minus solemni". "Lowest rank, first if
    equal" is my reading of that. The Ordo 1944 never names such a day, and it marks "add. Or. Omnipotens" only on the
    Anniversaries. The rule fires in 35 weeks of 2026-27, mostly in Lent, octaves and Advent; the list can be printed
    with `node -e` via /tmp/mr.js and `omnipotensDay`.
  - Not modelled: "Ubi Missa Anniv. cantari non potest, unica Missa de festo … add. Or. Omnipotens" (a choice for the
    house).

Tested pages:
- S1113 on 2027-02-04, 2027-07-12, 2027-09-06 and 2026-11-10.
- C114s on 2026-11-27, at low and at solemn with `rub=full`.
- S1208 on 2026-12-09 (W6).
- S1129v on 2026-11-28 (labels).
- `booklet.html?b=choir#C114s&d=2026-11-27`.
- S0804 with the full-rubric variant.

## Not done / next (resume steps)
1. Re-run mass_sweep on 8768 (see above).
2. **Apply W-F3's list: `tools/handoff/ordo44_diff.md`** (Jan–Nov checked; Dec not yet). It is grouped by cause A–N, with
   file, function and fix; the raw notes are in /tmp/wf3/notes.md (copy in scratch/wf3). The main causes:
   - `prescribed()` takes the rank from the feast's Kalendarium entry, not from the day's office (octave days, EpiOct,
     Pasc2w, Nat2).
   - From Septuagesima to Lent the 3rd prayer is A cunctis (Deus qui caritatis only in place of the ad libitum).
   - The Lent Sundays and Holy Week ferias need the Missal's "2-a et 3-a Or." (temporalClass 1 returns mem only).
   - Sundays get a 4th prayer, A cunctis, after two memoriae (Lauds suffrage).
   - A feast transferred off a Sunday is wrongly commemorated on that Sunday (mrank commems).
   - VIII.2 is applied too strictly: memoriae of Semiduplex feasts are marked privateOnly at II-class and temporal
     Masses.
   - Quad5f on 31 Mar is Compassion BVM (white, Credo, Pf BVM), not a feria (`ownFeriaMass` regex).
   - Pf. Apostolorum on the feasts of the Apostles (Conversion of St Paul, Cathedrae).
   - Kyriale by the G28 headings: Paschaltide IV for the whole Ordinary; 3 Lect. = VII; Maundy Thursday II.
   - Jan5a is white, with Gloria and no Credo (Missal p. 31).
   - The Pentecost vigil has one prayer and no Credo.
   - AscVig is violet with a commemoration of the Rogations.
   - Simplex memoriae are dropped within the Ascension octave.
   - The resumed Sunday (Rubr. IX.2): Gloria when there is a Te Deum, and the choir/extra-choir pair.
   - Missa votiva S. Thomae on Wednesdays in Paschaltide (Rubr. V.1).
   - The 25 Apr / Rogations single-Mass form.
3. **Rulings received (Joseph, via main):**
   - Keep the PROPER Prefaces from the Missal's inserted leaves (St Thomas p. 137, Sacred Heart p. 135 and the like).
     Do not switch them to the Lent/Nativity Prefaces that the Ordo 1944 gives.
   - The Vigil of St John: the common form.
   - A Sunday within the Sacred Heart octave: the Nativity (as relayed by main).
   - Everything else W-F3 finds: fix by the Missal 1939 plus the Ordo 1944.
4. **W-F2's items** are in `tools/handoff/W-F2.md`. W-F2 touched `js/app.js` in `paschalKyrie` (~763), the Kyrie hint
   (~1937), `massesOf` (~2224) and `dayRankLabel` (~2238). It covers W9 (verified, no change), W11 (fixed), and the rest
   of W10-W18, K1/K2 and the non-label C items, as its note records.
5. C2 (the verbose ad-libitum picker) is untouched. It belongs to the non-label C items (W-F2).

## Files touched by Lead F
- js/app.js: `prayerOf` (ADDIV title line only), `moreAllowed`, `prescribed`, `prescribed0`, `annivOf` (new), `NTH`/`moreText`/`drawMore` labels, `drawPreface` (2 lines), `drawMass` header (S1113 block), `drawDayAlts`
- js/mrank.js: `requiemExempt`/`requiemDay`/`omnipotensDay`, anniversary labels, export
- tools/rubrics/ordo_directions.py → data/ordo.js
- tools/requiem/build.py → data/addiv.js, data/masses.js (C114s title/en only)
- tools/handoff/F.md (this note)
