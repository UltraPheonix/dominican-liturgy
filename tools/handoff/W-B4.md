# W-B4: Good Friday 1939 orations, biddings and lessons in tone (stopped 27 Nov 2026)

## State
- 22 items are generated, compiled with gregorio and wired in with G: lines. `python3 tools/hw39/build.py` runs clean.
- holyweek.html#Quad6f&d=2027-03-26 (hwRite=1939) was checked in headless Chrome: no console errors, nothing undrawn, all 22 op-hw-quad6f-* drawn after scrolling (the chants draw lazily).
- Not committed.

## Files
- `tools/hw39/gen_quad6f.js`: the generator. It can be re-run, and it skips any G: line that is already there. Each .src is re-read right before it is edited.
  - `node tools/hw39/gen_quad6f.js [--gabc] [--compile] [--write] [--pointing=missal] [--questions] [--only=NN,..]`
- `gabc/op-hw-quad6f-01.gabc` to `-22.gabc` (new).
- G: lines inserted (only lines added, nothing else changed):
  - tools/hw39/Quad6f.src: 01, 02, 03
  - Quad6f_b.src: 04-21
  - Quad6f_c.src: 22
- Engine: js/mtones.js `OPMassTones.orationProc` / `lessonProc` (Lead B), with `pointing:'book'`.
- Words come from the Missal (.src). The inflexion marks come from the Triduum O.P. 1927 (/tmp/dl/tri.pdf, pdf page = printed/2 + 3), transcribed in the generator and checked word by word against the .src (a mismatch is reported as WORD DIFF).

## Inventory (Missal 1939 page / Triduum 1927 page / tone)
| # | Item | Missal | Tri. | Rubric | Tone |
|---|---|---|---|---|---|
| 01 | Prophecy Osee 6, Hæc dicit Dóminus | 166 | 179 | "legatur ... a fratre ... sine ullo titulo"; the Prior "legat submissa voce Prophetiam" | lesson IV, Proc. 408-413, end n. 11 |
| 02 | Deus, a quo et Judas | 166 | 181-2 | "absque Dóminus vobíscum, et absque Flectámus génua, præmisso tantum Orémus" (Orémus = op13-quad6f-oremus) | oration II, Proc. 404-406 |
| 03 | Lesson Exodus 12 | 167 | 182 | "legatur sine titulo, et in tono Lectionis" | lesson IV |
| 04-21 | 9 biddings + 9 Omnípotens prayers | 171-174 | 190-194 | "dicat sequentes Orationes, sine Dóminus vobíscum"; biddings "non respondeatur Amen" (Flectámus = op13-quad6f-flectamus; 8th: op13-quad6f-oremus) | oration II |
| 22 | Réspice (after Super ómnia) | 177 | 205 | "sine Dóminus vobíscum et sine Orémus"; Tri. adds "sicut dicitur ad horas hujus diei" and ends it with a flex sign | oration II, `final:'flex'`, no conclusion |
| (23) | Líbera nos | 178-9 | 209 | "Et immediate prosequatur Orationem"; no tone printed | OPEN, not generated |
| (24) | Quod ore súmpsimus | 179 | 210 | "dicat" (private ablution prayer) | OPEN, not generated |

Already notated, left alone: Orémus/Flectámus (op13-quad6f-*), Præcéptis + Pater and Per ómnia (op39-quad6f-*), the tracts, Pópule meus and the Adoration chants, Tantum ergo, Vexilla. The Passion belongs to Lead C.

## Open questions for main / Joseph
- Q1 **Pointing.** The Triduum 1927 pointing (used now) differs from the Missal's punctuation in:
  - Osee and Exodus: the verse divisions differ throughout.
  - Deus a quo: "sumpsit," is a comma in the Triduum, a ";" in the Missal.
  - Bidding 6 (pro necessitatibus): the Triduum has "omnipoténtem :" and "dissólvat :" where the Missal has commas.
  - Everything else matches.
  - Joseph's rule 3 says to keep the Missal's punctuation; Lead B said to use the Triduum's. `--pointing=missal` regenerates from the Missal's punctuation.
- Q2 **Réspice: tone II or III?** "ad horas hujus diei" could point to tone III, "Orationes ad Horas", Proc. p. 407. Lauds takes tone II. Tone II is used for now.
- Q3 **Líbera nos.** Neither the Missal nor the Triduum gives it a tone, and the rubric does not say "secreto". If it is to be sung in tone II: `--questions --only=23`. The conclusion ends at "...Deus." and Per ómnia (op39-quad6f-peromnia) follows.
- Q4 **Quod ore súmpsimus / Corpus Dómini.** These are private communion prayers. Suggest they stay text.
- Q5 **P3 conclusion.** It is sung as printed, "in unitáte Spíritus Sancti", without ejúsdem. The Missal rubric (Rubr., m39lin l. 7154) would add ejúsdem if "cujus spíritu" counts as a mention of the Holy Spirit.
- Q6 **Amen after Deus a quo.** The Missal p. 166 prints no ℟. Amen, but the gabc has the Proc. p. 406 conclusion with Amen.
- Q7 **"Juda" in Osee.** It is accented on the final syllable (Hebrew rule, Proc. p. 409), so the question cadence falls on "-da".

## Resume
1. Answer Q1-Q7.
2. Adjust the generator: the `pt` texts, `o` options, and the QUESTIONS set.
3. Run `node tools/hw39/gen_quad6f.js --gabc --compile --write`.
4. Run `python3 tools/hw39/build.py`.
5. Test in Chrome (/tmp/w4t/t.py scrolls the page to draw every chant).
6. Second pass: read each gabc against Proc. pp. 404-413 and the Triduum scan.
