# Where the work stands (2026-11-18)

## Done
- Office chant: every hour incl. Matins (all but the lessons); layout cleaned; 15 more 1933 antiphons read from
  the scan (tools/omr). ~90 pieces still on the Roman melody (labelled).
- Mass: Order of Mass (Low/Sung/Solemn, data/ordo.js) after the St Dominic Missal 1959 (no Roman additions).
- Orations (data/orations.js, tools/orations.py): Divinum Officium texts matched by day/Introit, KEPT ONLY where
  the St Dominic Missal prints the same prayer (27 dropped). Still to do: confirm each prayer belongs to the right
  Mass (tools/dm_orations.py is a first, weak attempt: DM Latin labels are OCR-poor), then fill the Dominican
  saints and the dropped ones from the Missale O.P. 1939 scan (dl/m39cols, pages via ordo2026.json) or the DM.
  Lenten ferias also need the Oratio super populum.
- Dominican Sunday numbering (js/cal.js OPNames), last Sunday after the Octave of Trinity (Pent24), resumed
  Epiphany Sundays (Epi3r-Epi6r) built in js/app.js.
- Holy Week (data/holyweek.js) after the St Dominic Missal: Palm Sunday blessing/procession, Mon-Wed lessons,
  Maundy Thursday (penitential psalms, Canon inserts, repository), Good Friday (Dominican order), Easter Vigil.

## Next
1. Orations: per-Mass verification against the Dominican books; Dominican saints; super populum.
2. Chant for the Mass (task 31): Dominus vobiscum, orations, Epistle/Gospel, Pater noster, Ite in the Dominican tones.
3. Daily variations: Candlemas, Ash Wednesday, Rogations.
4. Remaining Roman-melody antiphons (1933 scan), Matins responsories and Venite (Matutinum 1936).
