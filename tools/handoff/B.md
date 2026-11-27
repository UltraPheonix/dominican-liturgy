# Lead B: Holy Week 1939 tones (stopped 27 Nov 2026, swarm cut)

## State in one line
The tone engine (Proc. 1913) is DONE, tested and in js/mtones.js. Good Friday is wired in (W-B4, 22 gabc). Palm Sunday-Wed
has 26 gabc generated but NOT wired (W-B2). Thursday (W-B3) and Saturday (W-B5) have inventories only. Item-6 QC was
done by W-B6 (reviewed by me, see below). Nothing committed.

## 1. The engine (js/mtones.js, block appended at the end; the Harrison functions above it are untouched)
Source: Processionarium O.P. 1913, Art. III, pp. 402-430 (/home/claude/dl/proc/p.pdf, pdf = printed + 16), read at 150-300
dpi. All return GABC beginning `(f3) `. Text: pass the Missal words as printed; `plain()` drops `{}()[]^*✠`, † ‡ become the
flex (";"). Old browsers: no regex lookbehind used.
- `OPMassTones.orationProc(text, {tone:'mass'|'hours', dv, oremus | noOremus, amen=true, flectamus, pointing:'book', final:'flex'})`
  - 'mass' = tone II pp. 404-406 (flexio to MI, elevatio, conclusions p. 406); 'hours' = tone III pp. 407-408 (blessings,
    processions, absolution, altar of repose).
  - Without `pointing` the inflexions alternate back from the final elevatio (p. 405, 2°). `pointing:'book'`: ";"/† =
    flexio, ":" = elevatio (to follow Proc. pp. 20-21 / Triduum 1927 pointing). `final:'flex'`: no conclusion, ends on a
    flexio (Respice, Triduum p. 205).
  - Expands the Missal's short conclusions (Per Dóminum. / Per Dóminum… / Per eúmdem. / Per eúmdem Dóminum. / Qui tecum
    vivit. / Qui vivis. / Per Christum. / Qui vivis et regnas per ómnia.) in the Proc. p. 406 / 408 form. "ejúsdem" only if
    the prayer names the Holy Spirit (Missal rubric, m39lin l.7154) or the Missal prints it; "Per Dóminum… in unitáte
    Spíritus." keeps what is printed (Good Friday p. 172 set WITHOUT ejúsdem — question sent to Joseph via main).
    A conclusion written out to "…Deus." gets no Amen (Per ómnia follows in the Preface tone).
- `OPMassTones.lessonProc(text, {title, pointing:'book'})` — IV pp. 408-413: flex, mediation, termination to LA,
  questions (n. 9), speech colons (dixit/ait… : + capital) end a verse (n. 6), the last verse by n. 11 (p. 413).
- `OPMassTones.readingProc(text, gospel)` — drop-in for `reading()`: Epistle V pp. 414-419 / Gospel VI pp. 424-426.
  `epistleTitleProc(title)` drop-in for `epistleTitle()`. `epistleProc(text, {title})`, `gospelProc(text, {book, dv})`.
  `sequentia(book)` (old) is identical to Proc. p. 424 (checked).
- Proc vs Harrison differences implemented: Hebrew final accent (HEB table; Jerúsalem forced final, p. 418/425); a final
  monosyllable takes the cadence alone (p. 418 Dóminus est., p. 425 Non sum.); accents before the penultimate accent of a
  mediation stay FA, only the unaccented run before them goes RE (p. 425 Hosanná fílio David); secondary accent on a long
  last word of a mediation (p. 415, p. 424 E-van-gé-li-i); a 3-syllable Hebrew name at a mediation end has two accents
  (Néphta-lì p. 415); a preposition before a one-accent last word takes an accent (p. 416); the final modulation has
  RE-FA (fh) on the last accent before the pause (pp. 419, 426); monosyllables other than prepositions/conjunctions are
  accented (pp. 411, 414, 418, 426); "ii" and accented vowel + vowel split (á-bi-i, I-sa-í-æ), áu/éu kept.
- After the stop (Lead H's report): a written-out conclusion is sung as the p. 406 formula whatever the source's commas
  ("tuum,/tuum:/Patre," → flexio, "Sancti, Deus," → elevatio, ", per ómnia"); a conclusion run into the prayer ("…Fílium
  tuum: qui tecum vivit…", no "Per") is recognised (CONCL2) and the body ends on the flexio. Checked on all 1416
  orations in data/orations.js (only 2 Secrets with "qui cum eódem Deo Patre…" not recognised; Secrets are not sung).
- Heuristic (no printed rule): where the final modulation's "brevis pausa" falls when there is no comma: last 2 words (+ a
  preceding monosyllable). Juda is final-accented by the general Hebrew rule (no printed example).
- Tests: `cd tools/hw39 && node test_mtones.js` → `105 / 105 ok` (every printed example of pp. 404-426, note by note).
  Site check: index.html (sung/solemn) and holyweek.html all 7 days, headless Chrome: 0 console errors, nothing undrawn.
- Lead H (Mass page) was given this API and is wiring orationProc into app.js line ~1704 (its code, not mine).

## 2. Days (worker notes have details: W-B2.md, W-B3.md, W-B4.md, W-B5.md)
- Palm Sunday-Wednesday (W-B2): `tools/hw39/gen_quad6.js`; 26 gabc compiled (op-hw-quad6-1..6, quad6m-1..9,11,
  quad6t-1,2,3,5, quad6w-1,2,4,5,6,8), NOT wired. I read the headers; inventory/rubric citations look right. To finish:
  regenerate (engine changed after their run: `node tools/hw39/gen_quad6.js --write`), second pass against Proc/Missal,
  then `--insert`, build, Chrome.
- Thursday (W-B3): nothing generated. Finding to act on: per Triduum p. 123 only the Gospel *Ante diem festum* is in the
  Gospel tone; the rest of the Sermo Domini is "in tono Lectionis" (lessonProc), ending without Tu autem. The Sermo text
  in Quad6h_mand.src is the site Bible, not the Triduum text: retranscribe pp. 122-130 first (OCR in scratch/w-b3/).
- Good Friday (W-B4): DONE and wired (Quad6f.src 01-03, Quad6f_b.src 04-21, Quad6f_c.src 22), generated with the final
  engine (17:02), compiled, built. I spot-checked 01 (Osee, lesson tone) and 02 (Deus a quo, tone II) note by note against
  the Proc rules: correct.
- Holy Saturday (W-B5): inventory and questions answered by main; nothing generated. Note: the 1939 rite has no separate
  blessing of the grains or candle (inside the Exsultet, p. 180); font blessing Preface in the Missal App. Preface tone.

## 3. Item-6 QC (done by W-B6, reviewed by me in code)
Palm Sunday rubric split at "fiat Processio :" (p. 139); Thursday either/or note (p. 165); Saturday Litany one invocation
per line; HOLYWEEK 1959 data gated on hwr; 1939 Canon proper texts printed once; Saturday header Kyrie IV / Gloria II
(Triduum p. 281). DROP the qc_hw item "tríbulor. inclína → colon": the Missal p. 155 (pdf 111) prints the full stop.
Left for Lead C (not mine): John Passion English "When Jesus had said these things", "POST hæc autem" paragraph (p. 170).
Not done: confirm Tuesday's chants (6359/7181/5409) are G28 melodies.

## 4. Files I touched
js/mtones.js (appended block only), tools/hw39/test_mtones.js (new), data/holyweek_text.js (rebuilt by build.py),
tools/handoff/B.md. Backup of the pre-change mtones.js: none needed (diff = pure append + nothing above changed).

## 5. Resume
1. `cd tools/hw39 && node test_mtones.js` (expect 105/105).
2. Days in order: W-B2 (wire after second pass), W-B5 (write gen_quad6s.js on the model of gen_quad6f.js), W-B3 (Sermo
   text first). Each: generate → `cd /tmp && gregorio -o x.gtex /abs/gabc/op-hw-*.gabc` → second pass against the scan →
   insert G: lines → `python3 tools/hw39/build.py` → headless Chrome (python3 tools/handoff/scratch/lead_b_pw.py style: hwRite=1939, scroll,
   open folds, 0 errors, no "could not be drawn").
3. Hand up READY to main with the file list.

## 6. From W-B6 (after the stop): keep these when inserting G: lines
- app.js hides (when the Order of Mass is on) a G block whose id contains dv/vobiscum/oremus placed immediately before or
  after "L: Postcommunio": put the Postcommunion Dóminus vobíscum · Orémus G: lines there.
- Quad6s.src markers changed: X: offerNoOff, offertoryNoOff (p. 188); X: canonPater + X: communion after the Pax rubric;
  Litany one T per invocation. Quad6f_c.src: C: ad 0 replaced by G: op-hw-improperia-1/2/3/agios per verse (files exist,
  build OK). Don't overwrite these lines.
