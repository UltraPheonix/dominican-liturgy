# Lead D (Graduale and saints' Masses): state at end, 27 Nov 2026

All four G28 Masses (README item 4) are finished, checked against the scan and wired in. Most of the qc_mass DOUBTFUL items (item 8) are also wired in.
- Every batch was wired through tools/g28/corrections.json, then `python3 tools/g28/apply.py`, then `python3 tools/requiem/build.py`.
- Every batch was tested in headless Chrome: sung Mass page on its date, no console errors, nothing "could not be drawn".
- Nothing is committed. The coordinator commits.

## READY items and the files each one touched

### 1. S1002 Guardian Angels
- Files:
  - tools/g28/angeli_in.gabc, angeli_gr.gabc, angeli_al.gabc, angeli_of.gabc, angeli_co.gabc
  - gabc/op-g28-angeli-{in,gr,al,of,co}.gabc (new)
  - corrections.json: entry S1002
  - data/masses.js
- Second-pass fixes:
  - angeli_al: "e(ed/fgFE/e)". An extra e at the start of the staff was removed.
  - angeli_co: "Je(hjij)". An extra h was removed.

### 2. DOUBTFUL batch
- Files:
  - tools/g28/gaudete_co.gabc (new): the short Communio Gaudete justi, G28 p. 560
  - gabc/op-g28-gaudete-co.gabc (new)
  - corrections.json: entries S0319, S0428, S0508, S0916, S1009_2, S1031, C25s, C7s, C51s
  - data/masses.js
- S0925 needs no change: M39 p. 569 and the Ordo 1944 both give Seq. Laudes ergo.

### 3. S1024 St Raphael
- Files:
  - tools/g28/raphael_gr.gabc (fix: "ex(jhi)") and raphael_co.gabc
  - gabc/op-g28-raphael-{gr,co}.gabc (new)
  - corrections.json: entry S1024
  - data/masses.js

### 4. S1015 St Teresa
- Files:
  - tools/g28/teresia_{in,gr,al,of,co}.gabc. Virgas fixed: of "ex(fg/ixi/ivGF)", co "can(hghf/gvFE)".
  - gabc/op-g28-teresia-{in,gr,al,of,co}.gabc (new)
  - corrections.json: entry S1015
  - data/masses.js

### 5. S1115 St Albert
- Files:
  - tools/g28/albertus_{gr,al}.gabc (header only)
  - gabc/op-g28-albertus-{gr,al}.gabc (new)
  - corrections.json: entry S1115, with season data from the M39 votive rubric
  - data/masses.js

### Also written
- tools/handoff/D.md (this file).

## Left to do (qc_mass DOUBTFUL, not wired)
- **Commons' Paschal and Ascension II Alleluias** for C62s, C64s, C82s, C85s, C89s, C93s.
  - G50 OCR (scratch/g50all.txt) has rubrics near lines 12681, 12791, 13361, 13617, 13793 and 13974. Map each to its Mass first.
  - Then add `season_set` entries.
- **C110s:** the Offertory 6005 "In te speravi" is unverified. Check it against G28 or G50.
- **C25s:** the Offertory should be "Mirabilis, sine alleluia" (G28 27*). 4790 is printed with alleluia. Check how the app treats the alleluia.
- **S0428:** the orations still give St Paul's prayers as the Mass prayers. The Missal (pp. 420-421) has the prayers of B. Louis Grignion de Montfort, with St Paul only as a commemoration. Fixing this needs orations.js or app work.
- **No Common for a Martyr not a Bishop (G28 18*-20*).** Individual Masses were fixed through corrections.json. apply.py cannot create a new Mass.
- **apply.py 'ok' key:** it labels pages as "G50 p. N". Don't use it with G28 page numbers.

## Tools
- /tmp/ld/st.py PAGE L|R PREFIX y...: crops each staff into two halves from /tmp/ld/pPAGE.pnm. Make the pnm with `ddjvu -format=pnm -page=N <djvu> /tmp/ld/pN.pnm`.
- /tmp/ld/t/pw.py URL...: headless Chrome check. It reports console errors and any "could not be drawn".
