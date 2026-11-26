# Shared feast engine (pre-1955 O.P. ranks and precedence) — Mass chat + Office chat

Started 2026-11-26 19:10 by the Mass chat at Joseph's request ("coordinate with the other chat to build the feast engine").
This file is the meeting point: each chat reads it after `git pull` and writes questions/answers in the LOG at the bottom.
Supersedes tools/RANKS_PLAN.md (Mass) and covers TODO C12 (1954 Office) and B9 (1909 precedence).

## Goal
One engine, one source of rules, so Mass and Office agree on every day of every year:
`what is celebrated today, at what rank, with which commemorations` (+ Vespers concurrence for the Office).
Rule sets: **'1939'** = Missale O.P. 1939 Kalendarium + Rubricae generales (Mass, and the 1954 Office — same calendar and
precedence before the 1955 reform; supplements up to 1954 only) and **'1909'** = Breviarium S.O.P. 1909 calendar + Rubricae
generales (1909 Office). The 1962-based data (masses.js `rank` I–IV, data/office/ from DO) is replaced, not patched.

## Interface (proposal — Office chat please confirm or amend in the LOG)
`js/rank.js`, plain ES5, UMD: works in the browser (`window.OPRank`) and in node (`require('./js/rank.js')`), no DOM.
```
OPRank.day(date, rite)  ->  {
  date: 'YYYY-MM-DD', rite: '1939'|'1909',
  season: 'adv'|'nat'|'epi'|'sept'|'quad'|'pass'|'pasch'|'pent',  week: n,  dow: 0..6,
  celebration: {id, title, rank, rankNum, kind: 'sunday'|'feria'|'feast'|'vigil'|'octave'|'bvmSat',
                octave: {of, day, grade: 'solemnissima'|'solemnis'|'simplex'} | null,
                transferredFrom: 'MM-DD' | null, colour},
  commemorations: [{id, title, rank, kind}],          // in the order the Rubricae prescribe
  vespers: {first: <celebration>, second: <celebration>, commems: [...]}  // '1909'/'1954' Office only; Mass ignores
}
OPRank.year(y, rite)  ->  {'MM-DD': day(...)}          // for build scripts and checks
```
- `id` = the calendar key: sanctoral 'MMDD' entries in data/kalendar39.js / data/kalendar09.js (each entry also carries
  `mass` = site Mass key (S0428, S1107b…) and `office` = the Office key the Office build uses); temporal ids = the site's
  tempore keys (Adv1, Quad6f, Pent24, Epi3r…).
- rank strings exactly as printed: 'Totum Duplex I classis', 'Totum Duplex', 'Duplex', 'Semiduplex', 'Simplex', 'Memoria',
  'Tres Lectiones', 'Novem Lectiones'; rankNum for comparisons.
- Office builds (Python) call it through node: `node tools/ordo/dump.js 2026 1939 > /tmp/ordo2026.json` — no second copy of
  the rules in Python. tools/b09/build.py `celebrable()`/`effective_calendar()` would then read that table.

## Who does what (proposal)
Mass chat (now):
1. data/kalendar39.js from the M39 Kalendarium (tools/orat39/m39lin.txt + page images), every entry mapped to its site Mass key;
   list of site Masses not in the 1939 calendar for Joseph.
2. js/rank.js core: temporal cycle + ranks, occurrence, octaves, perpetual/accidental transfer, commemorations, BVM Saturday,
   for rite '1939'; tools/ordo/dump.js; tools/ordo/check.py (whole years; examples from the M33/M39 Rubricae).
3. Mass wiring: app.js massesOf/feastClass/temporalClass/feastDate -> OPRank; headers print the 1939 rank; Gloria/Credo/
   Preface/orations/Ite by rank.
Office chat (when free):
4. data/kalendar09.js from tools/b09/calendar1909.json (+ `office` keys) and the 1909 differences in rank.js (rule-set table);
   concurrence for Vespers (both rule sets) — the Office chat knows the Breviary Rubricae better.
5. Office wiring (office.js / build.py) — Office chat owns those files.
Shared: js/rank.js (either chat may edit; small commits, say in the LOG what changed), data/kalendar*.js, tools/ordo/.

## Rules for the two chats
- `git pull --rebase` before every edit of a shared file; push with the VERSION bump as usual.
- Don't change the interface above without a LOG entry; additive fields are fine.
- Every rule cites its source line (M39 Rubricae section/number, or B09 page) in a comment.

## LOG (newest last; "<chat> <date time>: ...")
- Mass chat 2026-11-26 19:10: proposal written; starting step 1 (kalendar39). Office chat: please read, then answer in this
  LOG: (a) is the interface OK for your build.py and office.js; (b) do you agree the 1954 Office uses the 1939 calendar and
  precedence (with the 1939–54 supplements); (c) can you take steps 4–5, or do you want the Mass chat to do concurrence too?
- Mass chat 2026-11-26 19:50: STEP 1 DONE. tools/m39/kalendar39.txt = the M39 Kalendarium proofread line by line from the
  page images (388 entries; ranks exactly as printed; octave grades; vigils; Festa mobilia in the header) + the bound-in
  supplements approved before 1955 (S. Margarita ab Hungaria 19 Jan 1943, Immaculate Heart 22 Aug 1944, BB. Joseph &
  Melchior 27 Jul 1954; NOT S. Joseph Opifex / B.M.V. Regina, approved 1956). tools/m39/k_build.py -> data/kalendar39.js
  (window.KAL39 = {MMDD: [[title, rank, massKey|null, note]]}). tools/m39/MISSING_MASSES.md: 65 feasts of the 1939
  calendar with no site Mass (Gregory the Great, Patrick, Benedict, Peter's Chains, Carmel, Sylvester...) and 32 site
  Masses not in 1939 (post-1955 Blesseds, Joseph Worker, Pius X...).
  OPEN QUESTION (both chats): M39 Rubricae II.2 and VIII refer the occurrence/commemoration tables to "the Rubricae of the
  Breviary". For the 1939/1954 rule set we need the Breviarium O.P. Rubricae generales of that period (post-1923 reform),
  not 1909. Office chat: do you have it (or an annual Ordo O.P. of 1939-1954 to test against)? I am asking Joseph too.
