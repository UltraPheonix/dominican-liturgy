# Handoff: Mass chat, paused 27 Nov 2026 (site v218)

Start here. Then read tools/RESUME.md (history) and the note for whichever item you pick up.
Every paused job has its own note in this folder:

| Note | Job | State |
|---|---|---|
| litanies.md | Every litany invocation in chant (Processionarium) | Rules read; generator `tools/proc/gen_lit.js` drafted, never run; nothing wired in |
| hw_tones.md | Holy Week priest/deacon tones (orations, lessons, Epistles, Gospels) | Rules transcribed note by note; no gabc written |
| english_1959.md | Prayer English from the St Dominic Missal 1959, verbatim | Extractor in `tools/orat39/dm1959/`; 935/1452 matched; no data changed |
| g28_four_masses.md | Guardian Angels, St Teresa, St Raphael, St Albert (G28) | 7 chants read, 1 partial (`tools/g28/angeli_*`, `teresia_*`); not wired |
| readings_cut.md | 25 readings cut at a page break | Continuations located; 0 fixed |
| proc_tones.md | Processions: versicles and prayers in tone | **Done and live** (reference only) |
| qc_mass.md, qc_ui.md, qc_hw.md | The three QC reports | Partly fixed (see the to-do list below) |

## Standing rules (Joseph)
- **Pre-1955 Dominican rite only.**
  - Use Dominican books only: Missale O.P. 1939/1933, Graduale O.P. 1928/1950, Processionarium O.P. 1913, Triduum O.P. 1927, Ordo 1944.
  - Never the Roman Missal. No Lumen Christi. Nothing from 1955/1959 in the 1939 forms.
- **Chant:**
  - Read GABC note by note from the scan, with a second checking pass. Never infer.
  - Where the book prints only a tone or formula, the text may be set to that printed Dominican tone. The gabc header must then say "set to the … tone, <book> p. N".
- **Communication:** be terse. Send a short status message after each substep, and per-chant / per-Mass updates when agents typeset.
- **After every step:** one quality run and one clarity run before moving on.
- **Push procedure:**
  1. `git pull --rebase`.
  2. Commit as `UltraPheonix <UltraPheonix@users.noreply.github.com>`.
  3. Run `bash tools/push.sh`. It needs a clean tree; it rebases, sets sw.js VERSION to origin's + 1 and pushes.
  4. Send a one-line message to Joseph.
- **Before every push:**
  - `timeout 590 python3 tools/check/mass_sweep.py` must print `cases 224 flagged 0`. It needs a server on port **8768**.
  - Check the changed pages in headless Chrome: playwright, `/usr/bin/google-chrome`, server on port 8765, no console errors.
- **Never touch (the Office chat owns them):** data/office*, tools/b09/, js/office.js, js/tones.js, data/chant/office.json, office.html.
- **Agents:**
  - Tell every agent the rules above.
  - Verify each agent's chant against the scan before wiring it in.
  - Agents don't commit; the coordinator does.

## Environment (recreate if the machine was reset)
```
cd /home/claude/dominican-liturgy
nohup python3 -m http.server 8765 >/dev/null 2>&1 &   # for checks by hand
nohup python3 -m http.server 8768 >/dev/null 2>&1 &   # mass_sweep.py needs this one
```
- **gregorio:** must run from /tmp with a relative output: `cd /tmp && gregorio -o x.gtex /abs/path/file.gabc` (or `gregorio -S`).
- **Mass page URL:** `index.html#KEY&d=YYYY-MM-DD` plus options such as `&ordo=low|sung|solemn|conv`. Open a new page per URL; changing only the hash doesn't reload.
- **Holy Week 1939 form:** localStorage `hwRite=1939`.

### Source books (local path ← download)
| Book | Local | URL |
|---|---|---|
| Missale O.P. 1939 | /home/claude/dl/missal/M39.pdf; text tools/orat39/m39lin.txt | https://media.musicasacra.com/dominican/M39.pdf |
| Processionarium O.P. 1913 (**pdf = printed + 16**) | /home/claude/dl/proc/p.pdf | https://media.musicasacra.com/dominican/processionarium-1913-Cormier.pdf |
| Triduum O.P. 1927 | /tmp/dl/tri.pdf | https://media.musicasacra.com/dominican/officium-hedomadae-sanctae-1927-paredes.pdf |
| St Dominic Missal 1959 | /tmp/en_sources/dl/musicasacra/dm.pdf | https://media.musicasacra.com/dominican/dm.pdf |
| Graduale O.P. 1928 (djvu, 1 page = 2 printed) | /home/claude/dl/grad351/x/graduale_juxta_ritum_1928_paredes.djvu | Joseph's Drive, "351_Graduale…zip" |
| Graduale O.P. 1950 GABC | /home/claude/dl/g50gabc/x (index copy: scratch/g50gabc_index.csv) | GregoBase source 14 |
| Ordo 1944 | /home/claude/dl/ordo44/o44.pdf, o44.txt | Joseph's Drive |
| Harrison, How to Sing Plain Chant 1920 | (js/mtones.js implements it) | https://media.musicasacra.com/dominican/howtosing.pdf |
| GregoBase DB | tools/gregobase/gb.sqlite (Dominican sources 11, 12, 13, 14, 20, 21, 35, 36) | |

- **Not usable:**
  - /home/claude/dl/cpass: Roman Vatican Cantus Passionis.
  - /home/claude/dl/passio: a 15th-century Passion sermon, no chant.
  - /home/claude/dl/hs247: Officium Hebd. Sanctae O.P. 1890, text only.
- **Scratch files saved from /tmp:** `tools/handoff/scratch/`:
  - g28pages.json and g50all.txt (G28/G50 text layers)
  - hs1890.txt
  - the g28w/ crop scripts
  - omr/notes.py
  The agents' notes still name the /tmp paths; use the copies here. The processions tone generator is `tools/proc/gen_tones.js`, not /tmp/gen.
- **Files Joseph uploaded in chat** (not in the repo; ask him to re-upload if a new session lacks /mnt/user-data/uploads):
  - **Fr Innocent Smith OP, *The Passion of our Lord Jesus Christ according to Mark* (v2, English, chant).** This is the model for the Passion.
  - Two one-page scans of a Dominican Ember-day lesson (Feria IV Quatuor Temporum Adventus, Lectio II).
  - "content.pdf" = *Officium hebdomadae sanctae juxta ritum S.O.P.* (Google Books, 133 pp.).

## Done 27 Nov (all live)
- **Saints' Masses:** all 120 inferred chants settled. 38 Masses corrected from qc_mass.md (tools/g28/corrections.json, applied by tools/g28/apply.py, then tools/requiem/build.py).
  - New correction keys: `season_set` and `name_en`.
  - St Louis Bertrand's full proper Mass.
- **Requiem:** the weekly conventual Requiem (C114s) with Rubr. XII.6 prayers; the day of death (C114o); the anniversary (S1113).
- **Mass page:**
  - Proper Communicantes / Hanc igitur (`properCanon()` in js/app.js).
  - Epiphany Gloria. No Gloria on a violet Sunday Mass said on Our Lady's Saturday.
  - The Requiem Introit repeat is shown once.
  - 1939 calendar titles on dated feasts (Patrocinium, Translatio, "B."). The 4 Feb "transfer" reported in qc_ui is correct: the Missal puts the Translatio S. Catharinae on the Thursday after Sexagesima.
  - Palm Sunday stub; duplicate #ordinary fixed.
  - gabc fetch retries (the host gives a 503 while a push is being published).
  - Asperges cleaned up, with its prayers.
- **Holy Week 1939:**
  - Palm Sunday dialogues. Flectamus and Humiliate on Monday–Wednesday.
  - Good Friday: Oremus, Flectamus, Pater, Per omnia.
  - Holy Saturday Vespers: Ps 116, Magnificat. The Alleluia now draws. The Tract Sicut cervus is in the printed order.
  - 14 Latin words corrected.
- **Processions:**
  - Candlemas.
  - Versicles and prayers in the Processionarium tones (pp. 395–396, 407–408).
  - Processions back in the menu.
- **About page and site:**
  - The private-devotion disclaimer and non-affiliation note, on the About page, in the page footer and in the booklets.
  - The bookstore: Dominican Liturgy Publications on Lulu, with links to 10 books.
  - The donation link: Dominican Friars Foundation (Province of St Joseph).
  - Footer buttons "Support the Dominican Friars" and "Buy the Order's books".
  - Cloudflare Web Analytics, token in js/ui.js, dominicanrite.com only.

## To-do, in order
1. **Litanies fully in chant** (litanies.md).
   - Run `tools/proc/gen_lit.js`, gregorio-check the output, do the second pass against Proc. pp. 91–95 and 124–134, then wire it in with `_at()`.
   - Add the pp. 132–134 texts (with English) to 'extraordinariae'.
2. **Holy Week tones** (hw_tones.md).
   - Add new functions to js/mtones.js and leave the existing ones alone, because the Mass pages use them. Then generate `gabc/op-hw-*.gabc` and add G: lines to tools/hw39/*.src, then run `python3 tools/hw39/build.py`.
   - Use two oration tones (Proc. pp. 404–406 and 407–408) and the lesson/prophecy tone (pp. 408–413).
   - Stays text: the fire blessing ("legendo sine nota"), the Secrets and Canon, and the Mandatum prayers ("humili voce").
   - Sung: the Thursday Sermo Domini, in the Gospel tone.
3. **1959 English** (english_1959.md).
   - Use the DM text wherever a match exists, replacing the Divinum Officium English too. Keep the DO English only where there is no DM match, labelled; label anything still AI as "AI translation".
   - Needs the one-line `prayerOf` change in js/app.js for commemoration labels.
4. **Four G28 Masses** (g28_four_masses.md).
   - Finish teresia_al/of/co, raphael_gr, and albertus_gr/al from the 1933 S.R.C. supplement leaf; second pass on all.
   - Then add `set` entries in corrections.json (`'g28:file|incipit|page'`) and run apply.py + requiem/build.py.
5. **25 cut readings** (readings_cut.md).
   - Fix in tools/m33/run.sh after the overrides, so a rebuild keeps the fix.
   - Epi Isaias 60 is not cut: drop the stray "Omne", ref 60:1-6.
   - Quad2h must be retaken; Quad1f has "moriétur in moriétur".
   - About 40 English endings need a full stop or a trim.
6. **qc_hw.md leftovers:**
   - Split the Palm Sunday rubric "fiat Processio: qua finita…".
   - Label Maundy Thursday's two endings as the Missal's either/or (p. 165).
   - Notes for Improperia verses 2–3 and Agios. They are notated in the single block above them; split it or place it once per verse.
   - Holy Saturday Litany on separate lines.
   - Gate drawOrdo's 1959 HOLYWEEK data on `state.hwr !== '1939'`.
   - Proper Communicantes and Hanc igitur print twice on Thursday and Saturday when the Order of Mass is on; hide the .src copy in that case.
   - Holy Saturday header says "Missa I", but the page sings Kyrie IV and Gloria II.
   - Holy Saturday ordo: the Pax/no-Agnus rubric comes after the priest's communion, and it mentions an Offertory the Missal omits.
   - John Passion English adds "When Jesus had said these things".
   - "POST hæc autem" should start a new paragraph (p. 170).
   - Confirm Tuesday's chants against G28 (masses.js says matched "by incipits in the Roman Graduale").
7. **qc_ui.md leftovers:**
   - W3/W4 Requiem ceremonial.
   - W5 anniversary prayers (Rubr. XII.7).
   - W6 Omnipotens when there's no Requiem day.
   - W7 Requiem naming.
   - W2/C1/C3 prayer labels.
   - W9 Paschal ferias Gloria (verify).
   - W10 Easter Kyrie.
   - W11 Dec 30 chips.
   - W12 five translation refs.
   - W13/W14 reading mismatches, "Amen dico" twice.
   - W15 "ministers" at Low Mass.
   - W16 Roman refs on S1127b and S0524.
   - W17 tono feriali at Low Mass.
   - W18 About-page claims.
   - K1/K2 titles.
8. **qc_mass.md leftovers:**
   - Typeset S1002, S1015, S1024 and S1115.
   - Go through the DOUBTFUL items.
   - S1228 Laus tua is app logic.
   - Masses with English names cut at a comma are fixed; check for more.
9. **Processions text:**
   - Punctuate proc_data.py by the book's flexa signs and colons; the chant already follows the book.
   - Ascension prayer: put the colon after "nobis" (p. 50).
10. **Ordo 1944 cross-check:** the Kyriale by 1939 rank, and the resumed Sunday as a commemoration.
11. **The Latin Passions** (Palm Sunday Matthew; Tuesday Mark; Wednesday Luke; Good Friday John).
    - **Found 27 Nov: the Processionarium 1913 prints the Dominican Passion tones, pp. 435–440 (pdf 451–456), "VII. Modus cantandi Passiones".**
      - 1° Vox textus C. (the Chronicler).
      - 2° Vox Christi ✠, including the special settings of "Eli, Eli", "Pater, in manus tuas" and "Consummatum est".
      - 3° Vox turbae S.
      - 4° The ending in the Lamentation tone ("Altera autem die…", p. 440).
      - Sung Gospel endings: p. 436.
    - **Plan:** transcribe these tones note by note, then set the Latin Passion texts (tools/hw39/{passio,marcus,lucas,joannes}_parts.txt) to them.
      - Use Fr Innocent Smith's English OP Passion (Mark) as the model for how the tones are applied.
      - Label each one: "set to the Dominican Passion tones, Processionarium O.P. 1913, pp. 435–440".
      - Then add them to the Holy Week pages.
    - The earlier note in tools/hw39/PROGRESS.md ("no Dominican source") is out of date.
12. **Offline download** (agreed with Joseph, not started).
    - Generate a manifest of all site files on each push.
    - Add an Options button "Download for offline use" with a progress bar, offering Mass only (about 15 MB stored) or everything (about 65 MB).
    - After a push, update only the files that changed.
    - Call `navigator.storage.persist()`.
13. **Later, if wanted:** an App Store app via Capacitor. Needs a Mac, Xcode, a $99 developer account, and native features (for example a today's-feast widget).
