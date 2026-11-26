# Mass chat — where to resume (27 Nov 2026, after v167)

Standing rules: pre-1955 Dominican rite only; never infer chant; terse; status after each substep; `git pull --rebase`,
bump sw.js, headless Chrome test, commit as UltraPheonix, `bash tools/push.sh`; do not touch the Office files.
**New (Joseph, 27 Nov): after every step, one quality run and one clarity run before moving on.**

## Done this session
- rubrics.html: every rubric of the Missale O.P. 1939 (De defectibus, Praeparatio, Modus et Ritus, genuflexions, Sacrament exposed /
  tabernacle, before a prelate, Masses for the dead, voice, servers, De officio ministrorum, De sacra Communione, general rubrics),
  Latin + English (AI, labelled), prayers bold. Built by tools/rubrics/build_rubrics.py (modules ritus_*.py); writes data/rubtext.js.
- Mass page: Basic / Full rubrics switch. Basic = only the rubrics of the Ordo Missae (M39 pp. 191-193). Full = the Ritus step by step,
  forms Low/Sung/Solemn/Conventual, conditional lines (prelate: Pope / Bishop / Master of the Order; Sacrament: tabernacle / exposed;
  servers; rank of the day, incense days, Requiem, Flectamus, etc.). Source: tools/rubrics/ordo_directions.py -> data/ordo.js
  (texts in tools/rubrics/ordo_texts.json). Day rank = KAL39 + heuristics (approximate until the day-classification engine exists).
- prayers.html: vesting prayers, prayers before and after Mass. Published PD English where found (tools/prayers/prayers_published.py:
  1905 reprint of Oakeley 1848 for vesting; Manual of Prayers, Baltimore 1889 for St Thomas, St Ambrose, Ad mensam, St Bonaventure;
  Hopkins for Adoro te; [brackets] = ours). Remaining AI-labelled: Augustine/Ambrose readings, confession prayers, O sancte N.,
  O serenissima, Pater caelestis, Anima Christi (Dominican form), In nomine.

## In progress when stopped: task #46, chant English
- data/masses.js trans: 357 Douay-Rheims ('douay'), 576 'own' (AI, replaced the 1959 St Dominic Missal English in an earlier session,
  see build_masses.py ~line 540; the 1959 English is still in tools/sources/dm_trans.json). tools/g50/trans.json (47 new chants) is AI.
- Next: (1) check scriptural chants in g50/trans.json against the real Douay-Rheims (/home/claude/src/jgabc/douay-rheims, tools/douay_match.py)
  and mark 's': 'douay'; (2) ask Joseph whether to bring back the 1959 St Dominic Missal English (human) for the 576 'own' chants,
  or keep AI and label it on the page; (3) label AI English on the Mass page.

## Then (Joseph's order)
1. 2nd and 3rd collects: dropdown where the priest chooses; carry to Secret and Postcommunion.
2. Error check: the 30 flagged feasts (tools/g50/check.py), then a full Mass check.
3. Processions, litanies and blessings (Processionarium 1913).

Test helpers (recreate if /tmp was cleared): local server `python3 -m http.server 8768`; sweep of Masses x forms x rubrics
is tools/check/mass_sweep.py (load index.html?n=<i>#<key>&ordo=<f>&rub=<full>&sac=..&prel=.., check pageerrors, duplicate rubric lines,
empty sections, Canon present).
