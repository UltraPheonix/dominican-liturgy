# Handoff (paused 27 Nov 2026, Mass chat)

Read this first, then tools/RESUME.md. Each running agent left its own note here (`*.md`).
The QC reports are copied here too: qc_mass.md (saints' Masses), qc_ui.md (site walkthrough) and qc_hw.md (Holy Week 1939).

## Standing rules
- Pre-1955 Dominican rite only. Use Dominican books only: Missale O.P. 1939, Graduale O.P. 1928/1950, Processionarium O.P. 1913 (pdf page = printed + 16), and the Triduum O.P. 1927.
- No Roman Missal. No Lumen Christi.
- Chant is typeset GABC read note by note from the scan. Where the book prints only a tone or formula, the text may be set to that printed Dominican tone, and the file header must say so with the page.
- To push: commit as UltraPheonix, then run `bash tools/push.sh`.
  - push.sh rebases and bumps sw.js. It needs a clean tree.
- Before every push: run `timeout 590 python3 tools/check/mass_sweep.py`; it must report "cases 224 flagged 0". Then check the page in headless Chrome.
- Never touch the Office chat's files: data/office*, tools/b09/, js/office.js, js/tones.js, data/chant/office.json, office.html.

## Done this session
- **Saints' Masses:** 38 corrected from the QC list (tools/g28/corrections.json).
  - New keys: `season_set` (replaces one part within one season) and `name_en`.
- **Proper Communicantes / Hanc igitur:** js/app.js `properCanon()`, for Christmas, Epiphany, Easter, Ascension and Pentecost.
- **Holy Week 1939:**
  - Good Friday: Oremus, Flectamus, Pater, Per omnia.
  - Holy Saturday Vespers: Ps 116, Magnificat.
  - Palm Sunday dialogues; Flectamus and Humiliate on Monday–Wednesday.
  - 14 Latin words corrected.
  - The Holy Saturday Alleluia now shows.
- **Processions:** Candlemas (6 chants); versicles and prayers set to the Processionarium tones (tone_*.gabc, generator tools/proc/gen_tones.js). Processions is back in the menu.
- **UI:**
  - Epiphany Gloria.
  - The Requiem Introit repeat is shown once.
  - No Gloria on a violet Sunday Mass said on Our Lady's Saturday.
  - 1939 calendar titles on dated feasts.
  - Palm Sunday stub.
  - Duplicate #ordinary.
  - gabc fetches are retried (the host gives a 503 while a push is being published).

## Left (in order)
1. **Litanies fully in chant:** see litanies.md.
2. **Holy Week priest's and deacon's tones** (orations, prophecies, Epistles, Gospels, solemn prayers): see hw_tones.md.
3. **1959 St Dominic Missal English, verbatim:** see english_1959.md.
4. **Guardian Angels, St Teresa, St Raphael's Gradual, St Albert (G28 p. 567–601 and the 1933 supplement):** see g28_four_masses.md.
5. **25 readings cut at a page break:** see readings_cut.md.
6. **Rest of qc_hw.md:**
   - Palm Sunday rubric split.
   - Maundy Thursday's two endings.
   - Improperia verses 2–3 with notes.
   - Holy Saturday Litany split into lines.
   - drawOrdo should read the 1959 HOLYWEEK data only when hwr ≠ 1939.
7. **Rest of qc_ui.md W/C/K items:**
   - Requiem ceremonial.
   - Anniversary prayers (XII.7).
   - Prayer labels.
   - The About page.
   - Roman references on S1127b and S0524.
8. **Rest of qc_mass.md:**
   - S1002, S1015, S1024 and S1115 need typesetting.
   - The DOUBTFUL items.
9. **Ordo 1944 cross-check:** Kyriale by 1939 rank; the Sunday resumed as a commemoration.
10. **Processions page text punctuation:** follow the book's flexa and colons (see the note in proc_tones handback). Also, the proc_data.py header says +15 but it is +16.
11. **Offline download (agreed, not started):**
    - Generate a manifest of all site files at push time.
    - Add an Options button "Download for offline use" with a progress bar, with Mass-only (about 15 MB) or everything (about 65 MB).
    - Update only the changed files after a push.
    - Call `navigator.storage.persist()`.
12. **Later, if wanted:** an App Store app via Capacitor. Needs a Mac, Xcode and a $99 developer account, plus native features such as a today's-feast widget.

Also added after the pause:
- About page and site footer: the disclaimer and non-affiliation note, the bookstore (Dominican Liturgy Publications on Lulu) and the donation link (Dominican Friars Foundation).
- The footer's Support and Books buttons.
- Cloudflare Web Analytics, loaded in js/ui.js on dominicanrite.com only.

13. **Last:** the Latin Passion, reconstructed from Fr Innocent Smith's English OP Passion GABC, clearly labelled.
