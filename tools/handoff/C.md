# Lead C (Latin Passions, README item 11): paused 27 Nov 2026 by Joseph's decision (save credits)

## State
- Nothing wired in, nothing generated, no gabc written. No existing file changed.
- New files: tools/passion/TONES.md (every tone read so far, note by note, with pages and rules quoted),
  tools/passion/words.py (measures the x-extent of printed syllables, to tie text to notes).
- No Agent tool was available in this session, so no workers were spawned; the lead did the reading itself.

## Read (Processionarium O.P. 1913, pdf = printed + 16)
- pp. 435-439 complete and checked by eye at 2-4x zoom: Chronista (mediation, final, before Christ, before turba,
  before a clamor, clamor/death/end), Christus (incipit, mediation, final, 3 later incipits, interrogation,
  Ego sum, Tu dixisti, Sitio, Eli Eli in two forms, Hoc est / Deus meus, Consummatum est, Pater in manus),
  Turba (mediation, final, interrogation + comma flexio, Tu videris, Non sum, Barabbam, Tolle tolle).
- p. 440 NOT finished: "crucifige eum. Crucifigatur." (raw reader output only, clef unconfirmed) and the
  Lamentation-tone ending "Altera autem die ... custodibus" (not read).

## Questions for Joseph: ANSWERED 27 Nov 21:50 (see RULINGS.md). Q1 yes; Q2 ALWAYS the full incipit (Scitis), not the proposal; Q3 flat in finals and before Christ, natural in mediation; Q4 yes (<6 syllables); Q5 yes (divisio minima).
## (original questions)
1. Chronista final with a dactyl ("Dóminum"): the book prints only spondees (p. 436). Proposed Dó(g) mi(f) num(ed).
2. Christus later sentences: the book gives three incipits that "possunt" be used (p. 437: Opus / Jam / Mittens).
   Which one when? Proposed: monosyllabic first word -> Jam; otherwise alternate Mittens/Opus; full incipit
   (Scitis) at the start of each speech.
3. Chronista B flat: printed in "Secúndum Matthǽum" and before "discípulis", not in "Discípulis suis" (p. 436)
   nor in the mediation (p. 435). Proposed: flat in every final and before-Christ cadence (as Fr Smith), natural
   in the mediation.
4. "nisi in brevioribus" (p. 435): no length given. Proposed: no mediation when the member has < 6 syllables.
5. The short stroke inside melismas (Voce ma-|gna, Trá-|didit, Con-|tra, Scitis|, má-|tum): rendered as a
   divisio minima, as Fr Smith does.

## How to resume
1. Finish p. 440: `cd /tmp/pt && pdftoppm -r 400 -f 456 -l 456 -png /home/claude/dl/proc/p.pdf h`; crop each
   staff, run tools/handoff/scratch/omr/notes.py on it, zoom 2-3x to confirm, measure text with
   tools/passion/words.py; add to TONES.md.
2. Engine: tools/passion/tones.js using js/psalm.js `P.analyse(text)` for syllables/accents (as tools/proc/gen_tones.js
   does). One function per voice and cadence type as in TONES.md; every printed example in TONES.md is a test
   (the engine must reproduce it note for note); the "Sententiae variae" (Ego sum, Tu dixisti, Sitio, Eli,
   Deus meus, Consummatum est, Pater in manus, Non sum, Barabbam...) are fixed settings used whenever that
   text occurs. Clefs: Chronista/Christus c3 (Christus cb3, i.e. flat at the clef), turba c2; switch to c2
   where the book does (Eli "Vel" form, Consummatum est, Pater in manus). Check with
   `cd /tmp && gregorio -o x.gtex /abs/file.gabc`.
3. Answer the open questions with Joseph first.
4. Then the 4 Passion workers (one each; they may write only gabc/op-passio-<mt|mc|lc|jo>-*.gabc and
   tools/passion/<name>/): check tools/hw39/{passio,marcus,lucas,joannes}_parts.txt against the Missal 1939
   (W-C0 was doing this), split per voice turn and sentence by the Missal's punctuation (: ; , ? .), choose the
   cadence by what follows (next voice, clamor/death, end), set with the engine, one gabc per paragraph of
   *_parts.txt (phone-sized), header: "set to the Dominican Passion tones, Processionarium O.P. 1913, pp. 435-440".
   Second pass: a sample against TONES.md and against Fr Smith's English Mark (uploads, not to be copied).
   The ending of each Passion in the Lamentation tone (p. 440) only where the Missal's Passion text has it.
5. Hand up READY with the G: lines for tools/hw39/*.src (Lead B / coordinator integrates).
