# Lead H: every sung prayer in its proper tone (README item 11b), 27 Nov 2026

## State
The work is finished and tested, and nothing is committed.
- `timeout 590 python3 tools/check/mass_sweep.py` printed `cases 224 flagged 0`.
- Headless Chrome showed no console errors and no "could not be drawn" on these pages:
  - index.html: Adv1 (solemn), Quad2m (sung, Super populum), EmbSatSept (conv, 5 prophecies), C114s (Requiem), Pasc0t (solemn), S0807 (sung and low), Pasc2 (Vidi aquam).
  - booklet.html: choir and priest for Adv1, Pasc2 and Quad2m.

## Files touched
- **js/app.js** (only the regions named here):
  - **New `tonePrayer(la, oremus)`:** uses `OPMassTones.orationProc` (Proc. 1913 pp. 404-406, mass tone, without pointing:'book', as Lead B advised). Falls back to Harrison `oration`.
  - **New `toneReading(la, r, pro)`:**
    - Gospel: `readingProc(la, true)`, the body only. DV and Sequentia stay in the Order of Mass (singLines).
    - Prophecy (pro): `lessonProc` (Proc. p. 408, IV "Prophetias in Missa").
    - Epistle, or a lesson in the Epistle's place: `epistleTitleProc` + `readingProc` (p. 414, "et in similibus").
  - drawOratio and drawMore now use tonePrayer.
  - **Flectamus day, sung:** chant plus English. The doubled Latin text line is gone.
  - **Super populum, sung:** Orémus (op-h-oremus, Proc. p. 405), then op-m39-humiliate, then the prayer.
  - drawReading(r, pro) uses toneReading. drawMass passes `it.pro`.
  - **massSequence:** the two `q.push({t:'read', r:r})` calls in the lessons loops get `pro: i < pre.length - 1`. That is the only change there.
  - **drawAspergesPrayers:**
    - Sung forms use the new gabc below.
    - Text corrected to Missal p. 33: "Dómine exáudi" (no comma) and "habitáculo: Per Christum".
    - The rubric hint cites pp. 33 and 40.
  - **ProprOP exports:** aspergesGabc, tonePrayer and toneReading.
- **js/booklet.js:**
  - Priest book: orations go through `A.tonePrayer`, readings through `A.toneReading` (with `it.pro`).
  - **New `aspergesUnits(priest)`:** on Sundays (`ORD.as`, not at Low Mass) the choir and priest books open with the Asperges or Vidi aquam (aspergesGabc picks the day's verse), then the versicles and the prayer in chant (Joseph's ruling).
- **New gabc files** (all compile with gregorio):
  - gabc/op-tone-asperges-v.gabc
  - gabc/op-tone-asperges-v-tp.gabc
  - gabc/op-tone-asperges-or.gabc
  - The versicles use the tone "quotiescumque dicitur ℣. a Sacerdote" (Proc. pp. 395-396). Paschaltide allelúia follows the p. 396 example.
  - The prayer uses tone III (pp. 407-408), with the pointing read from the Missal scan p. 33 (pdf 34). Its rules were checked on the scans of pp. 407-408.

## Verified against the scans (no change needed)
- Missal Appendix (M39 pdf 460-462): op-m39-pater-solemn, op-m39-pax and the ferial Preface dialogue match note by note.
- The special Benedicamus on p. 33 (Advent Sundays, Dec 24, Septuagesima to Holy Thursday Sundays, Holy Innocents) equals 7303 (G50 p. 135*). The site uses it on those days.
- 7339 (DV) and op-h-oremus match Proc. pp. 404-405.

## Open
- 163 of 472 Masses in data/orations.js (src Tempora/…, Sancti/…, Commune/…) still have Divinum Officium punctuation, not the 1939 Missal's (e.g. Adv1).
  - The tone pointing therefore falls back to the p. 405 alternation rule.
  - Re-punctuating them from the scans is a text job (reported to main).
- The first Secret with more prayers following shows "℟. Amen." This is unchanged and is text, not sung.
