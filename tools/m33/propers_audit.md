# Propers vs Missale O.P. 1933 — audit (step 3)

propers_audit.py compares words 2-6 of every Introit/Gradual/Offertory/Communion the site sings with the OCR after the heading in M33.
All 43 lines of the first pass and every line below were checked on the page images. Real mismatches are corrected in
propers_fix.json (applied by propers_apply.py, also from build_masses.py); M33 anchors in dpmap.json. What is left below is
OCR noise (lost drop caps, mixed columns, NOHEAD = heading not read) or Masses absent from M33 (C1s Commune Apostolorum).

| Mass | part | site | M33 OCR | pdf p. |
|---|---|---|---|---|
| Adv2 | gr | NOHEAD | 51 | | |
| Adv2 | co | NOHEAD | 51 | | |
| Adv3 | gr | NOHEAD | 52 | | |
| Adv3w | gr | tollite portas principes uestras eleuamini | prope est dominus omnibus inuocantibus eum omni bus qui inuocant | 54 |
| Adv3f | in | prope domine omnes uiae tuae | gnoui de testimoniis tuis rittttttt quia in aeternum tu es | 55 |
| Dec24 | gr | NOHEAD | 61 | | |
| Dec25_1 | gr | NOHEAD | 65 | | |
| Dec25_2 | gr | NOHEAD | 67 | | |
| Dec25_3 | gr | NOHEAD | 69 | | |
| Nat1 | gr | NOHEAD | 71 | | |
| Nat1 | of | NOHEAD | 71 | | |
| Nat1 | co | NOHEAD | 71 | | |
| Jan1 | gr | NOHEAD | 74 | | |
| Jan5a | in | lux fulgebit hodie super nos | h bilis deus princeps pacis uoc s filius et heres | 76 |
| Jan5a | gr | NOHEAD | 76 | | |
| Epi | gr | NOHEAD | 79 | | |
| Epi1 | gr | unam petii domino hanc requiram | beati qui habitant in domo tua domine in saecula saeculorum | 81 |
| Epi1 | of | NOHEAD | 81 | | |
| Epi3 | gr | NOHEAD | 87 | | |
| Epi4 | gr | NOHEAD | 88 | | |
| Epi5 | gr | NOHEAD | 89 | | |
| 6a | gr | NOHEAD | 93 | | |
| 5aw | gr | NOHEAD | 98 | | |
| 5ah | gr | NOHEAD | 100 | | |
| 5af | gr | NOHEAD | 101 | | |
| Quad1w | in | reminiscere miserationum tuarum domine misericordiae | eminiscere m sunt ne unquam dominen tur nobis inimici nostri | 108 |
| Quad1f | gr | NOHEAD | 111 | | |
| Quad1s | gr | NOHEAD | 113 | | |
| Quad2 | gr | NOHEAD | 116 | | |
| Quad2w | co | NOHEAD | 120 | | |
| Quad2h | gr | NOHEAD | 121 | | |
| Quad2h | co | qui manducat meam carnem bibit | psalm iustus domi r terra salsuginis et inhabitabili bene uidit | 121 |
| Quad3 | gr | NOHEAD | 127 | | |
| Quad3t | gr | NOHEAD | 130 | | |
| Quad3h | gr | oculi omnium sperant domine das | attendite popule meus legem meam inclinate aurem ue stram in | 133 |
| Quad4w | gr | NOHEAD | 143 | | |
| Quad4h | gr | NOHEAD | 146 | | |
| Quad5 | gr | NOHEAD | 151 | | |
| Quad5m | gr | NOHEAD | 152 | | |
| Quad5w | gr | NOHEAD | 155 | | |
| Quad5f | gr | NOHEAD | 382 | | |
| Quad6 | of | NOHEAD | 163 | | |
| Quad6 | co | NOHEAD | 163 | | |
| Quad6m | in | iudica domine nocentes expugna impugnantes | si et exsurge in adiutorium meum domine uirtus salutis meae | 168 |
| Quad6m | gr | NOHEAD | 168 | | |
| Quad6t | gr | ego autem dum mihi molesti | deus misereatur nostri et benedicat nobis illuminet uultum suum super | 169 |
| Quad6w | of | NOHEAD | 174 | | |
| Quad6w | co | NOHEAD | 174 | | |
| Quad6h | gr | christus factus est pro nobis | uoce mea dicta post ultimum psalmum antiphona prior stans ad | 183 |
| Pasc0 | co | NOHEAD | 291 | | |
| Pasc0w | co | NOHEAD | 295 | | |
| Pasc0h | co | populus acquisitionis annuntiate uirtutes eius | rom christus resur gens ex mortuis iam non moritur alleluia | 296 |
| Pasc6s | of | NOHEAD | 321 | | |
| Pasc6s | co | NOHEAD | 321 | | |
| Pent0s | gr | NOHEAD | 330 | | |
| CorpusChristi | gr | NOHEAD | 337 | | |
| Pent4 | gr | NOHEAD | 345 | | |
| Pent7 | co | NOHEAD | 349 | | |
| Pent8 | gr | NOHEAD | 350 | | |
| Pent11 | gr | NOHEAD | 354 | | |
| Pent13 | gr | NOHEAD | 356 | | |
| Pent14 | gr | NOHEAD | 357 | | |
| Pent15 | gr | NOHEAD | 358 | | |
| Pent19 | gr | NOHEAD | 370 | | |
| Pent20 | gr | NOHEAD | 371 | | |
| Pent22 | gr | NOHEAD | 374 | | |
| ChristusRex | in | NOHEAD | 618 | | |
| Pent23 | gr | NOHEAD | 376 | | |
| Dedicatio | gr | NOHEAD | 648 | | |
| C1s | gr | NOHEAD | 697 | | |
| C1s | of | mihi autem nimis honorati sunt | psalm in omnem terram exiuit sonus eorum et in fines | 698 |
| C18s | gr | NOHEAD | 655 | | |
| C28s | co | NOHEAD | 660 | | |
| C35s | gr | NOHEAD | 663 | | |
| C42s | gr | domine praeuenisti eum benedictionibus dulcedinis | ascendit deus in iu bilatione et dominus in uoce tubae | 666 |
| C64s | gr | spiritus domini super propter quod | dicite filiae sion ecce rex tuus uenit tibi mansuetus isa | 683 |
| C68s | gr | NOHEAD | 684 | | |
| C75s | gr | NOHEAD | 689 | | |
| C76s | gr | NOHEAD | 690 | | |
| C76s | of | NOHEAD | 690 | | |
| C76s | co | NOHEAD | 690 | | |
| C79s | gr | benedicta uenerabilis uirgo maria quae | surrexit dominus et occurrens mulieribus ait auete tunc accesserunt et | 693 |
| C82s | gr | dilectus meus mihi ego illi | sicut dies uerni circum dabant eam flores rosarum et lilia | 695 |
| C85s | gr | NOHEAD | 700 | | |
| C93s | gr | NOHEAD | 703 | | |
| C110s | gr | NOHEAD | 722 | | |
| C114s | gr | requiem aeternam dona eis domine | si ambulem in medio umbrae mortis non timebo mala quo | 737 |
| G420 | gr | NOHEAD | 436 | | |
| G446 | gr | NOHEAD | 456 | | |
| G470 | gr | iustus palma florebit sicut cedrus | diligam te domine for titudo mea dominus firmamentum meum et | 478 |
| G481 | gr | NOHEAD | 493 | | |
| G494 | gr | NOHEAD | 507 | | |
| G505 | gr | NOHEAD | 515 | | |
