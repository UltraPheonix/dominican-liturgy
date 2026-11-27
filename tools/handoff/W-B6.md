# W-B6: Holy Week QC fixes (qc_hw.md, README item 6), 27 Nov 2026

Status: all items done and tested. Nothing was committed.

## Files touched
- tools/hw39/Quad6.src: l.40 split at "fiat Processio :"; new R line "Qua finita… procedant more solito ad altare" at the head of Ad Missam (p. 139).
- tools/hw39/Quad6h.src: "Si vero prius Vesperæ dicantur…" is now its own paragraph, as in the Missal. Added an I: line "Si vero prius Vesperæ dicantur, antequam Missa terminetur (pag. 165) :" with English, before "Stetque in eodem loco", to mark the either/or ending.
- tools/hw39/Quad6s.src:
  - The Litany has one invocation per line (141 pairs). "Repetatur a Choro Pater de cælis" is now an R line, and the 3rd Kyrie's English ℟ was added.
  - `X: offer, offertory` became `X: offerNoOff, offertoryNoOff` (p. 188).
  - `X: canonNoAg` became `X: canonPater`, and `X: communion` was added after the "Postea dicente Sacerdote Pax Domini…" rubric (pp. 189-190; Triduum p. 285 "facto modico intervallo").
- tools/hw39/Quad6f_c.src: `C: ad 0` was replaced by per-verse G lines (op-hw-improperia-1, -2, -3), and op-hw-improperia-agios goes after the Agios and after each "Agios… etc." rubric.
- tools/hw39/joannes_parts.txt and joannes_en.txt:
  - "^POST hæc autem…" is its own paragraph (p. 171 scan: large initial). "Erat autem in loco…" is joined to it, as the Missal prints them.
  - The English begins "Jesus went forth…"; "When Jesus had said these things" was dropped.
  - Already gone before this pass: Ítaque/Íterum, the stray "1", and "Dicit"→"Dixit".
- gabc/op-hw-improperia-1.gabc, -agios.gabc, -2.gabc, -3.gabc (new): split from gabc/9867 (G50 p. 176) and read note by note against Graduale O.P. 1928, pp. 176-178. Two G28 corrections:
  - verse 2 "Qui-a": "a" is on D, not C.
  - verse 3 "potásti": "po" is on D, not F.
  - 9867 itself was not changed.
- data/holyweek_text.js: rebuilt with `python3 tools/hw39/build.py`.
- js/app.js (Holy Week paths only):
  - massSequence: HOLYWEEK skipChants is read only when hwr !== '1939'. New X markers: offerNoOff, offertoryNoOff, canonPater. With the ordo on, the 1939 "Infra Canonem" blocks are hidden, together with any Postcommunion DV/Oremus G block (id contains dv, vobiscum or oremus, placed next to "L: Postcommunio"), following Joseph's ruling.
  - drawOrdo(k, R, it):
    - The 1959 HOLYWEEK data is read only in the 1959 form. The 1939 form uses HW39 (lastGospel Mt 21:1-9, p. 146; alleluiaDismiss, p. 190).
    - The Canon takes Communicantes / Hanc igitur / Qui pridie from HW_TEXT via hwCanon39(); Qui pridie = the proper opening + the Canon's words.
    - On Thu/Sat the "Pax tibi" / pax lines are dropped (pp. 163, 190).
    - With noOff, the Offertory rubric lines are removed.
  - drawMass passes `it` to drawOrdo.
  - rubricLine: the Holy Saturday header now reads "Kyrie IV · Gloria II (Triduum p. 281) · no Credo · Preface of Easter · Sanctus I · no Agnus Dei · Ite, missa est, alleluia, alleluia".

## Tests (headless Chrome, hwRite=1939, Propers / Solemn / Low)
- All 7 days were checked: no console errors, nothing reported "could not be drawn", and every chant on Fri/Sat/Thu drew after scrolling.
- With the ordo on, Thursday and Saturday show Communicantes, Hanc igitur and Qui pridie once each.
- Saturday order: canon, then Pax rubric, then communion, then Vespers. The Offertory rubric now reads "the Offertory is not said".
- On Palm Sunday at Low Mass, the last Gospel is Cum appropinquasset.

## Open questions for main
- The Holy Saturday Sanctus. The Missal (p. 188) and the Triduum (p. 284) only say "dicatur Sanctus", so the page sings Sanctus I by the 1st-class rule. Is that right?
- Tuesday chants: confirmed in G28 itself. On p. 161, "Feria III. Hebdomadæ Sanctæ: Officium Nos autem, ut in Feria V. pag. 169", followed by:
  - Resp. Ego autem (mode IV), p. 161;
  - Off. Custodi me (mode I), pp. 162-163;
  - Comm. Adversum me (mode V), p. 163.
  These are the gabc 6359/7181/5409, with the same pages, modes and texts. Melodic openings were spot-checked; there was no full note-by-note pass. The masses.js note ("found by the incipits… in the Roman Graduale") is misleading, and Lead D could change it to "Graduale O.P. 1928, pp. 161-163".
- Lead B says to keep "tríbulor." as printed (p. 155); it was not changed.
