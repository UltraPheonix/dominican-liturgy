# Dominican Passion tones: Processionarium O.P. 1913, pp. 435-440 (pdf 451-456), "VII. Modus cantandi Passiones"

Read note by note from 400 dpi renders (`pdftoppm -r 400 -f 451 -l 456`), with the note reader
tools/handoff/scratch/omr/notes.py (gabc staff letters: d = bottom line, f, h, j = top line), then each staff
checked by eye at 2-4x zoom. Text-to-note assignment was measured: the x-extent of each printed syllable
(script below) compared with the x of the notes. In this book a syllable's text starts 0-90 px (at 400 dpi)
left of its first note.

Notation used below: gabc staff letters; UPPER case = rhombus (punctum inclinatum) in a descending group;
`,` = the short vertical stroke the book prints inside long melismas (render as divisio minima);
`|` = bar; `||` = double bar. Pitches in brackets are for the clef shown.

STATUS: pp. 435-439 read and checked by eye. p. 440 is NOT finished: see the end of this file.

## Clefs
- Chronista, Christus (pp. 435-438 first half): **c3** (C on the 3rd line = h). Pitches: d=F e=G f=A g=B h=c i=d j=e k=f.
- Christus "Vel: Eli..." (p. 438 from "Vel"), "Consummatum est", "Pater, in manus" (p. 439 top): **c2** (C on line f).
  Pitches: c=G d=A e=B f=c g=d h=e i=f j=g k=a. The flat is printed on e (= B flat).
- Turba (p. 439): **c2**. Tenor i = f, the octave above the Chronista's final F (rule text "incipit in octava
  ultimae notae vocis textus").
- Flats: Christus has the flat at the clef (p. 437 "Tradétur", "Opus"; flat before each incipit): treat every B
  in the Christus voice as B flat (c3: g; c2: e). Chronista: the flat is printed on g in the final cadence
  "Secúndum Matthǽum" and before "discípulis" (before Christ); NOT printed in the mediation ("Jesu" g) nor in the
  second final example "Discípulis suis". Fr Smith's English model puts B flat in every Chronista final cadence.

## 1. Vox textus C. (Chronista), c3, tenor h (= c)
Rule (p. 435): "Fit mediatio in mediis sententiis (nisi in brevioribus) elevando accentum ultimum et reliquas
syllabas, si adsint, flexis prius duabus syllabis ante ipsum, ut in Lectionibus".
- p.435-436 `Pas(h) si(h) o(h) Dó(h) mi(h) ni(h) nos(h) tri(h) Je(g) su(f) Chrí(h) sti(h). ||`
- `In(h) il(g) lo(f) tém(h) po(h) re(h). ||`
  => MEDIATION: the 2 syllables before the last accent: g, f; accent and following: h.

Rule (p. 436) "Finales Versuum fiunt, quando non sequitur vox turbae aut Christi, flectendo duabus syllabis ante accentum ultimum":
- `Se(h) cún(h) dum(e) [flat on g] Mat(f) thǽ(gf) um(ed). ||`  (gf and ed are clivis)
- `Dis(h) cí(h) pu(e) lis(f) sú(gf) is(ed). ||` (no flat printed here)
  => FINAL: 2 syllables before the last accent: e, f; accent: gf (B flat-A); last syllable: ed.
  OPEN QUESTION: a dactyl (e.g. "Dóminum") is not printed. Default proposed: Dó(g) mi(f) num(ed)
  (like the turba, where the post-tonic note moves to the middle syllable, and like Fr Smith's "ó-ver to them"
  g f e d). Ask Joseph before generating.

Rule (p. 436) "Quando sequitur vox Christi, fit terminatio incipiendo ad penultimum accentum":
- `Di(h) xit(h) Je(h) sus(h) [flat on g] dis(h) cí(gi) pu(h) lis(h) sú(gFE gFE) is(ef). ||`
  (cí = pes g-i; sú = two climaci g-F-E; is = pes e-f; text measured: both climaci are on "su")
  => BEFORE CHRIST: penultimate accent: pes gi; then h up to the last accent; last accent: gFE gFE; last syllable: ef.
- p. 438 short form `Hoc(hg iHGFE , gFE) est(ef). ||` ("C Hoc est: ✠ Deus meus"; flat at the clef).

Rule (p. 436) "Quando sequitur vox turbae, terminatio fit elevando syllabam quae praecedit ultimum accentum et reliquas post accentum, flectendo ad quintam":
- `Di(h) cé(h) bant(i) áu(h) tem(d). || Di(i) cén(h) tes(d). ||`
  => BEFORE TURBA: syllable before the last accent: i; accent: h; all after: d (F).

Rule (p. 436) "Quando sequuntur verba turbae clamantis: Crucifige, Crucifigatur, Tolle, sic dicitur":
- `At(h) il(h) li(h) ma(h) gis(h) cla(h) má(h) bant(i) di(j) cén(i) tes(h). ||`
  => before a clamor of the crowd: 2nd syllable before the last accent: i; syllable before: j; accent: i; after: h.

Rule (p. 436-437) "Quando exprimitur clamor vel mors Christi, vel finitur Passio, sic terminatur":
- `Vo(h) ce(h) má(hi jk , kJIH) gna(gh) dí(ih) cens(h). |`
- `Trá(hi jk , kJIH) di(g) dit(h) spí(i) ri(h) tum(h). |`
- p.437 `Cón(hi jk , kJIH) tra(g) se(h) púl(ih) crum(h). ||`
  (hi jk = two pes; then the stroke; then virga k + 3 rhombs j i h)
  => CLAMOR/DEATH/END: the penultimate accent: hi jk , kJIH; the syllables up to the last accent: g, h
  (one syllable: pes gh); last accent: i, then h (one post-tonic: accent = clivis ih); all after: h.

## 2. Vox Christi ✠ (p. 437), c3, tenor e (= G), every B flat
"sic incipit":
- `Sci(de fh giHGFE) tis(e) , qui(e) a(e) post(e) bí(e) du(e) um(e). ||`
  (S = drop cap; de, fh = pes; gi = pes followed by 4 rhombs h g f e; the stroke is after "Scitis")
  => INCIPIT (first sentence): first syllable de fh giHGFE, then tenor e.
"Sic mediatur, flectendo duabus syllabis ante accentum ultimum":
- `Pas(d) cha(e) [flat] fí(fg) et(f), | et(e) Fí(e) li(e) us(e) hó(e) mi(e) nis(e). ||`
  => MEDIATION: 2 syllables before the last accent: d, e; accent: pes fg; after: f. Bar after.
"Sic finitur, incipiendo duabus syllabis regulariter ante ultimum accentum":
- `[flat at clef] Tra(e) dé(e) tur(e) ut(e) cru(e) ci(f) fi(g) gá(fEDC e) tur(d). ||`
  (climacus f-e-d-c = virga + 3 rhombs, c below the staff; then punctum e; measured: the e is on "gá")
  => FINAL: 2 syllables before the last accent: f, g; accent: fEDC e; all after: d.
"Posteriores sententiae, quando plures immediate sibi succedunt, sic incipere possunt" (three options):
- `O(gFE) pus(e) e(d) nim(e) bó(fg) num(f). |`  (incipit + a mediation)
- `Jam(hg iHGFE) sem(e) per(e). |`
- `Mit(hFD gFE) tens(e). ||`  (measured: both climaci on "Mit")
"Interrogationes incipiunt ut aliae sententiae, et finiuntur flectendo syllabam ante accentum ultimum":
- `Quid(de fh giHGFE) mo(e) lés(e) ti(e) es(e) tis(e) hu(e) ic(e) mu(b) lí(d) e(d) ri(ef)? || Si(de fh giHGFE)` [p.438] `mon(b), dór(d) mis(ef)? ||`
- `Quem(de fh giHGFE b) quǽ(d) ri(d) tis(ef)? ||`  (b = ledger line below the staff = D; on Quem as a 5th rhomb)
  => INTERROGATION: syllable before the last accent: b; accent: d; after: d; last syllable: pes ef.
"Sententiae variae" (p. 438), c3:
- `E(de) go(fg fEDC e) sum(d). ||`
- `Tu(de fg) di(g) xí(fEDC e) sti(d). ||`
- `Sí(de fg fEDC e) ti(d) o(d). ||`   (measured: ti centred on d)
- `E(i jk , kJIHGF h) li(i), | E(i jk , kJIHGF h) li(i) | lam(e) ma(f) sa(g) bac(h) tá(gf) ni(hi)? ||`
- Chronista `Hoc(hg iHGFE , gFE) est(ef): ||` ✠ `De(i) us(i) mé(i jk , kJIHGF h) us(i), | De(i) us(i) mé(i jk , [flat] kJIHGF h) us(i) | ut(e) quid(f) de(g) re(h) li(g) quí(f) sti(e) me(hi)? ||`
- "Vel:" (new clef **c2**, flat on e): `E(g gFD fg) li(g), | E(jki iHGFE f) li(g) | lam(c) ma(d) sa(e) bac(f) tá(ed) ni(fg)? || De(g) us(g gFD) me(fg) us(g) | De(g) us(g) me(jki iHGFE) us(g), | ut(c) quid(d) de(e) re(f) li(e) quí(d) sti(c) me(fg)? ||`
  (the c2 "Vel" form of "lamma sabactani" and "ut quid dereliquisti me" gives the same pitches as the c3 form)
- c2: `Con(g gFD) sum(fg) má(g , jki iHGF) tum(hi) est(g). ||`
- p. 439, c2: `Pa(g gFD fg) ter(g), | in(g) ma(h) nus(i) tu(j) as(j) | com(j) mén(k) do(j) spí(g) ri(g) tum(f) mé(hi) um(g). ||`

## 3. Vox turbae S. (p. 439), c2, tenor i (= f)
Rule: "incipit in octava ultimae notae vocis textus; mediatur ut ipsa vox textus; finitur autem sententia elevando ad penultimum accentum, et iterum ad ultimum":
- `Non(i) in(i) di(h) e(g) fés(i) to(i), | ne(i) for(i) te(i) tu(i) múl(i) tus(i) fí(j) e(h) ret(h) in(h) pó(i) pu(h) lo(gf). ||`
  => MEDIATION: 2 syllables before the last accent: h, g; accent and after: i.
  => FINAL: penultimate accent: j; syllables between: h; last accent: i; post-tonic: h; last syllable: clivis gf.
"Interrogationes fiunt flectendo duas syllabas ante ultimum accentum; et si in medio sententiae fuerit virgula, ad ipsam fit flexio":
- `Ut(i) quid(i) per(i) dí(i) ti(h) o(f) haec(gji)? ||`  (pes g-j + i)
- `Quid(i) vul(i) tis(i) mi(i) hi(i) dá(i) re(g), | et(i) e(i) go(i) vo(i) bis(i) e(h) um(f) trá(g) dam(ji)? ||`
- `Num(i) quid(i) e(i) go(h) sum(f), Dó(g) mi(g) ne(ji)? || Quid(h) ad(f) nos(gji)? ||`
  => INTERROGATION: 2 syllables before the last accent: h, f; accent: g; middle post-tonic: g; last: clivis ji;
     accent on the last syllable: gji. FLEXIO at a comma: post-tonic syllables to g ("dá(i) re(g)").
"Sententiae variae":
- `Tu(j) ví(hi) de(h) ris(gf). || Non(jh ih) sum(gf). || Ba(j) ráb(hih) bam(gf). ||`
  => the final formula compresses: no syllable between P and L: L = pes hi; one post-tonic only: L = hih;
     monosyllable at the end: the previous syllable carries j h i h.
- `Tol(i) le(i), tol(i) le(i), |` then p. 440 (NOT VERIFIED, see below).

## p. 440: NOT FINISHED
- "crucifige eum. Crucifigátur." Raw note-reader output only (staff from y=600 at 400 dpi, x from 330), clef not
  yet confirmed (looks low, possibly c1 or c2 placed low): `98:i 176:i 209:l(flat) 242:l 320:k 353:j 376:i 399:h 498:j 564:i || 784:i 826:l(flat) 860:l 927:k 961:j 982:i 1005:h 1082:j 1160:i ||`.
  The image shows: cru ci (two puncta), fí = [flat] + punctum above the staff with ledger, then virga + 3 rhombs,
  then virga, punctum. Read again at 3x zoom; determine the clef and the flat's pitch.
- "4° Finitur Passio cum tono Lamentationis, hoc modo: Altera autem die ... cum custódibus." (4 staves +
  "bus.") NOT READ. Also p. 436 has nothing more for Gospel endings beyond the examples above.

## Measuring helpers (used above)
- notes: `python3 tools/handoff/scratch/omr/notes.py PAGE.png x0,y0,x1,y1` (prints staff line y's and x:letter)
- text extents: tools/passion/words.py PAGE.png x0,y0,x1,y1 GAP OFFSET (x-extent of each printed word/syllable)
