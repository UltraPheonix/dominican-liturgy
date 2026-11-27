# W-B3: Maundy Thursday (1939) prayers, readings and versicles in the Dominican tones

Stopped 27 Nov 2026, when the swarm was cut. **Nothing has been generated or wired in.** No gabc was written, no G: line
was added to any tools/hw39/Quad6h*.src, and no site file was changed. The only files written are this note and the
OCR scratch files in tools/handoff/scratch/w-b3/.
The engine (js/mtones.js, Lead B) was declared STABLE just before the stop. It was tried on sample prayers (see 4).

Books: Missale O.P. 1939 (M39), text in tools/orat39/m39lin.txt. Triduum O.P. 1927 (/tmp/dl/tri.pdf): **pdf page =
printed/2 + 3** (one pdf page holds two printed pages, e.g. pdf 18 = pp. 30-31). Processionarium 1913 (Proc): pdf =
printed + 16.

## 1. Findings that change the plan (read these first)
1. **The Sermo Domini is NOT all in the Gospel tone.** Triduum p. 123 (pdf 64, right half) says: "Finito Evangelio
   ... Diaconus ex integro prosequatur Sermonem Dominicum **in tono Lectionis**, stans versus Crucifixum ...". The
   "tono cantus Evangelii" covers only the Gospel *Ante diem festum* (Jn 13:1-15, ending "ita et vos faciátis.", pp.
   122-123), with Dóminus vobíscum and Sequéntia. The rest (Jn 13:16 "Amen, amen dico vobis" to 17:26, pp. 123-130) is
   in the **lesson tone** (Proc pp. 408-413). It ends "sine Tu autem" (rubric, p. 130), so it ends by n. 11 (p. 413).
   - The "Finito Evangelio ..." rubric is missing from Quad6h_mand.src.
   - hw_tones.md and the coordinator's brief ("use gospelProc for the Sermo") are wrong on this point.
2. **The Sermo text in Quad6h_mand.src is not the Triduum's text.** It is the site Bible, in 31 paragraphs. The book
   differs in words and pointing. For example, p. 124 inserts "Cap. 14 / Et ait discípulis suis. Non turbétur ...".
   The book's punctuation ("Dómine: tu mihi lavas pedes?") and its flex signs (‡) differ too. The .src text (a
   W-B6 / text-owner job) must be retranscribed from pp. 122-130 before any chant is generated. OCR (Italian model,
   needs proofreading): scratch/w-b3/tri_pp123-130_sermo_ocr.txt.
3. **The Triduum prints the prayers pointed for singing** (‡ = flexa, ":" = metrum), even those said "humili voce".
   The punctuation in the .src often differs from the book, and the generator must take the book's pointing:
   - Actiónes nostras (p. 112): book "...a te semper incípiat ‡ et per te cœpta finiátur: Per Christum Dóminum
     nostrum ‡ ℟. Amen."; the .src has "incípiat, et ... finiátur. Per Christum".
   - Adésto (p. 121): book "...retinénda mandásti ‡ sed præsta ... lavéntur peccáta: Qui vivis et regnas per ómnia
     sǽcula sæculórum ‡ ℟. Amen."; the .src has "mandásti: sed" and "laventur" with no accent.
   - Réspice (Lauds p. 44; Compline p. 133): book "famíliam tuam ‡ pro qua ... mánibus tradi nocéntium: et crucis
     subíre torméntum". Compline ends with "‡"; Lauds prints a full stop. The .src has "nocéntium, et crucis".
   - The altar-washing prayers and versicles (pp. 92-111) carry ‡ and colons throughout; "Orémus ‡" is printed
     before each prayer. OCR: scratch/w-b3/tri_pp92-111_ablutio_ocr.txt. In it ‡ is read as 3, 4, %, &, z or <.
   Report these text differences to the text owner.
4. **Versicles in the Triduum:** Proc p. 395 2° ("Versiculi in Triduo ante Pascha ... ante Lectiones Nocturnorum
   tantum") covers only the Tenebrae versicles, which are already notated. The other versicles take 3° ("ad Memorias
   ... et in Processionibus, et quotiescumque dicitur ℣. a Sacerdote", pp. 395-396). Reuse `vr()` from
   tools/proc/gen_tones.js (the same rule as the live processions).

## 2. Inventory (in order), with rubric, tone and status
| # | Item | Source / rubric | Tone | Status |
|---|---|---|---|---|
| 01 | Preces "Et ne nos ... Dómine exáudi" (Prior; ℣ only, no ℟ printed) | M39 p. 54 (Quad6h.src l.13): "dicat :" stands BEFORE "Quæ sequuntur, dicat eo modo, quo dicuntur Orationes ad Horas" | versicle 3° p. 395? | **QUESTION** for main: are they sung, and to which tone? |
| 02 | Dóminus vobíscum. Orémus. Exáudi ... Per Christum. ℟ Amen | M39 p. 54: "Quæ sequuntur, dicat eo modo, quo dicuntur Orationes ad Horas." | III, Proc pp. 407-408; orationProc hours, dv, pointing book | to generate |
| 03 | Absolution "Dóminus Jesus Christus ... in sǽcula sæculórum. ℟. Amen." | M39 p. 54: "faciat absolutionem absque Dóminus vobíscum, et absque Orémus" (still under "Quæ sequuntur") | III, noOremus; append ℟ Amen | to generate, see 4 (ending) |
| 04 | Collect "Deus, a quo et Judas" | M39 p. 161 prints "Orémus / Oratio" only (DV comes from the Order of Mass after the Gloria) | II (mass), oremus | to generate |
| 05 | Epistle 1 Cor 11, title "Léctio Epístolæ beáti Pauli Apóstoli ad Corínthios." | M39 p. 161 | epistleProc {title} | to generate |
| 06 | Gospel Jn 13 "Ante diem festum" | M39 p. 162 | gospelProc {book:'Joannes', dv:true} | to generate |
| 07 | Postcommunion "Refécti" with DV + Orémus | M39 p. 164: "dicat Dóminus vobíscum. Deinde reversus ad librum dicat more solito: Orémus." | II, dv, oremus | to generate |
| 08 | ℣ Panem de cælo ℟ Omne delectaméntum (Acolytes) | M39 p. 165: "Acolythi dicant" (in the procession) | versicle 3° | to generate |
| 09 | Altar of repose "Deus, qui nobis" ... "Qui vivis et regnas per ómnia." | M39 p. 165: "Prior erectus subjungat: Orémus" | III (not de corpore Missae), oremus | to generate |
| 10 | Alternative ending (Vespers first) "Orémus. Refécti ... ut supra" | M39 p. 165 | reuse 07 after the R line (Quad6h.src l.310) | to wire |
| 11 | Actiónes nostras | Triduum p. 112: "dicat humili voce hanc Orationem" (no Orémus) | III, noOremus, book pointing (1.3) | to generate; keep the rubric above |
| 12 | Adésto Dómine | Triduum p. 121: "dicat humili voce Orationem sequentem, sine Orémus" | III, noOremus, book pointing | to generate; keep the rubric above |
| 13 | Sermo, Gospel part Jn 13:1-15 + DV + Sequéntia | Triduum p. 122: "dicat tono cantus Evangélii: Dóminus vobíscum ... legat solémniter Evangélium" | gospelProc dv | **blocked by 1.2** (.src text) |
| 14-18 | Sermo, rest Jn 13:16-17:26 (book's chapter breaks: 13, 14, 15, 16, 17) | Triduum p. 123 "in tono Lectionis", p. 130 "sine Tu autem" | lessonProc pointing book; only the last part ends by n. 11, the others need a non-final ending (option to ask B for) | **blocked by 1.1/1.2** |
| 19 | ℣ Adjutórium nostrum ℟ Qui fecit (Prelate) | Triduum p. 130 (Quad6h_mand.src l.119 rubric) | versicle 3° | to generate, after the R line |
| 20+ | Altar washing: 32 versicles + ~35 prayers (the Virgin altar has 3; the Doctor altar has a prayer and no antiphon) | Triduum p. 87ff: "Ceroferarii ... dicant ℣. ..., et Prior Orationem ex libello"; "voce mediocri (in qua totum hoc Officium fieri debet)" | ℣ 3°; prayers III with "Orémus" (printed "Orémus ‡"), book pointing | to generate. **QUESTION:** the "N." in the commons, recite on h? |
| T1 | Lauds "Réspice" (no DV, no Orémus, no conclusion, no Amen) | Triduum p. 44: "absque Dóminus vobíscum, et absque Orémus, dicatur" | II ("Orationes ad Vesperas, Laudes et Missam", p. 404) | **QUESTION:** the ending (p. 44 prints no ‡ at the end) |
| T2 | Compline "Réspice" | Triduum p. 133 (ends "torméntum ‡") | III, final flex (tormén(h)tum(f)) | to generate |
| T3-6 | Prime/Terce/Sext/None "Réspice" (Quad6h_ten.src l.1107, 1279, 1403, 1527) | Triduum pp. 44-56 | III; check each page's pointing | to generate |
| opt | Prime: Pretiosa ℣, "Sancta María" (absque Orémus), ℣ Réspice, "Dirígere" (absque Orémus), short lesson "Secúndum Joánnem ... Tu autem", ℣ Osténde + DV + "Actiónes", ℣ Adjutórium | Triduum pp. 44-46 | ℣ 3°, prayers III, lesson IV (n. 10) | **QUESTION:** in scope? (this is the Office) |
| opt | Tenebrae Lessons IV-IX (Leo, Chrysostom) | Triduum pp. 1-31: "Lector incipiat legere", no Tu autem; pointed with ‡ | lessonProc, end by n. 11 | **QUESTION:** in scope? |

Already notated (leave alone): Tenebrae antiphons, versicles, Lamentations (op-ten-h-*), the responsories
(op-abl-r01-10), the altar antiphons (op-abl-a01-32), the Mandatum antiphons (op-mand-01-13), Pange lingua, the
Vespers antiphons and psalms (op-hv-*), the Compline psalms.

## 3. Generator plan (tools/hw39/gen_quad6h.js, not yet written)
- `globalThis.window = globalThis; require('../../js/psalm.js'); require('../../js/mtones.js')`, then use OPMassTones.
- The items table: {id op-hw-quad6h-NN, src file, anchor (the start of the T line, or of the "T: Orémus." /
  "T: Dóminus vobíscum." line just above it), position before/after, kind, opts, book text with its pointing (for
  Triduum items), book/page/rubric}.
  - Check that the book text equals the .src text, ignoring punctuation and j/i, and print the differences for
    the text owner.
- Header like gabc/op13-*.gabc: name; office-part; book: "Missale O.P. 1939 p. N" or "Officium Triduo ante Pascha
  O.P. 1927 p. N"; commentary: "set to the <tone>, Processionarium O.P. 1913 pp. X (rule quoted)"; transcriber:
  "tone applied to this text for this site".
- `--insert`: re-read the .src just before the edit and insert "G: id|label" before the anchor, only if it is not
  already there.

## 4. How the STABLE engine behaves (tried 27 Nov)
- orationProc 'hours' with `pointing:'book'` turns ‡ into ";". The ";" then shows in the lyric
  ("in(h)cí(h)pi(f)at;(f)"). Strip the ";" that came from ‡ afterwards, as tools/proc/gen_tones.js strips †.
- **A prayer with no conclusion whose book ends it with ‡** (Compline Réspice) comes out as an elevatio
  (tor(f)mén(h)tum;(h)). Build the last member with `T._proc.flexO(last, true)`; the result should be
  tormén(h)tum(f).
- The absolution ending "in sǽcula sæculórum." comes out as an elevatio (sæ(g)cu(f)ló(h)rum(h)). Suggestion, to be
  confirmed by main: a final flex, as the book does in Compline p. 133 and in the conclusion p. 408
  ("sæculó(h)rum(f)"). Add ℟. A(g)men.(h) by hand, because orationProc adds Amen only after a recognised conclusion.
- The repose prayer and Actiónes came out right: the metrum at the colons, the flex at ";", and the conclusions
  nos(h)trum(f) and sæculó(h)rum(f) as on p. 408.
- expandConcl adds "ejúsdem" when the body names the Holy Spirit. PROGRESS.md says the Missal prints "in unitáte
  Spíritus" without ejúsdem. Ask B (not relevant to Thursday's prayers).

## 5. Resume steps
1. Get answers from main: 01 preces, T1 Lauds ending, absolution ending, "N." in the commons, the optional items,
   and who retranscribes the Sermo .src text (with the missing p. 123 rubric).
2. Write gen_quad6h.js as in 3. Do items 02-12, 19, 20+, T2-T6 first.
3. For each file: `cd /tmp && gregorio -o x.gtex /home/claude/dominican-liturgy/gabc/op-hw-quad6h-NN.gabc`.
4. Insert the G: lines (re-read the .src first; W-B6 edits the same files), then `python3 tools/hw39/build.py`.
5. Headless Chrome (playwright, /usr/bin/google-chrome), http://localhost:8765/holyweek.html#Quad6h&d=2027-03-25,
   localStorage hwRite=1939: no console errors and no "could not be drawn".
