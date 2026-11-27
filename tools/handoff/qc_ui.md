# QC walkthrough: Mass side of UltraPheonix/dominican-liturgy

Read-only. No repo file was edited and nothing was committed.

- **Code audited:** commits up to `b0d68ae` (12:07 on 27 Nov 2026). The repo was being committed to during the run: "Requiem rebuilt from the Missale O.P. 1939" landed at 11:59, then `00e68e3` (Asperges) and `96868f7` (Processions).
- **Effect on the results:** my first pass (`/tmp/qc/s1/`) was partly stale, so every page was re-run against the new code (`/tmp/qc/s2/`). All quotes below come from the re-run, unless marked s1.
- **Harness:** Python Playwright with `/usr/bin/google-chrome` at 1280×900. Each URL got a new page. The script waited until no `.loading` placeholders were left, then took a full-page screenshot, cut it into 1600-px JPEG crops (`NAME_cK.jpg`), and saved `#mass` innerText (`NAME.txt`). It also collected console errors and warnings, page errors and HTTP status ≥ 400. Per-page data is in `res.json` in each folder.
- **Pages visited:**
  - 111 Mass pages for 104 distinct dates from Nov 2026 to Nov 2027, plus alternative Masses (`/tmp/qc/s2/`).
  - 30 Order-of-Mass variants: Low, Sung, Solemn, Conventual, Full rubrics, Latin+English (`/tmp/qc/s4/`).
  - Holy Week, the three booklets, About, Rubrics and Prayers (`/tmp/qc/s3/`).
  - The year's Mass assignments as `/tmp/qc/year.txt`.
- **JS errors:** none. No console errors, page errors or 404s on any of the 157 page loads. Every chant rendered (after waiting).
- Severity groups: **BROKEN** (wrong output a user will act on), **WRONG** (contradictory or incorrect text), **CLUNKY** (wording), **COSMETIC**.

---

## BROKEN

### B1. Epiphany has no Gloria, uses Kyriale VIII and ends with Benedicamus Domino
- URL: `index.html#Epi&d=2027-01-06`
- Screenshot: `/tmp/qc/s2/d2027-01-06_c0.jpg`
- Quote: "Kyriale: Missa VIII (Profestis diebus) · no Gloria · Credo · Preface of the Epiphany · Benedicamus Domino". The pill reads "White · Totum Duplex, I class".
- Cause: in `js/app.js`, `rubricsOf` calls `teDeumDay(r)`. Jan 6 is ranked `office.kind === 'temporal'`, so the function falls through to `return /^(Pasc0|Pent0|Dec25)/.test(t.key)`, which does not match `Epi`. The booklets inherit the same error.
- Fix: in `teDeumDay`, return true for `t.key === 'Epi'`. Better still, return true for any temporal office whose rank is Totum Duplex.

### B2. The weekly conventual Requiem uses the wrong prayers, by the site's own Rubrics page
- URLs: `index.html#C114s&d=2026-11-27`, which is also today's `index.html`. The same applies on 2026-12-17, 2027-01-26, 2027-04-07 and 2027-06-21.
- Screenshot: `/tmp/qc/s4/req_low_c1.jpg`; text in `/tmp/qc/s4/req_low.txt`
- Shown:
  - 1st prayer: "Deus, qui inter apostólicos Sacerdótes, fámulos tuos Pontificáli vel Sacerdotáli…"
  - 2nd: "Deus, véniæ largítor"
  - 3rd: "Omnípotens sempitérne Deus, qui vivórum"
- The Rubrics page, Rubr. gen. XII.6, says: "If Mass is celebrated for the brethren, familiars and benefactors on the first unimpeded day of the week… the first Prayer is Deus, veniae largitor, the second Deus, qui nos Patrem; the third is unchanged."
- "Deus, qui inter apostolicos" is prescribed only "if it is not known for whom Mass is to be celebrated" (XII.5). The Secret and Postcommunion are wrong in the same way.
- Fix: for C114s used as the weekly conventual Requiem, take the prayers from XII.6: Deus veniae largitor / Deus qui nos Patrem / Omnipotens… qui vivorum. Apply the same change to the matching Secrets and Postcommunions.

### B3. The Introit of every Requiem prints its repeat twice
- URLs: All Souls `index.html#S1102&d=2026-11-02`, the conventual Requiem, and the anniversaries.
- Screenshots: `/tmp/qc/s1/d2026-11-02_c0.jpg` (the s1 shot of the same page; the code in question had not changed); `/tmp/qc/s4/req_low_c0.jpg`
- Quote (end of the Introit): "…ad te omnis caro véniet. Repet. Réqui-em. Ant. Réqui-em". In Low Mass text it reads "Repet. Réquiem. Ant. Réquiem ætérnam dona…".
- Cause: `fullIntroit()` in `js/app.js` (around line 140) checks `/repetitur|<i>[^<]*Ant\.?<\/i>/` to see whether the book already shows the repeat. The Requiem GABC writes `<i>Repet.</i>`, so the check misses it and a second "Ant." cue is appended. The same happens in the text version (Low Mass and Latin+English).
- Fix: add `Repet` to the regex, i.e. `/repetitur|<i>[^<]*(Ant|Repet)\.?<\/i>/i`.

### B4. Twenty-five readings stop in mid-sentence (OCR page-break cuts in `data/readings33.js`)
- Example URL: `index.html#S1129v&d=2026-11-28`
- Screenshot: `/tmp/qc/s2/d2026-11-28_c1.jpg`
- Quote: the lesson ends "…et circumcínxit eum zona justítiæ, et índuit eum" with no full stop.
- Others:

| Key | Reading | Ends with |
|---|---|---|
| Epi | Isaias 60 | "…Dómino annuntiántes. Omne" |
| Adv2 | Romans 15 | "…et magnificáte eum omnes" |
| Quad1h | Ezechiel 18 | "…vita vivet, ait Dóminus" |
| Quad1f | Ezechiel 18 | "…Et cum avérterit se ímpius" |
| Quad2h | Jeremias 17 | "…in desérto, in" |
| Quad5m | Jonas 3 | "…et misértus est" |
| Pasc0h | Acts 8 | "…Generatiónem" |
| Pent0s | Deuteronomy 26 | "…Dóminus Deus tuus déderit tibi" |
| Pent22 | Philippians 1 | "…in glóriam" |
| C30s, S0603, S1211 | Matthew 24 | "…super ómnia bona sua" |
| C62s | 1 Corinthians 11 | "…Itaque quicúmque" |
| C85s | Ephesians 4 | "…sicut est véritas in" |
| S0122 | Ecclus 14/15 | "…et" |
| S0424 | Canticle 3/4 | "…coronáberis" |
| S0430 | Matthew 13 | "…Aliam" |
| S0822 | Ecclus 24 | "…omnis viæ et" |
| S0908, S1207v | Matthew 1 | "…de qua natus est Jesus, qui" |
| S0119b | Luke 10 | "…regnum Dei. In" |
| S0920, S0920v, G369, S1129v | Ecclus 44/45 | "…et índuit eum" |

- Fix: re-read each against the Missal page that follows. The list comes from scanning `la` fields that end without punctuation.

### B5. The Saturday-of-Our-Lady private Mass of an Advent Sunday gets Gloria and Ite
- URL: `index.html#Adv1&d=2026-12-05` (the "Mass of the Sunday (private Masses)" chip)
- Screenshot: `/tmp/qc/s2/d2026-12-05_Adv1_c0.jpg`
- Quote: "Violet · Mass of the Sunday (private Masses)" with "Kyriale: Missa VI · Gloria · no Credo · Common Preface · Ite, missa est".
- Cause: `teDeumDay` returns true for a `bvmSat` office (`return t.season !== 'sept'`), and the resumed Sunday Mass "follows the day". A violet Advent Sunday Mass never has the Gloria.
- Fix: in `rubricsOf`, force `gloria = false` when the Mass itself is a penitential temporal Mass (Adv, Septuagesima, Lent), whatever the office.

### B6. 4 Feb 2027 shows the wrong feast
- URL: `index.html#S0430&d=2027-02-04`
- Screenshot: `/tmp/qc/s2/d2027-02-04_c0.jpg`
- Quote: the title is "S. Catherinæ Senensis, O.P., V." and the pill is "White · Totum Duplex · Septuagesima–Lent".
- `KAL39["0204"]` gives S. Andreæ Corsini (Duplex) and the Anniversarium Patrum et Matrum. S0430 is the key that `KAL39["0401"]` uses for the Impressio SS. Stigmatum S. Catharinæ. That feast has apparently been "transferred" from 1 April (impeded by Holy Week 2026 or Easter week 2027) forward almost a year, to 4 Feb 2027.
- Fix:
  - In `mrank.js`, cap the forward search for a transfer, for example to within the same liturgical year.
  - Make the title the Stigmata feast ("Impressio SS. Stigmatum…"), not "S. Catherinæ Senensis".

### B7. 13 Nov shows St Thomas's March feast instead of his Patronage
- URL: `index.html#S0307&d=2026-11-13`
- Screenshot: `/tmp/qc/s2/d2026-11-13_c0.jpg`
- Quote: "S. Thomæ Aquinatis O.P. C. D." / "St. Thomas Aquinas, OP", with no mention that this is the "Patrocinium S. Thomæ Aq. in Scholas catholicas" (`KAL39["1113"]`).
- Fix: when a calendar entry reuses another feast's Mass key, show the calendar entry's own title, here "Patrocinium S. Thomæ…".

### B8. Palm Sunday on the Mass page is an empty stub with controls that do nothing
- URL: `index.html#Quad6&d=2027-03-21`
- Screenshot: `/tmp/qc/s2/d2027-03-21_c0.jpg`
- The page shows only "Holy Week has its own section, with the whole rite of each day as the Missal gives it, in the traditional (1939) and the reformed (1959) form." It also shows an "Open in Holy Week ›" button whose label is nearly invisible (very pale on white).
- The Propers/Low/Sung/Solemn/Conventual, Latin/English and Print & share controls stay visible and do nothing.
- Fixes:
  - Hide the massbar on this stub.
  - Give the button readable contrast.
  - Drop "and the reformed (1959) form" from the text: the 1959 form is hidden by default and the site is pre-1955.

---

## WRONG

### W1. The "Kyrie" link in the jump bar scrolls to the Asperges on every Sunday
- URLs: every Sunday, e.g. `index.html#Adv1&d=2026-11-29`, plus 11-08, 11-22, 12-06, 12-13, 12-20, 2027-01-03/10/17/24, 02-14, 03-14, 03-28, 04-04, 04-25, 05-16, 05-23, 05-30, 07-11, 08-15, 10-03 and 10-31.
- Screenshot: `/tmp/qc/s2/d2026-11-29_c0.jpg`
- Quote (DOM): `<section data-part="as" id="ordinary">` … `<section data-part="ky" id="ordinary">`. Both sections carry `id="ordinary"`, so `<a href="#ordinary">Kyrie</a>` lands on the Asperges.
- Fix: give each Ordinary slot its own id (`ord-as`, `ord-ky`, …) and point the jump links at them.

### W2. Requiem labels for the 2nd and 3rd prayers repeat the Collect's incipit
- URLs: `index.html#C114s&d=2026-11-27` (all forms)
- Screenshot: `/tmp/qc/s4/req_low_c3.jpg`
- Quote: "2nd prayer · For our deceased brethren, relatives and benefactors · Deus, véniæ largítor". The prayer printed beneath it is "Deus, cuius misericórdiæ non est númerus…" in the Secret and "Præsta, quǽsumus, omnípotens et miséricors Deus…" in the Postcommunion.
- In the same way, "3rd prayer · For the living and the dead (another) (n. 38) · Omnípotens sempitérne Deus, qui" sits above "Deus, cui soli cógnitus est…" and "Puríficent nos…".
- Fix: in the Secret and Postcommunion, give the label without the incipit ("2nd prayer · for the brethren, relatives and benefactors"), or with that prayer's own incipit.

### W3. The solemn Requiem says the ministers go in "when the choir begins the Gloria Patri"
- URL: `index.html#C114s&d=2026-11-27&ordo=solemn&rub=full`
- Screenshot: `/tmp/qc/s4/req_solemn_full_c0.jpg`
- Quote: "When the choir begins the Gloria Patri of the Introit, the ministers go to the altar…". A Requiem Introit has no Gloria Patri (Rubr. IV: "non dicitur Gloria Patri post Introitum").
- Fix: when `R.requiem`, read "When the choir begins the verse Te decet of the Introit…", or follow the Missal's own wording for Masses of the dead.

### W4. The solemn Requiem keeps the deacon's blessing before the Gospel
- URL and screenshot: as W3, crop around `/tmp/qc/s4/req_solemn_full_c5.jpg`
- Quote: "℣. Iube, domne, benedícere. … Dóminus sit in corde tuo et in lábiis tuis…". Rubr. IV (Rubrics page): "…nec Dominus sit in corde meo… in Missa pro Defunctis".
- Fix: check against the Missal's ceremonial for the deacon in a Requiem. If it is omitted, filter it out when `R.requiem`.

### W5. The anniversary Masses show one prayer and the same second prayer all year
- URL: `index.html#S1113&d=2026-11-10`
- Screenshot: `/tmp/qc/s2/d2026-11-10_c0.jpg`
- Quote: one prayer only, "Deus indulgentiárum Dómine… quorum anniversárium depositiónis diem commemorámus".
- Rubr. XII.7 gives the four Order anniversaries three prayers: 2nd Deus veniae largitor, but "in the February one… Deus, qui nos Patrem, and in the July one… Deus, cujus miseratione". XII.1 says one prayer for the Masses in VI.3-7, so the rubrics need reconciling.
- All four anniversaries (Feb 4, Jul 12, Sep 5, Nov 10) also use the one key S1113, titled "Anniversarium Omnium Fratrum et Sororum Ordinis".
- Fix: decide whether XII.1 or XII.7 governs, then give the February and July anniversaries their own second prayer and their own title.

### W6. A week with no free day for the Requiem gets no "Omnipotens… pro vivis et defunctis" prayer
- URL: `index.html#S1202&d=2026-12-02`
- Screenshot: `/tmp/qc/s2/d2026-12-02_c0.jpg`
- The week of 29 Nov to 5 Dec 2026 has no Requiem day. The Simplex on 2 Dec shows only "2nd prayer · Commemoration: I Adventus / 3rd prayer · Of Our Lady (Advent)".
- Rubr. VI.2 says that "on another, less solemn day of the week the Prayer Omnipotens for the Living and the Dead is added, after the Prayers prescribed by the Rubrics".
- Fix: when `requiemDay()` returns null for the week, add that prayer on the least solemn day.

### W7. The Requiem is named three different ways
- Main page title: "Missa pro Defunctis (in Missis quotidianis)"
- Day pill: "Conventual Mass for the dead (the week's first free feria)"
- Booklet: "Mass for the Dead (daily and conventual)"
- Screenshots: `/tmp/qc/s4/req_low_c0.jpg` and `/tmp/qc/s3/book_choir_req_c0.jpg`
- The conventual Requiem is the Mass for the brethren, relatives and benefactors (XII.6), not the "in Missis quotidianis" Mass.
- Fix: title it "Missa pro Defunctis (conventualis)" with the English "Conventual Requiem for the brethren, relatives and benefactors", and use the same name everywhere.

### W8. The Requiem summary line is hard-coded
- Quote (every black Mass): "Mass for the Dead · Kyrie (Requiem) · without Gloria or Credo · Sequence Dies iræ · Preface for the Dead · Agnus Dei with dona eis requiem · Requiescant in pace"
- The string is a literal in `rubricLine()`, so it cannot change with the day. Check whether the Dies iræ is obligatory at the daily and conventual Requiem in the 1939 Missal (Rubr. XIII).
- The line also repeats information the page already shows.
- Fix: build the line from the parts actually present. Suggested: "Requiem · no Gloria or Credo · Dies iræ · Preface for the Dead".

### W9. Daily Easter-season ferias show no Gloria
- URL: `index.html#Pasc1&d=2027-04-08` (Thursday after Low Sunday)
- Screenshot: `/tmp/qc/s2/d2027-04-08_c0.jpg`
- Quote: "White · Feria" with "Kyriale: Missa VIII (Profestis diebus) · no Gloria · no Credo · Preface of Easter · Benedicamus Domino".
- In Paschaltide the Te Deum is said at ferial Matins, and so the Gloria at the ferial Mass. `teDeumDay` returns false for every temporal feria outside the Easter and Pentecost octaves.
- The English subtitle "Low Sunday (The Octave of Easter)" on a Thursday is also misleading.
- Fix: verify against the Breviary rubric, then make Paschaltide ferias return true. Add "(Mass of the preceding Sunday)" to the subtitle.

### W10. Easter Kyrie IV is missing on some I and II class feasts in Paschaltide
- URLs: `index.html#Pasc2w&d=2027-04-14` (Solemnity of St Joseph, I class) and `index.html#S0505&d=2027-05-05` (St Pius V, II class)
- Screenshot: `/tmp/qc/s2/d2027-04-14_c0.jpg`
- Quote: "Kyriale: Missa VI · Gloria · Credo · Preface of St Joseph". Yet the site's own hint says "In Paschaltide the Easter Kyrie is sung on Sundays and on feasts of the I and II class." St Peter Martyr (II class) does get "Missa III, Kyrie IV".
- Fix: apply `paschalKyrie()` to every I and II class feast in Paschaltide, and check why Pasc2w and S0505 get Missa VI.

### W11. The Holy Name Sunday lists the Christmas Masses as alternatives on 30 Dec
- URL: `index.html#Nat1&d=2026-12-30`
- Screenshot: `/tmp/qc/s2/d2026-12-30_c0.jpg`
- Quote: the pill reads "White · Feria" while the title is "Sunday within the octave of Christmas", and the chips read "Also today / At midnight: Nativitas Domini, Missa ad media noctem / At dawn: Nativitas Domini, Missa ad matutinam".
- The midnight and dawn Masses belong only to 25 December. The pill should say "Sunday within the octave (transferred)".
- Fix: offer `Dec25_1` and `Dec25_2` only when the date is 12-25, and label a transferred Sunday as such.

### W12. Five chant translations cite the wrong Scripture reference
These show in the booklet heading and the congregation booklet.
- URL: `booklet.html?b=choir#Adv1&d=2026-11-29`
- Screenshot: `/tmp/qc/s3/book_choir_adv1_c0.jpg`
- Quote: Officium "Ad te levavi" is marked "Ps. 142 · Grad. O.P. p. 1". It is Ps. 24:1-3.
- All five references found have descending verse ranges:

| Chant id | Shown | Chant |
|---|---|---|
| 5367 | "Ps. 142, 8-3" | Ad te levavi |
| 4284 | "Ps. 118, 137-124" | Justus es Domine |
| 6841 | "Ps. 37, 22-8" | Ne derelinquas me |
| 7015 | "John 15, 5-1" | Ego sum vitis |
| 8003 | "Ps. 118, 46-1" | Loquebar |

- Fix: correct `D.trans[id].r` for these five.

### W13. The Adv1 Epistle's English runs past the Latin, and similar mismatches elsewhere
- URL: `index.html#Adv1&d=2026-11-29` (Latin+English)
- Quote: the Latin ends "…sed induímini Dóminum Jesum Christum." The English continues "…and make not provision for the flesh in its concupiscences."
- A length-ratio scan (English/Latin > 1.45) points to likely truncated Latin, or over-long English, in:
  - Epi (Isaias 60, 1.52)
  - S0122 (1.83)
  - S0430 Gospel (1.66)
  - Quad5w (1.62)
  - S0211 and G420 (1.59)
  - Quad5f (1.54)
  - Pent0s, Adv3s (1.49)
- Two lessons have no English at all, and their references are malformed: S0611 (St Barnabas) "Actus Apostolorum 11, 13" and S0722 (St Mary Magdalen) "Canticum Canticorum 3, 2, 8".
- Fix: trim the English to the Missal's pericope. Add English and proper references for S0611 and S0722.

### W14. Ash Wednesday Gospel typo
- URL: `index.html#5aw&d=2027-02-10`
- Text: `/tmp/qc/s2/d2027-02-10.txt`
- Quote: "Amen dico bis, quia recepérunt mercédem suam". It should read "Amen dico vobis". The source is `data/readings33.js` (5aw Gospel).

### W15. "Ministers" appears in the Low Mass rubrics
- URL: `index.html#C114s&d=2026-11-27&ordo=low`
- Screenshots: `/tmp/qc/s4/req_low_c0.jpg`, `/tmp/qc/s4/req_low_c2.jpg`
- Quotes: "Then the ministers repeat the Confession, and where the priest said vobis, fratres…" and "The ministers answer Gloria tibi Domine:". At Low Mass there is one server.
- Fix: when `ordo === 'low'`, write "the server".

### W16. "Roman ref." readings appear where they don't fit
Roman-borrowed readings were found on only 2 of 104 dates.
- **B. Margaret of Savoy, a widow:** `index.html#S1127b&d=2026-12-23` (screenshot `/tmp/qc/s2/d2026-12-23_c0.jpg`).
  - Badges: "Epistola Apocalypsis 12: 1,5,14-16 [Roman ref.]" and "Evangelium Joannes 2: 1-11 [Roman ref.]".
  - These are Marian readings (the Woman clothed with the sun, Cana). They look borrowed from the wrong Mass.
- **Translation of St Dominic:** `index.html#S0524&d=2027-05-24` (screenshot `/tmp/qc/s2/d2027-05-24_c0.jpg`).
  - Badges: "Ecclesiasticus 31: 8-11 [Roman ref.]" and "Lucas 12: 35-40 [Roman ref.]".
  - Their Dominican source should be easy to find.
- The s1 pre-rebuild Requiem also had "Apocalypsis 14: 13 [Roman ref.]". The rebuilt one no longer does.

### W17. The Requiem preface header says "tono feriali" at Low Mass
- Quote (Low Mass): "Praefatio Pro Defunctis tono feriali". There is no chant tone at a Low Mass.
- Fix: drop the tone label when `ordo === 'low'`.

### W18. About page versus the other pages
- **"Human verified":** About (`/tmp/qc/s3/about_c0.jpg`) says "All of the work has been human verified, and all its sources have been verified." Rubrics and Prayers say "The English is an AI translation (made with Claude) and has not yet been checked by a human translator". Chants carry "AI translation" tags.
- **Missing source:** recent commits cite the "Graduale O.P. 1928" throughout, but it is not in the About sources list.
- **1950 claim:** the booklet footer says "All chants from the Graduale… (Rome, 1950)", but the Requiem chants are now from 1928.
- Fix: reword the disclaimer to "checked by hand where marked; AI translations are labelled", add the 1928 Graduale, and make the booklet footer generic.

### W19. Calendar items to verify
These came from `/tmp/qc/year.txt` and the pills. Not certain, but each looks off:
- **Vigil of the Epiphany** (`index.html#Jan5a&d=2027-01-05`): "Violet · Vigil", no Gloria, Benedicamus. The Roman pre-1955 vigil was white, with Gloria and Credo, in Christmastide. Check the Missal O.P.
- **Pentecost Vigil** (`#Pasc6s&d=2027-05-15`): "Gloria · Credo". Check whether the Credo belongs.
- **Annunciation 2027** is placed on Tue 6 Apr, with Vincent Ferrer (II class) on Mon 5 Apr. Normally the transferred I class feast takes the first free day.
- **Ss Philip and James** on 1 May are titled "11 Maii —" in the Mass title (`year.txt`). The same date-prefix problem shows on B. Emily Bicchieri ("3 Maii —" on 19 Aug), the Anniversary ("13 Nov." on 10 Nov), and B. Margaret ("27 Nov." key on 23 Dec).
  - Fix: strip the date prefix from any title shown on a date other than its own.
- **St Blaise and Ss Vitus etc. ("Tres Lectiones")** get no Gloria and Benedicamus. Simplex days such as St Bibiana get Gloria and Ite.
  - This follows `teDeumDay` ("never on feasts of three lessons"), but the octave-day exception shows the rule is unsure. Worth checking with the Ordo.

---

## CLUNKY (rubric wording, with suggested rewrites)

### C1. 2nd and 3rd prayer headers repeat the prayer printed beneath them
- Example: `index.html#S1129v&d=2026-11-28` (`/tmp/qc/s2/d2026-11-28_c0.jpg`)
- Quote: "2nd prayer · Of Our Lady (through the year) · Concéde nos fámulos" followed by "Concéde nos fámulos tuos…".
- Suggested: "2nd prayer — of Our Lady".

### C2. The ad libitum picker is verbose
- Same page.
- Quote: "3rd prayer (at the priest’s choice)" [select: None] and "Missal, Rubr. gen. X.1: the 3rd prayer is at the priest’s choice today, from the Orationes ad diversa."
- Each option reads like "1. For the prayers of all the Saints · Concéde, quǽsumus omn…", across 37 options.
- Suggested: label "3rd prayer (ad libitum, Rubr. X.1)". Drop the second sentence. Group the options by heading (Of the Saints / For the living / For the dead).

### C3. Label for the third Requiem prayer
- Quote: "For the living and the dead (another) (n. 38)".
- Suggested: "3rd prayer · for the living and the dead".

### C4. Low Mass Offertory and Lavabo rubrics (`/tmp/qc/s4/req_low.txt`)

| Quote | Suggested |
|---|---|
| "Then, going to the Epistle corner for the washing of the fingers, he says (and no further):" | "At the Epistle corner he washes his fingers, saying:" |
| "This said, standing erect and turning to the people, extending and joining his hands, he says in a moderate voice Orate fratres, these two words only, continuing the rest secretly:" | "He turns to the people and says aloud Orate, fratres; the rest secretly:" |
| "and Oremus. Then, with hands extended, he says the Secret prayer or prayers; when they are finished, at the conclusion, he says in a clear and audible voice Per omnia saecula saeculorum, with the Preface proper to the Mass." | "Oremus, and the Secret(s); the conclusion Per omnia saecula saeculorum aloud, then the Preface." |

The third quote also begins with a lowercase "and".

### C5. Rite and chant headings duplicate each other
- Low Mass shows "Offertorium / Offertory" (the rite) directly followed by "Offertorium / Domine Jesu Christe" (the chant).
- It shows "Communio / Communion" (the rite) and later "Communio / Lux aeterna".
- It shows "Dimissio / Dismissal" followed by "Requiescant in pace / Dismissal".
- Screenshot: `/tmp/qc/s4/req_low_c2.jpg`
- Suggested: rename the rite parts "Ad Offertorium", "Ad Communionem" and "Ad finem".

### C6. The Gospel announcement is printed twice, with I/J spelled differently
- Quote: the rubric section gives "℣. Sequéntia sancti Evangélii secúndum Ioánnem." Immediately below, the Gospel section repeats "Sequéntia sancti Evangélii secúndum Joánnem."
- Suggested: print the announcement once, and normalise I/J (the readings use J, the Ordo and orations use I, e.g. "Iesum" against "Jesum").

### C7. "Ante Evangelium" carries a bare "Requiem" badge
- Quote: "[Requiem] Then, having said the Collect, the Epistle and the Responsory with the Tract, he goes to the Gospel corner…". The Sequence is omitted.
- Suggested: "Then, having said the Collect, Lesson, Responsory, Tract and Sequence, he goes to the Gospel side…", and drop the badge.

### C8. "Actiones nostras" stands at the head of Low Mass with no rubric
- Screenshot: `/tmp/qc/s4/req_low_c0.jpg`. The reader cannot tell when it is said.
- Suggested: add "Before Mass, at the foot of the altar, secretly:".

### C9. The Requiem's "Sanctus" text is printed twice at Low Mass
- Quote: "Sanctus, Sanctus, Sanctus…" ends the Preface, then a full "Sanctus" section follows.
- Suggested: drop the ellipsis line.

### C10. The second conventual Mass chip is confusing
- URL: `index.html#S0712&d=2027-07-12`
- Quote: "Second conventual Mass, sung: Anniversarium sepultorum in Cœmeteriis nostris: Anniversarium Omnium Fratrum et Sororum Ordinis". The 4 Feb chip has the same problem.
- Suggested: "Second conventual Mass (sung): Anniversary of those buried in our cemeteries".

### C11. The "Per annum" season pill is noise on fixed feasts and Requiems
- Quote: "Black · Duplex · Per annum" on All Souls.
- Suggested: show the chant season only when it changes the chants (Paschaltide, Septuagesima–Lent).

### C12. Holy Week Good Friday repeats each Tract as text and as chant
- Screenshot: `/tmp/qc/s3/hw_fri_c0.jpg`
- Quote: "Tractus Habacuc 3 Dómine audívi audítum tuum…" printed as prose, then the same Tract as chant directly below.
- The Rite switch is a single lonely pill, "Traditional, Missale O.P. 1939", next to the tiny link "Show/hide the post-1955 (1959) reform, for reference".

---

## COSMETIC

### K1. Truncated English subtitles

| URL (index.html#…) | Subtitle shown |
|---|---|
| `S1112&d=2026-11-12` | "Feast of All Dominican" |
| `S1208&d=2026-12-08` | "Immaculate Conception of" |
| `S0319&d=2027-03-19` | "St. Joseph, Spouse of the" |
| `S0325&d=2027-04-06` | "The Annunciation of the" |
| `S0511&d=2027-05-01` | "SS. Philip and James," |
| `S0429&d=2027-04-29` | "St. Peter Martyr, O.P" |

Missing English subtitles: S0505 Pius V, S0524, S0712, S0503b, S1127b, CorpusChristi, 7a, C79s.

### K2. Title capitalisation
- "FestivitaS Omnium Sanctorum O.P." (12 Nov, `/tmp/qc/s2/d2026-11-12_c0.jpg`)
- "S. IOSEPHI, SPONSI B. MARIÆ VIRG. C. et Eccl. Univ. Patr." (19 Mar): `clean()` only fixes titles that are more than 70% capitals.
- "S. Petri Martyris, O.P. M. II Cl." (29 Apr): the rank has leaked into the title.

### K3. Drop-cap glitch on the Requiem Agnus Dei
- Screenshot: `/tmp/qc/s1/d2026-11-27_c3.jpg`
- The drop cap "A" is followed by "-gnus De-i" with a stray leading hyphen.

### K4. "Also today" chips wrap without indentation
- Screenshot: `/tmp/qc/s1/d2026-11-02_c0.jpg`
- "Third Mass:" starts at the left margin under "Also today".
- The Christmas Midnight page lists "Nativitas Domini, Missa interdiu" with no "During the day:" label.

### K5. The jump bar is clipped at the right
- Example: "Offertoriu…" on `/tmp/qc/s1/d2026-11-02_c0.jpg` and "Secret…" on `/tmp/qc/s4/req_low_c0.jpg`. There is no fade or scroll hint.

### K6. Rubrics page chapter numbering
- "De defectibus" begins with an unnumbered chapter, and the next heading is "II De defectibus materiae". Label the first one "I".

### K7. Mixed English register in the orations
- Adv1 Secret: "…make us come purer before You Who are their author. Through Jesus Christ, thy Son our Lord, Who liveth…" mixes You with thy.

### K8. Holy Week typography
- Holy Week texts keep a space before the colon ("Dóminus : In tribulatióne").

---

## Not covered or not done
- I did not visually check every crop. I read the text of all pages, and viewed crops for the Requiems, All Souls, the vigil, Palm Sunday, Good Friday and the booklets.
- The Latin+English click on Holy Week used the wrong selector and timed out (`hw_fri_both`).
- Folders and timing:
  - `/tmp/qc/s1/` is stale for anything touched by commits after 11:59 (the Requiem, orations and Asperges). The Asperges commit `00e68e3` landed after `/tmp/qc/s2/` was taken, so Asperges findings may be outdated.
  - `/tmp/qc/s4/` (the Order-of-Mass variants) was produced around 12:10–12:25, after `b0d68ae`.
