# W-F2 (under Lead F): remaining qc_ui.md items. Stopped 27 Nov on the coordinator's order

Rules as in README.md. Nothing committed. The only file edited is js/app.js. Every edit there is finished and tested in headless Chrome with no console errors, and `node --check` passes. mass_sweep.py was **not** run after these edits, so run it before you push.

## Done
- **W9 (Gloria on Paschal ferias): verified, no change.** Ordo 1944, Tuesday after Low Sunday: "Omitt. Te Deum" and "Missa priv. de Dom. praec. … Omitt. Gloria et Credo … in fine Bened. Domino". Missal 1939 Rubr. IX.2: "Gloria in excelsis Deo dicitur solum quotiescumque in Officio ante Laudes dictum fuerit Te Deum laudamus". The site is right. The subtitle "(Mass of the preceding Sunday)" was not added.
- **W10 (Easter Kyrie), js/app.js:**
  - `paschalKyrie()` (about line 763) now goes by the day's 1939 rank from mrank, per Graduale O.P. 1928, Kyriale p. 129*: "IV. Tempore Paschali in Dominicis et Duplicibus et supra". Page 155* adds: "neque Tempore Paschali in Ordinariis de B. M. V. … neque in Semiduplicibus et infra".
  - The Kyrie hint (about line 1937) now reads "on Sundays and on Doubles and above (Graduale O.P. 1928, Kyriale p. 129*)".
  - Checked: S0505 and Pasc2w now get Kyrie IV; Semidoubles (S0409b) do not; the Easter octave and Pasc1 ferias are unchanged.
- **W11 (30 Dec chips), js/app.js:**
  - `massesOf()` (about line 2224) drops Dec25_1 and Dec25_2 unless the date is 25 Dec.
  - `dayRankLabel()` (about line 2238) gives Nat1 on a weekday the label "Sunday within the octave (transferred to 30 Dec.)". Missal: "ejus Officium transferatur in diem 30 Decembris".
  - **Root fix for the mrank.js owner:** at line ~519, `if (win.kind === 'temporal' && /^Dec25/.test(tKey))` also fires on 26–31 Dec, because tKey is Dec25_3 there. It should fire only on 12-25.
- **W15 ("ministers" at Low Mass) and W17 ("tono feriali" at Low Mass): already fixed** on the current site. Checked C114s and Adv1 at ordo=low.

## Left
- **W12: data/masses.js, Lead D's file. Sent to main.** Change D.trans[id].r as follows:

  | id | Chant | Now | Should be |
  |---|---|---|---|
  | 5367 | | "Ps. 142, 8-3" | "Ps. 24, 1-3.4" |
  | 4284 | | "Ps. 118, 137-124" | "Ps. 118, 137.124.1" |
  | 6841 | | "Ps. 37, 22-8" | "Ps. 37, 22-23.2" |
  | 7015 | | "John 15, 5-1" | "John 15, 5.1" |
  | 8003 | | "Ps. 118, 46-1" | "Ps. 118, 46-47.1" |
  | 6453 | Domine non secundum | "Ps. 102,.10" | "Ps. 102, 10; Ps. 78, 8-9" |

  No other malformed or descending refs were found.
- **W14:** data/readings33.js, 5aw Gospel: "Amen dico bis" should be "Amen dico vobis" (Matt. 6:16). This is the only occurrence. The fix goes in tools/m33/run.sh overrides so that a rebuild keeps it. It needs a check against the M39 scan, because m39lin.txt has no clean hit. Send it to main.
- **Not started:**
  - W13: reading English/Latin mismatches; S0611 and S0722 references.
  - W16: Roman refs on S1127b and S0524.
  - W18: about.html claims. Keep the disclaimer and support sections.
  - K1/K2: title truncation and capitalisation.
  - The C and K items that are not about prayer labels.
- **Question for main (rule 4), not changed:** Paschal feria Alleluia verse. app.js `massParts` uses `parts.al[d.getDay() % 2 ? 0 : 1]`, which gives Tuesday the 2nd verse and Wednesday the 1st. Ordo 1944 (18–19 Apr.) gives Tuesday "semel ante et post 1-um Versum (omisso 2-o)" and Wednesday the 2nd. Missal Rubr. XIII.1 only says "alternatim desumi debet". That is one data point, and it is the opposite of the code.
- **Ordinary choice:** `autoKyriale` cites the post-1960 classes (Thompson). Pasc2w, a I class feast, gets Missa VI. This belongs to README item 10 (Kyriale by 1939 rank).

## Resume
1. Run `timeout 590 python3 tools/check/mass_sweep.py` (port 8768). It must print `cases 224 flagged 0`.
2. Then W13/W16: look up the Dominican pericopes in M39 and send them to main. Then W18 about.html, then K1/K2.

Harness: /tmp/wf2/dump.py (`HEAD=1` prints the pills, chips and header) and /tmp/wf2/ev.py.
