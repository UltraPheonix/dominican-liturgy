# W-C0: Passion texts proofed against Missale O.P. 1939 (paused 27 Nov)

Source: /home/claude/dl/missal/M39.pdf. Each pdf page is a spread of two printed pages, and pdf page = text-layer `@@PAGE` + 1.
Method:
- A word, punctuation and case diff against tools/orat39/m39lin.txt, with C/S sigla and parentheses as tokens.
- Then every column read at 150 dpi and compared with the file reflowed to the Missal's lines, zooming to 300 dpi where unsure.
- Scripts are in /tmp/wc0s (diff.py, align.py, case.py, zoom.py, noacc.py). They are not in the repo.

## State
All four Passions were checked word by word against the scan. Every correction below was seen on the scan and has been applied.
build.py has been run, and holyweek.html for Sun, Tue, Wed and Fri shows no console errors in headless Chrome.
No G-blocks were lost: all 204 in HEAD are still there, plus Lead B's new op-hw-quad6f-*.

| Passion | Missal pp. (pdf) | Fixes applied |
|---|---|---|
| Matthew, passio_parts.txt | 140-146 (104-107) | 10 accents on æ: Galilǽam, Zebedǽi x2, Galilǽo, Galilǽa, prǽsidi, prǽsidem, prǽsidis, Cyrenǽum, Arimathǽa |
| Mark, marcus_parts.txt | 149-153 (108-110) | 9 fixes, listed below |
| Luke, lucas_parts.txt | 155-160 (111-114) | 20 fixes, listed below |
| John, joannes_parts.txt | 167-171 (117-119) | 16 fixes, listed below |

### Mark
- "et Azyma": the Missal has no accent; the file had Ázyma.
- "Amen dico vobis : ubicúmque": colon, not comma.
- "(erant enim óculi eórum graváti)": parentheses added.
- "núbibus cæli": was cœli.
- "Et cœpit flere. * Et conféstim": period and red asterisk added.
- "Ave Rex Judæórum. C Et percutiébant": C added.
- "Israël": was Israél.
- "mortem : Sustinéte": capital S.
- "témpore : Erat": spacing only.

### Luke
- "introëúntibus": was "introéúntibus".
- "At ille dixit : ✠ Dico tibi Petre": ✠ was missing.
- "sácculo" and "sácculum": were sǽculo and sǽculum, which is the wrong word.
- "Et qui non habet": a stray colon removed.
- "de cælo": was cœlo.
- "Et ait illis : ✠ Quid dormítis": was "illis J.Quid".
- "illo erat. C At ille negávit": C added.
- Five missing colons before S: "affirmábat, dicens :", "interrogábant eum, dicéntes :", "concílium suum, dicéntes :", "accusáre, dicéntes :", "glorificávit Deum, dicens :".
- "de ore ejus. * C Et surgens": period and red asterisk added.
- "Cǽsari" and "Judǽam": accents added.
- "si homo Galilǽus": a stray C removed.
- "quamdam factam": the Missal has no accent.
- "lítteris Græcis": capital G.
- "genuflectitur": was "genujlectitur", an OCR error.

### John
- "Pharisǽis" and "notus Pontífici": capitals.
- "mihi : Quid": colon, not semicolon.
- "dimíttam vobis": lower-case v.
- "dicéntes : S Non hunc": colon added.
- "latro. * Tunc ergo": red asterisk added.
- "C (Exívit ... vestiméntum)": opening parenthesis added.
- "Græce, et Latíne": a stray "t" removed.
- "scripsi. C Mílites" and "cujus sit. C Ut Scriptúra": C added in both places.
- "Matri suæ : ✠": colon added.
- "Judǽi ergo, (quóniam Parascéve erat) ... (erat enim magnus dies ille sábbati)": the Missal prints no C after the rubric, so the C was removed; parentheses added.
- "Arimathǽa, (eo quod ... Judæórum)": parentheses added.

### QC items already right in the files
Dixit ergo Petro, the stray "1" (gone), Cyrenénsem (Luke), conviciabántur.

## Voice assignment (C / ✠ / S)
- Every C and S now matches the Missal's printed sigla. Every ✠ was confirmed on the scan; the text layer often drops it.
- The Missal marks every speaker other than Christ and the narrator as S. That includes single speakers: Judas, Peter, the maids, Caiaphas, Pilate, Pilate's wife, the thief, the centurion.
- Proc. 1913 p. 439 confirms this: its examples of the Vox turbae include Judas's words "Quid vultis mihi dare..." and "Numquid ego sum, Dómine?".
- Not doubtful, but note: words quoted inside the narration stay C because the Missal gives them no siglum. Examples: Mt "Quia non novi hóminem", "Hic est Jesus Rex Judæórum"; Mk "Quia hic ex illis est"; Jn "Ego sum" in "Ut ergo dixit eis", "Quia éxpedit".
- The closing sections have no sigla (one voice), as printed.

## Special passages (for Lead C's tone engine)
- **Proc. 1913 pp. 435-440 (pdf 451-456):**
  - p. 438: settings for Sítio, "Eli, Eli, lamma sabactáni? C Hoc est : ✠ Deus meus..." (also a "Vel" form without the C), and "Consummátum est".
  - p. 439: "Pater, in manus tuas commendo spíritum meum".
  - p. 436: cadences "Quando sequuntur verba turbæ clamantis: Crucifige, Crucifigatur, Tolle" and "Quando exprimitur clamor vel mors Christi, vel finitur Passio" (e.g. "Voce magna dicens", "Trádidit spíritum").
- **Where they are in the files:**
  - Mt: "✠ Eli, Eli, lamma sabactháni? C Hoc est : ✠ Deus meus...".
  - Mk: "✠ Eloi, Eloi, lamma sabactháni? C Quod est interpretátum : ✠ Deus meus...".
  - Lk: "✠ Pater, in manus tuas comméndo spíritum meum."
  - Jn: "✠ Sítio." and "✠ Consummátum est."
  - Crucifige / Crucifigátur / Tolle: Mt (Crucifigátur x2), Mk (Crucifíge eum x2), Lk (Crucifíge, crucifíge eum), Jn (Crucifíge x2; Tolle, tolle, crucifíge eum).
- **Lamentation-tone ending.** Proc. p. 440: "4° Finitur Passio cum tono Lamentationis, hoc modo : ALTERA autem die...". The Missal starts each closing section as a new paragraph with a large initial:
  - Mt p. 146: "ALTERA autem die".
  - Mk p. 153: "ET cum jam sero esset factum".
  - Lk p. 160: "ET ecce vir nómine Joseph".
  - Jn p. 171: "POST hæc autem rogávit Pilátum".
- **Red asterisks:** "* Mane autem facto" (Mt p. 143), "* Et conféstim" (Mk p. 151), "* C Et surgens" (Lk p. 158), "* Tunc ergo apprehéndit" (Jn p. 169). The Missal does not explain them; build.py's comment calls the asterisk "the pause before Mane autem facto". **Question for main:** what is the asterisk for?
- **Rubric "Hic pausatur aliquantulum, et genuflectitur."** It comes after "emísit spíritum" (Mt), "exspirávit" (Mk), "exspirávit" (Lk), and "trádidit spíritum" (Jn).

## Left to do (not done; needs files outside my list or an English re-pairing)
1. **Paragraph breaks for the closing sections:**
   - Mark "ET cum jam sero" and John "POST hæc autem" are still in the same paragraph as the text before them (marcus line 45, joannes line 31). Each needs a split, and the matching _en.txt paragraph must be split at the same verse (Mk 15:42, Jn 19:38). Matthew and Luke are already separate paragraphs.
   - build.py (not mine) drops the initial only for `a.startswith('ALTERA')`. It should also handle "ET cum", "ET ecce" and "POST hæc", or better, mark the Lamentation section explicitly.
2. **English _en.txt:** not reviewed. qc_hw.md lists these known items: the John English adds "When Jesus had said these things" and lacks the speaker marks; the Tue and Wed English drop "At that time".
3. The red asterisk question above.
