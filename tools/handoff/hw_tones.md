# Holy Week 1939: celebrant's and ministers' tones (orations, lessons, Epistles, Gospels)

Status 2026-11-27 13:xx: research done, NO site files changed yet (no gabc written, no G: lines added,
js/mtones.js untouched). Everything below is ready to implement.

Sources read (pdf page = printed + 16): Processionarium O.P. 1913, /home/claude/dl/proc/p.pdf, Art. III
"Modus cantandi Capitula, Orationes, Benedictiones, Lectiones, Epistolas, Evangelia, Passiones", pp. 402-426.
Page images were read at 400 dpi (pdftoppm -r 400 -f N -l N). Clef: F on the 3rd line (f3), the small
punctum before the clef marks the F clef. Pitches below in gabc letters with f3: h = FA (reciting note),
g = MI, f = RE, i = SOL, c = LA (A below the staff, below line 1).

Also checked: Missale O.P. 1939 appendix (/home/claude/dl/missal/M39.pdf, pdf 446-463) has ONLY Gloria,
Prefaces, Pater, Agnus/Ite tones: no oration/lesson/Epistle/Gospel tones. Triduum O.P. 1927 (/tmp/dl/tri.pdf,
no text layer) prints the Good Friday and Holy Saturday orations and lessons WITHOUT notes but POINTED for
singing with the flex sign and colons (e.g. pdf 92 = pp. 178-179 Osee, pdf 98 = pp. 190-191 solemn prayers;
Holy Saturday lessons/prayers around pdf 137-140). Its pointing confirms Proc. p. 405: "ad signum flexae
(vel in Missali ad punctum cum virgula ;)" = the Missal's semicolon is the flex.

## 1. Orations

### Tone II: "Orationes ad Vesperas, Laudes et Missam" (pp. 404-406)
- Dominus vobiscum (p. 404): Dó(g)mi(h)nus(h) vo(gh)bís(hg)cum.(g) ℟. Et(g) cum(h) spí(h)ri(g)tu(g) tu(h)o.(h)
  (identical to gabc/op13-palm-evangelium-dv.gabc, p. 23).
- Orémus (p. 405): O(h)ré(gh)mus.(h)  (= gabc/op13-quad6f-oremus.gabc, op-h-oremus.gabc)
- Flectámus génua. Leváte. (p. 405, Lenten ferias): Flec(f)tá(h)mus(i) gé(i)nu(h)a.(h) Le(f)vá(hi)te.(i)
  (= gabc/op-m39-flectamus.gabc, op13-quad6f-flectamus.gabc with Orémus)
- Before the last Postcommunion (p. 405): Hu(h)mi(h)li(h)á(h)te(h) cá(h)pi(f)ta(f) ves(fh)tra(g) De(h)o.(h)
  (= gabc/op-m39-humiliate.gabc)
- Body (2°, p. 405): two inflexions, by punctuation:
  * FLEXIO at the flex sign / Missal ";": the syllables after the last accent go to MI (g).
    e.g. tri(h)stí(h)ti(g)a(g) ; ... Fí(h)li(h)um(h) tú(h)um(g) ; ... Pá(h)tre(g) ;
  * ELEVATIO at ":": the two syllables before the last accent on MI (three, if the third before the accent
    is the middle syllable of a dactyl: pér-fru-i læ-tí-ti-a -> fru(g) i(g) læ(g) tí(h)), the accent and
    following syllables back on FA: sa(h)lú(h)te(g) gáu(g)dé(h)re(h) :
  * Order: elevatio at the start, flexio in the middle, ALWAYS elevatio at the end (before the conclusion),
    alternating; shorter prayer drops the first elevatio, longer prefixes another flexio. Commas: no inflexion.
  * Implementation plan: split body at : ; (and . ? inside the body), assign types from the END backwards:
    last = elevatio; earlier ones by punctuation (; flex, : elev) but flipped if equal to the following one.
    Tested by hand on the Good Friday prayers: reproduces the Triduum 1927 pointing exactly.
  * Anomaly: p. 406 prints "et(g) æ(g)térna" after the flex; the same example in tone III (p. 407) has
    et(h) æ(h). Not in the rule text: treat as a misprint, recite on h.
- Conclusions (3°, p. 406):
  Per Dóminum nostrum Jesum Christum Fílium tu(h)um(g) ; [flex]
  qui tecum vivit et regnat in unitáte Spíritus sanc(g)ti(g) Dé(h)us(h) : [elevatio]
  per(h) óm(i)ni(h)a(h) sǽ(h)cu(g)la(g) sæ(g)cu(h)ló(hg)rum.(g)   ℟. A(g)men.(h)
  Qui vivis et regnas cum Deo Pá(h)tre(g) ; in unitáte ... (as above)
  (the TERM string in mtones.js is identical to this). Note "Spíritus sancti" WITHOUT ejúsdem in the book.
- Memorial/short conclusions (4°, p. 406):
  Per(h) Chris(i)tum(h) Dó(h)mi(g)num(g) nos(h)trum.(h) ℟. A(g)men.(h)
  Qui vivis et regnas per(h) óm(i)ni(h)a(h) sǽ(h)cu(h)la(h) sæ(g)cu(g)ló(h)rum.(h)

### Tone III: "Orationes ad Horas, et quotiescumque aliae Orationes quae non sunt de corpore Officii et Missae" (pp. 407-408)
- Dó(h)mi(h)nus(h) vo(h)bís(h)cum.(f) ℟. Et(g) cum(g) spí(g)ri(g)tu(g) tu(g)o.(h)  O(h)ré(h)mus.(f)
  (= gabc/op13-palm-benedictio-dv.gabc, p. 20)
- FLEXIO: syllables after the last accent to RE (f): tri(h)stí(h)ti(f)a(f) ;
- ELEVATIO: syllable just before the accent RE, the one(s) before it MI: sa(h)lú(h)te(g) gau(f)dé(h)re(h) :
  pér(h)fru(g)i(g) læ(f)tí(h)ti(h)a(h) :
- Conclusions: Fí(h)li(h)um(h) tú(h)um(f) , qui tecum ... Spí(h)ri(h)tus(h) sanc(g)ti(f) Dé(h)us(h) :
  per ómnia sǽcula sæculó(h)rum(f).   Per(h) Chris(h)tum(h) Dó(h)mi(h)num(h) nos(h)trum(f). ℟. A(g)men.(h)
- Quando Episcopus celebrat: Humiliáte vos ad benedictiónem (not needed).
- Applies to: Palm Sunday blessing of palms (Proc. p. 20: "benedicat eo tono, quo dicuntur Orationes ad
  Horas"; Proc. pp. 20-21 prints the prayer pointed with flex signs: use that pointing), the closing prayer
  of the Palm procession (Missal: "dicat Orationem eo modo quo dicitur ad Horas"), Maundy Thursday absolution
  before Mass (Missal: "Quæ sequuntur, dicat eo modo, quo dicuntur Orationes ad Horas": Dóminus vobíscum,
  Orémus, Exaudi ... Per Christum, and the absolution Dóminus Jesus Christus ... ℟. Amen), Thursday prayer
  at the altar of repose (Deus qui nobis ... Qui vivis et regnas per ómnia).

## 2. Lessons and prophecies (IV, pp. 408-413) = "Prophetias in Missa"
Verse = up to "."; within it at most flex then mediation (Capitula rules p. 402), repeated alternately in
long verses (lessons only). Short verse: no flex; shorter: no mediation either.
- FLEX (‡ / Missal ;): after the last accent to RE: Ec(h)ce vé(h)ni(h)o ci(h)to(f) ‡ ; té(h)ne(f)bris(f) ‡ ;
  magní(h)fi(h)cas e(h)um(f) ‡.  Last word monosyllable or Hebrew: NO flex ("Non flectuntur ... ").
  (p. 409 prints Ec(g)ce(g) at the start: unexplained, ignore like the oration anomaly.)
- MEDIATION (:): two syllables before the last accent MI RE, accent and rest FA:
  vi(h)dit(h) lu(g)cem(f) mag(h)nam(h) : ; e(h)rat i(h)ná(h)nis(g) et(f) vá(h)cu(h)a(h) : ;
  only one syllable available -> RE: Et(f) á(h)li(h)bi(h) :
  last word monosyllable/Hebrew -> last three syllables MI RE FA: me(g)cum(f) est(h) : ; Is(g)ra(f)el(h) : ;
  ra(h)dí(h)ce(g) Jes(f)se(h) :
- TERMINATION at "." (4°-5°, p. 410-411): the unaccented syllable before the last accent RE (two, if it is
  the last syllable of a dactyl), the accent MI, syllables after it LA (c):
  Fra(h)ter Jo(f)án(g)nes.(c)  Grá(h)ti(f)a(f) ple(g)na.(c)  ad(f) tú(g)mu(c)lum.(c)  in(f) fí(g)de.(c)
  di(h)es(f) mé(g)i.(c)  Dó(h)mi(f)nus(f) Dé(g)us.(c)  Pec(f)cá(g)vi.(c)  Ab(g)sit.(c)
  If the syllable before the accent is itself accented (accented monosyllable, Hebrew final) it stays FA:
  cor(h) mé(g)um.(c)  non(h) á(g)li(c)us.(c)  Je(h)sus(h) Chris(g)tus.(c)  Na(h)than(h) dí(g)cens.(c)
  (so "non", "cor" count as accented; prepositions in/ad do not; Jesus/Nathan are Hebrew = final accent)
  If the LAST syllable is accented (monosyllable / Hebrew) the one before is always RE, final MI, no LA:
  A(h)pud(h) te(f) est.(g)  Con(h)ver(h)sá(h)tus(f) est.(g)  Mi(h)sé(h)ri(f)cors(f) est.(g)  Is(h)ra(f)el.(g)
- 6° Termination also at ":" when the author introduces direct speech: Hæc(h) di(h)cit(f) Dó(g)mi(c)nus(c) :
  Et(h) di(h)xit(h) ad(f) me(g) :   (implement: member contains dicit/dixit/ait/dicens/dicentes/inquit/
  respondit..., and the next member starts with a capital).
- 7° Reported words (not spoken / already said): no termination before them, no question inflexion
  ("also in Epistles and Gospels"); the example on p. 411 is ambiguous (notes do not fit the other rules):
  ignore.
- 8° (homilies) not needed.
- 9° QUESTIONS (p. 412): begin at the interrogative word; inside, only a flex, no mediation; at "?" like
  the mediation but the accent only to MI, syllables after it FA:
  ap(h)pó(h)nis er(h)ga(h) e(h)um(g) cor(f) tú(g)um(h) ?   monosyllable/Hebrew end: the final gets MI-FA
  joined: e(h)du(h)xís(g)ti(f) me(gh) ?  Quæ(gh) ?  de(h)um(h) A(g)cha(f)ron(gh) ?
- 10° Ends with Tu autem / Hæc dicit Dominus Deus: Convertimini (Office only).
- 11° Lesson that does not end with Tu autem or Hæc dicit (= Mass prophecies): the end inflected a
  semitone at the last accent: Dí(h)cit Dó(h)mi(h)nus om(h)ní(g)po(g)tens.(g)  In sem(h)pi(h)tér(g)num.(g)
  Fí(h)li(h)is Is(h)ra(h)el.(g)  Con(h)ver(h)sá(h)tus(h) est.(g)  quod pa(h)trá(g)rat.(g)

## 3. Epistle (V, pp. 414-420) and Gospel (VI, pp. 424-430)
Checked against js/mtones.js (Harrison 1920): same rules. Epistle: no flex; mediation = RE on the
unaccented syllables before the penultimate accent, that accent FA, MI to the last syllable, last FA
(mtones mediationL: matches "In(f) íl(h)lo(g) tém(g)po(g)re(h) :" p. 424); questions on MI, last FA, final
monosyllable MI-FA (matches); verse ends p. 417 "fit elevatio vocis ad penultimum accentum" (examples
Ad Ro-má-nos, Ad Co-rín-thi-os ... on p. 417, pdf 433: begin with podatus h-i on the penultimate accent:
looks like mtones termEp; not compared note by note yet); final modulation in two parts (6°, p. 418-419,
= mtones conclusion()).
Gospel: "Omnia ut supra in Epistolis, excepta terminatione Versuum, quæ fit ... flectendo uno semitonio
accentum ultimum et syllabas quæ sequuntur ... (ut in fine Lectionum, n. 11)" = mtones termEv.
DIFFERENCES found (implement as new functions, do not change the live API used by app.js):
- Hebrew names (Jesus/Jesu, Israel, Jacob, David, Sion, Nathan, Jesse, Aaron, Edom, Bosra, Ephraim,
  Emmanuel, Acharon...) carry the accent on the LAST syllable (p. 424 Lo(h)quén(h)te(f) Je(f)su(h) ad(g)
  tur(g)bas(h) :, p. 425 Gé(h)nu(h)it(h) Ja(h)cób.(g)); psalm.js analyse() puts it on the first.
- A final monosyllable takes the cadence alone (p. 425 Non(h) sum.(g); p. 413 Conversátus est(g)), whereas
  mtones lastAccent() goes back to the previous polysyllable.
- Gospel announcement p. 424 = mtones sequentia() + the tone-II Dominus vobiscum above (Proc p. 23 /
  op13-palm-evangelium-dv identical).

## 4. Which tone where (Missale O.P. 1939 rubrics, tools/hw39/*.src)
- Collects, Postcommunions, Super populum (Mon-Wed), Good Friday "Deus a quo" and the 9 solemn prayers AND
  their biddings ("Oremus, dilectissimi": the rubric calls them Orationes, "In fine hujus Orationis non
  respondeatur Amen"), Holy Saturday 5 prayers after the lessons + collect + Postcommunion at Vespers,
  Thursday collect + Postcommunion: tone II. Lenten 2nd/3rd orations (lent_or.src, lent_pc.src, INC'd
  Mon-Wed): tone II, "Orémus" before the 2nd, one conclusion after the 3rd ("Per eúmdem").
  Conclusions printed abbreviated (Per Dóminum., Qui tecum vivit., Per eúmdem.): expand in the gabc only.
- Mon/Tue/Wed second collect line "Dóminus vobíscum. Orémus. Flectámus..." -> add a DV+Orémus gabc before
  the existing G op-m39-flectamus. Wednesday first collect (rubric: no Dominus vobiscum, but Orémus):
  add G op13-quad6f-oremus before op-m39-flectamus.
- Epistles in the Epistle place (Palm Sunday Phil 2, Mon Is 50, Tue Jer 11, Wed 2nd lesson Is 53, Thu
  1 Cor 11, Sat Col 3): mtones epistleTitle + reading(false).
- Gospels Mon (Jn 12), Thu (Jn 13), Sat (Mt 28), Palm blessing Gospel Cum appropinquasset (announcement
  already in op13-palm-evangelium-dv; body only), Thursday Sermo Domini Jn 13-17 in Quad6h_mand.src
  (rubric: "dicat tono cantus Evangélii: Dóminus vobíscum ... legat solémniter Evangélium": Gospel tone,
  31 paragraphs, conclusion only on the last).
- Lesson tone (IV): Wednesday 1st lesson (Is 62-63), Good Friday Osee (read by a friar; Prior reads it
  "submissa voce" meanwhile) and Exodus 12 ("in tono Lectionis" explicit), Holy Saturday 4 lessons ("legantur
  sine titulo ... in loco in quo Epistola"); end by rule 11. Better pointing: copy the Triduum 1927 flex
  signs/colons onto the Missal words (OCR with tesseract is available).
- STAY TEXT (rubric): Holy Saturday blessing of the fire ("absque Dóminus vobíscum, et absque Orémus,
  legendo sine nota, benedicat ignem"); Secrets (said secretly); Canon (Communicantes, Hanc igitur);
  Mandatum prayers Actiones nostras / Adesto ("dicat húmili voce"); Good Friday Libera nos (no tone in the
  Missal appendix; uncertain); Thursday preces "Et ne nos ... Dómine exáudi" (no Dominican source in hand).
- Already notated, leave: Exsultet, Litany, Passions (separate task), Palm procession chants, Pater/Per
  omnia on Good Friday.

## 5. How to resume
1. Add to js/mtones.js (new names, old API unchanged): orationOP(text, {tone:'II'|'III', oremus, dv}),
   lessonOP(text, {final:true}), and optionally readingOP with the Hebrew/monosyllable fixes. Node needs
   `globalThis.window = globalThis; require('./js/psalm.js'); require('./js/mtones.js')`.
2. tools/hw39/mktones.js: list of items {id: op-hw-<day>-<n>, src file, T-line prefix, kind, opts}; read the
   Latin from the .src (exact Missal words), j->i, expand conclusions, write gabc/op-hw-*.gabc with header
   "Set to the Dominican <...> tone (Proc. O.P. 1913 p. X / Harrison 1920 p. Y); text from Missale O.P. 1939
   p. Z", then insert "G: op-hw-...|label" right before the T block (after L: Oratio).
3. Check: cd /tmp && gregorio -o x.gtex FILE for each; python3 tools/hw39/build.py; serve
   (python3 -m http.server 8765) and load holyweek.html#Quad6&d=2027-03-21 ... #Quad6s&d=2027-03-27 with
   localStorage hwRite=1939 in headless Chrome (/usr/bin/google-chrome, playwright): no console errors,
   no "could not be drawn".
Helper used for reading staves: /tmp/omr/notes.py (crude; read by eye at 400 dpi instead).
