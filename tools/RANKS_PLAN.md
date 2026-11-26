# Plan: pre-1955 ranks for the Mass calendar (TODO E24) — 2026-11-26, Mass chat

Now: data/masses.js `rank` = 1960 classes (I–IV), js/app.js feastClass()/temporalClass()/massesOf() use the 1960 rules,
headers print "III class", data/ordo.js says "with the rubrics of 1960". The rite rule is pre-1955 O.P. only.

Source: the Missale O.P. 1939 (M39.pdf; text layer tools/orat39/m39lin.txt) — the Kalendarium (lines ~1400–3300, every day
with its rank: Totum Duplex [I/II classis], Duplex, Semiduplex, Simplex, Memoria, iij Lectiones; octaves Solemnissima /
Solemnis / Simplex) and the Rubricae generales (lines ~3300–7700: occurrence, concurrence, transfers, commemorations,
Gloria/Credo/Preface/number of orations, votive Masses, colours), plus the bound-in supplements (1944–1956 feasts; only
those before 1955 count). Cross-check: Missale O.P. 1933 (tools/m33) and the 1909 Breviary calendar
(tools/b09/calendar1909.txt, transcribed from the page images by the Office chat).

Steps
1. tools/m39/kalendar.py: Kalendarium -> data/kalendar39.js {MMDD: [[title, rank, op?], ...]}; doubtful lines checked on the
   page images; map every entry to a site key (S-keys, b-Blesseds) and list the site Masses that are not in the 1939
   calendar (post-1939 Blesseds, 1955+ feasts) for Joseph.
2. Temporale ranks from the Rubricae: Sundays (privileged I class: Advent I, Passion, Palm, Easter, Low, Pentecost;
   II class: other Advent/Lent/Septuagesima Sundays; the rest semiduplex), ferias (privileged: Ash Wed., Holy Week;
   major: Advent, Lent, Ember days, Rogation Monday), vigils (I/II class, common), octaves (solemnissima: Christmas,
   Easter, Pentecost, Corpus Christi, Sacred Heart; solemnis; simplex) and their days.
3. js/rank39.js: precedence by the 1939 Rubricae — occurrence (Totum Duplex > Duplex > Semiduplex > Simplex/Memoria;
   privileged Sundays and ferias; octave days), perpetual and accidental transfer of impeded Totum Duplex/Duplex,
   commemorations (Memoria, Sunday, feria, octave), Saturday Office/Mass of Our Lady. Replaces massesOf(),
   feastClass(), temporalClass(), feastDate() (the 1960 transfer rules for St Joseph / Annunciation go).
4. Rubrics from the rank: Gloria, Credo, Preface, number and order of orations (with the commemorations' prayers from
   data/orations.js), Ite/Benedicamus, Kyriale by rank (Graduale O.P. table), colour.
5. UI: headers and chips print the 1939 rank ("Totum Duplex I classis", "Duplex", "Memoria"…); data/ordo.js text;
   tools/check/year.py checks rank/precedence for whole years (compare with the 1933 Missal's examples and the
   Office chat's 1909/1954 engine so Mass and Office agree).
6. Shared engine: the Office chat needs the same 1954 rule set (TODO C12). Build rank39.js as a library both pages load;
   agree the interface with the Office chat before step 3 (Office chat owns js/office.js).

Holy Week: the "Reformed 1959" toggle (state.hwr '1959', holyweek.html) shows the post-1955 rite. Options (Joseph to decide):
(a) remove it; (b) keep it but hidden and labelled "post-1955, not the Dominican rite of this site"; (c) keep as is.
