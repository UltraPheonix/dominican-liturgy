# CHECK.md: independent check of the audit fixes (A1-A6)

Sample: random 1 in 10 of non-'src' entries, Python random.seed(1939), stratified per file (k = round(n/10) per file): A1 20, A2 23, A3 23, A4 26, A5 13, A6 14 = 119 entries. Script: /tmp/CHK/sample.py; list /tmp/CHK/sample.json.
Method: text-layer diff (/tmp/CHK/cmp.py) to flag word/punctuation/case differences, then every entry read on the M39 scan (crops in /tmp/CHK/) for words, accents and marks. i/j and the conclusion pointing (canon()) ignored.

**STOPPED EARLY on the coordinator's order (Joseph out of credits): entries 55-118 were not checked.**

| # | fixes entry | file | path | verdict | note |
|---|---|---|---|---|---|
| 0 | A1.json #6 | data/readings33.js | Adv3/0/la | AGREE | checked on scan p. 5 (pdf 36): words, accents, punctuation as printed |
| 1 | A1.json #27 | data/readings33.js | Adv3s/1/la | AGREE | checked on scan pp. 10-11 (pdf 39), incl. the added 'Ait Dóminus omnípotens.' |
| 2 | A1.json #35 | data/orations.js | Dec24/se/0 | AGREE | p. 17 (pdf 42) as printed |
| 3 | A1.json #43 | data/readings33.js | Dec25_1/0/la | AGREE | p. 18 (pdf 43) as printed (lower-case consiliárius, fortis, pater, princeps confirmed) |
| 4 | A1.json #44 | data/readings33.js | Dec25_1/2/la | AGREE | p. 19 (pdf 43) as printed; note: print has 'Angelus/Angelo' without accent on the capital (site Á) - typographic only |
| 5 | A1.json #45 | data/readings33.js | Dec25_1/1/la | AGREE | p. 18-19 (pdf 43) as printed |
| 6 | A1.json #58 | data/orations.js | Dec25_3/se/0 | AGREE | p. 24 (pdf 46) as printed |
| 7 | A1.json #60 | data/orations.js | Nat1/se/0 | DISAGREE | p. 27 (pdf 47) prints 'obtíneat' (accented); new has 'obtineat'. Rest (punctuation change) as printed. |
| 8 | A1.json #63 | data/readings33.js | Nat1/1/la | AGREE | pp. 26-27 (pdf 47) as printed |
| 9 | A1.json #68 | data/readings33.js | Nat2/1/la | AGREE | p. 31 (pdf 49) as printed (print 'Angelo' unaccented capital) |
| 10 | A1.json #79 | data/readings33.js | Epi/1/la | AGREE | pp. 34-35 (pdf 51) as printed (rubric 'Hic genuflectitur' omitted from text, small caps lowered) |
| 11 | A1.json #84 | data/readings33.js | Epi1/0/la | AGREE | p. 37 (pdf 52) as printed |
| 12 | A1.json #92 | data/orations.js | Epi3/pc/0 | AGREE | p. 43 (pdf 55) as printed |
| 13 | A1.json #119 | data/orations.js | 5a/se/0 | AGREE | p. 53 (pdf 60) as printed |
| 14 | A1.json #139 | data/readings33.js | 5as/0/la | AGREE | pp. 61-62 (pdf 64-65) as printed |
| 15 | A1.json #147 | data/orations.js | Quad1m/se/0 | AGREE | p. 67 (pdf 67) as printed |
| 16 | A1.json #164 | data/readings33.js | Quad1h/0/la | AGREE | pp. 71-72 (pdf 69-70) as printed (print 'Anima' unaccented capital) |
| 17 | A1.json #183 | data/orations.js | Quad2/or/0 | DISAGREE | p. 79 (pdf 73): body as printed, but the print ends 'mundémur in mente : Per Dóminum.' (colon before the conclusion); new has 'in mente. Per Dóminum' (mark before the conclusion, not canon()-handled) |
| 18 | A1.json #193 | data/orations.js | Adv3f/en_src | DISAGREE | Labels Adv3f Secret English 'ai', but the St Dominic Missal 1959 does print English for this Latin (Ember Friday of Advent, DM key T4: 'Having received our gifts and prayers, we beseech You, Lord, to cleanse us by these heavenly mysteries and mercifully to hearken to us: through our Lord.' per tools/orat39/dm_prayers.json); RULINGS allow AI only where DM 1959 has none. (dm.pdf scan itself not on this machine.) |
| 19 | A1.json #194 | data/orations.js | 7a/se/1 | DISAGREE | English matches its Latin, but it is an AI translation where the St Dominic Missal 1959 has English for the same Secret (Septuagesima Sunday T19 has the Latin; same Latin with English in T4 Ember Friday of Advent: 'Having received our gifts and prayers...'); RULINGS: use DM 1959 verbatim. Latin (Muneribus nostris) checked p. 49 not needed. |
| 20 | A2.json #2 | data/orations.js | Quad5s/pc/0 | DISAGREE | p. 136-137 (pdf 102) prints 'satiáti, quǽsumus Dómine Deus noster; ut hujus' - no comma after Dómine; new has 'quǽsumus Dómine, Deus noster;' |
| 21 | A2.json #6 | data/readings33.js | Quad6/0/la | AGREE | pp. 140-141 (pdf 104) as printed (rubric Hic genuflectitur omitted) |
| 22 | A2.json #20 | data/readings33.js | Quad6/1/title_en | AGREE | Latin heading p. 140 (pdf 104) 'Passio Domini nostri Jesu Christi secundum Matthaeum'; English matches |
| 23 | A2.json #24 | data/readings33.js | Quad6m/0/la | AGREE | p. 147 (pdf 107) as printed ('Ideo' capital unaccented in print) |
| 24 | A2.json #41 | data/orations.js | Quad6h/or/0 | AGREE | p. 161 (pdf 114) as printed |
| 25 | A2.json #61 | data/readings33.js | Pasc0/1/en | AGREE | Latin p. 212 begins 'In illo tempore: Maria Magdalene' (no Mk 16:1a); English (Douay) now matches |
| 26 | A2.json #65 | data/orations.js | Pasc0h/se/0 | AGREE | p. 219 (pdf 148) as printed |
| 27 | A2.json #73 | data/readings33.js | Pasc0f/0/la | AGREE | p. 219 (pdf 148) as printed (facit; no stray stop) |
| 28 | A2.json #76 | data/orations.js | Pasc0s/se/0 | AGREE | p. 222 (pdf 150) as printed |
| 29 | A2.json #95 | data/orations.js | Pasc2w/pc/0 | AGREE | p. 316 (pdf 197) as printed |
| 30 | A2.json #119 | data/orations.js | Litaniis/or/0 | AGREE | p. 231 (pdf 154) as printed |
| 31 | A2.json #124 | data/readings33.js | Pasc5/1/en | AGREE | Latin p. 229 (pdf 153) 'In illo tempore: Dixit Jesus discipulis suis: Amen, amen'; English (Douay) matches |
| 32 | A2.json #128 | data/readings33.js | Asc/0/la | AGREE | pp. 236-237 (pdf 157) as printed |
| 33 | A2.json #143 | data/readings33.js | Pent0/1/en | AGREE | Latin p. 246 (pdf 162) 'Dixit Jesus discipulis suis: Si quis...sic facio'; English matches |
| 34 | A2.json #145 | data/readings33.js | Pent0m/0/la | AGREE | pp. 246-247 (pdf 162) as printed |
| 35 | A2.json #162 | data/orations.js | Pent0h/or/0 | AGREE | p. 251 (pdf 164) as printed |
| 36 | A2.json #163 | data/orations.js | Pent0h/se/0 | AGREE | p. 252 (pdf 165) as printed |
| 37 | A2.json #189 | data/orations.js | Pent0m/or/0 | AGREE | p. 247 (pdf 162) as printed |
| 38 | A2.json #190 | data/orations.js | Pent0w/or/0 | AGREE | p. 249 (pdf 163) as printed |
| 39 | A2.json #193 | data/orations.js | Pent1/or/0 | AGREE | pp. 256-257 (pdf 167) as printed |
| 40 | A2.json #198 | data/readings33.js | Pent1/1/en | AGREE | Latin p. 258 (pdf 168) 'Dixit Jesus discipulis suis: Data est'; English matches |
| 41 | A2.json #223 | data/readings33.js | SCJ/0/la | DISAGREE | Suppl. p. 7 (pdf 362) prints 'in cæléstibus per Ecclésiam multifórmis sapiéntia Dei' and 'omnis patérnitas in cælis et in terra nominátur' - no comma after 'Ecclésiam' nor after 'cælis'; new adds both commas. Rest as printed. |
| 42 | A2.json #229 | data/readings33.js | Pent3/1/la | AGREE | p. 265 (pdf 171) as printed |
| 43 | A3.json #2 | data/readings33.js | S1102_2/0/la | AGREE | p. 610-611 (pdf 344) as printed |
| 44 | A3.json #3 | data/readings33.js | S1102_2/1/la | AGREE | p. 612 (pdf 345) as printed |
| 45 | A3.json #6 | data/orations.js | S1112/pc/0 | AGREE | p. 620 (pdf 349) as printed |
| 46 | A3.json #14 | data/masses.js | masses/S1106/parts/al | AGREE | p. 616 (pdf 347) 'Officium Intret, de Communi plurimorum Martyrum, pag. 14*'; p. 15* (pdf 375) one verse 'Te Martyrum candidatus' (gabc 4992 = Te Martyrum); 5648 = Sancti et justi (Paschal). Rule XIII.4 one verse. (Note: 5648 still listed in S1106 'extras'.) |
| 47 | A3.json #31 | data/readings33.js | S1119/1/la | AGREE | p. 626 (pdf 352) as printed |
| 48 | A3.json #38 | data/readings33.js | S1122/0/la | AGREE | pp. 628-629 (pdf 353) as printed |
| 49 | A3.json #56 | data/orations.js | S1130/pc/0 | AGREE | p. 324 (pdf 201) as printed |
| 50 | A3.json #66 | data/orations.js | S1206/or/0 | AGREE | p. 328 (pdf 203) as printed |
| 51 | A3.json #68 | data/orations.js | S1206/pc/0 | AGREE | p. 329 (pdf 203) as printed |
| 52 | A3.json #73 | data/orations.js | S1207v/se/0 | AGREE | p. 332 (pdf 205) as printed |
| 53 | A3.json #87 | data/readings33.js | S1220 | DISAGREE | Minor, English only. Choice of readings agrees with rubric p. 338 ('Os justi, ut in Comm. unius Abbatis, pag. 25*') and Lesson Latin agrees with p. 25* (pdf 380: 'Dilectus Deo, et hominibus: ... legem vitae et disciplinae'); Gospel p. 26* begins 'In illo tempore: Dixit Petrus ad Jesum: Ecce nos reliquimus'. But the English does not match its Latin: Lesson English begins 'Moses was beloved of God' (Latin has no 'Moyses'); Gospel English 'Then Peter answering, said to him' (Latin 'Dixit Petrus ad Jesum' = 'Peter said to Jesus'). |
| 54 | A3.json #95 | data/orations.js | S1226/or/0 | AGREE | p. 340 (pdf 209) as printed |
| 55 | A3.json #109 | data/readings33.js | S1228/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 56 | A3.json #112 | data/readings33.js | S1229/0/en | AGREE | Latin p. 346 (pdf 212) 'Fratres: Omnis pontifex'; English now 'Every high priest' matches |
| 57 | A3.json #123 | data/orations.js | S1206/pc/1 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 58 | A3.json #126 | data/masses.js | masses/S0113/en | NOT CHECKED | stopped by coordinator before this entry was checked |
| 59 | A3.json #127 | data/masses.js | masses/S0113/name_en | NOT CHECKED | stopped by coordinator before this entry was checked |
| 60 | A3.json #138 | data/readings33.js | S0117/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 61 | A3.json #141 | data/readings33.js | S0117/1/en | AGREE | Latin p. 354 (pdf 216) 'Dixit Jesus discipulis suis: Sint lumbi'; English matches |
| 62 | A3.json #159 | data/orations.js | S0121/se/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 63 | A3.json #177 | data/readings33.js | S0128/1/en | AGREE | Latin p. 366 (pdf 222) 'Dixit Jesus discipulis suis: Nolite timere'; English matches |
| 64 | A3.json #182 | data/readings33.js | S0123/1/en | AGREE | Latin p. 20* (pdf 378) 'Dixit Jesus discipulis suis: Vos estis sal'; English matches |
| 65 | A3.json #189 | data/readings33.js | S0202/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 66 | A4.json #8 | data/readings33.js | S0526/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 67 | A4.json #11 | data/readings33.js | G481/0/en | AGREE | English (Douay) cut to the Latin ending 'amicitiae Dei' (Wis 7:14a) |
| 68 | A4.json #38 | data/orations.js | S0624/or/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 69 | A4.json #43 | data/orations.js | S0626/se/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 70 | A4.json #59 | data/readings33.js | G502_3/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 71 | A4.json #69 | data/orations.js | S0701/or/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 72 | A4.json #95 | data/readings33.js | S0710/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 73 | A4.json #97 | data/readings33.js | S0711/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 74 | A4.json #106 | data/readings33.js | S0718/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 75 | A4.json #124 | data/orations.js | S0725/or/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 76 | A4.json #127 | data/readings33.js | S0725/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 77 | A4.json #143 | data/masses.js | masses/S0709/season/asc | NOT CHECKED | stopped by coordinator before this entry was checked |
| 78 | A4.json #150 | data/masses.js | masses/S0726/parts/in/0/m39text | NOT CHECKED | stopped by coordinator before this entry was checked |
| 79 | A4.json #158 | data/readings33.js | S0624/1/en | AGREE | English (Douay, cut) matches the Latin Isa 49:1-3,5-7 as on the site |
| 80 | A4.json #162 | data/readings33.js | S0611/0/en | DISAGREE | English drops the Missal's 'Antiochíæ' in the first sentence: Latin 'Multus númerus credéntium Antiochíæ convérsus est ad Dóminum'; new English 'A great number believing, were converted to the Lord' (the old English had 'at Antioch'). Should read e.g. 'A great number believing at Antioch were converted to the Lord.' |
| 81 | A4.json #166 | data/orations.js | S0719/en_src | NOT CHECKED | stopped by coordinator before this entry was checked |
| 82 | A4.json #183 | data/readings33.js | S0809v/0/en | DISAGREE | Minor. Print p. 523 (pdf 300): '...quóniam éruis sustinéntes te, et líberas eos de mánibus géntium, Dómine Deus noster.' (no 'Dómine' after 'sustinéntes te'). The new English keeps Douay's 'them that wait for thee, O Lord,' and adds 'O Lord our God' at the end, so the vocative appears twice; it should be 'How thou deliverest them that wait for thee, and savest them out of the hands of the nations, O Lord our God.' (Removal of the Eccli 51:1 heading is right.) |
| 83 | A4.json #188 | data/orations.js | S0810/pc/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 84 | A4.json #190 | data/readings33.js | S0810/0/en | AGREE | Latin 'Fratres: Qui parce seminat'; English without 'This I say' matches |
| 85 | A4.json #213 | data/readings33.js | S0817/0/en | AGREE | Latin 'Fratres: Fiduciam habuimus'; English without 2:2a matches |
| 86 | A4.json #217 | data/readings33.js | S0820/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 87 | A4.json #218 | data/readings33.js | S0821/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 88 | A4.json #225 | data/readings33.js | S0824/0/en | AGREE | Latin ends 'charismata meliora'; English ends 'better gifts' matches |
| 89 | A4.json #230 | data/readings33.js | S0825/1/en | AGREE | Latin p. 540 (pdf 309) 'Dixit Jesus discipulis suis parabolam hanc'; English matches |
| 90 | A4.json #231 | data/readings33.js | S0827/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 91 | A4.json #234 | data/readings33.js | S0825/0/en_src | NOT CHECKED | stopped by coordinator before this entry was checked |
| 92 | A5.json #0 | data/orations.js | C7s/or | NOT CHECKED | stopped by coordinator before this entry was checked |
| 93 | A5.json #19 | data/masses.js | masses/C30s/en | NOT CHECKED | stopped by coordinator before this entry was checked |
| 94 | A5.json #33 | data/readings33.js | C51s/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 95 | A5.json #34 | data/readings33.js | C51s/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 96 | A5.json #56 | data/orations.js | C79s/pc/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 97 | A5.json #71 | data/readings33.js | C93s/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 98 | A5.json #81 | data/readings33.js | S1114b/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 99 | A5.json #93 | data/readings33.js | S0724b/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 100 | A5.json #98 | data/readings33.js | S0906b_2/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 101 | A5.json #105 | data/readings33.js | S0102b/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 102 | A5.json #108 | data/readings33.js | S0512b/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 103 | A5.json #114 | data/readings33.js | S0512b/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 104 | A5.json #138 | data/readings33.js | S0602b/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 105 | A6.json #15 | data/readings33.js | S0119b/1/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 106 | A6.json #23 | data/readings33.js | S0103b/0/ref | NOT CHECKED | stopped by coordinator before this entry was checked |
| 107 | A6.json #25 | data/readings33.js | S0103b/0/title_en | NOT CHECKED | stopped by coordinator before this entry was checked |
| 108 | A6.json #45 | data/readings33.js | S0228b/1/en | DISAGREE | English begins 'At that time: The kingdom of heaven is like...' but the Latin (p. 38*, pdf 387) begins 'Dixit Jesus discípulis suis parábolam hanc: Símile est regnum'; English lacks 'Jesus spoke this parable to his disciples:' (the standard the other fixes apply, e.g. A4 S0825) |
| 109 | A6.json #51 | data/readings33.js | S0808b/0/title_en | NOT CHECKED | stopped by coordinator before this entry was checked |
| 110 | A6.json #60 | data/masses.js | masses/S0808b/readings/1 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 111 | A6.json #63 | data/readings33.js | S0609b/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 112 | A6.json #75 | data/readings33.js | S0904b/1/en | DISAGREE | English 'At that time: Then shall the kingdom of heaven be like to ten virgins' but the Latin (p. 30*-31*) is 'Dixit Jesus discípulis suis parábolam hanc: Símile erit regnum cælórum'; English lacks 'Jesus spoke this parable to his disciples:' and keeps Douay 'Then'. Readings choice (Comm. Virg. non Mart. p. 30*) itself agrees with rubric |
| 113 | A6.json #96 | data/readings33.js | S1030b/0/la | NOT CHECKED | stopped by coordinator before this entry was checked |
| 114 | A6.json #104 | data/masses.js | masses/S1012b/readings | NOT CHECKED | stopped by coordinator before this entry was checked |
| 115 | A6.json #115 | data/memoriae.js | 0531|S. Petronillæ Virg./pc/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 116 | A6.json #121 | data/memoriae.js | 0803|Inventio Corporis S. Stephani Protomartyris/or/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 117 | A6.json #130 | data/memoriae.js | 0701|Octava S. Joannis Baptistæ/se/0 | NOT CHECKED | stopped by coordinator before this entry was checked |
| 118 | A6.json #136 | data/masses.js | masses/S0529b/season/pasch | NOT CHECKED | stopped by coordinator before this entry was checked |

## Summary

- Sample size: 119; checked: 69; not checked (stopped): 50
- AGREE 58 / DISAGREE 11 / CANNOT VERIFY 0
- Typographic note (not counted): the print never accents capitals ('Angelus', 'Anima', 'Ideo'); some entries write 'Ángelus', 'Ánima', 'Ídeo' (A1 Dec25_1, Nat2, Quad1h; A2 Quad6m), others 'Angelis' (A2 Pent3). Convention only.
- Side note: S1106 still lists 5648 (Sancti et justi) in 'extras' after A3 removed it from parts.al.

## DISAGREE items (correct text as printed)

- **#7 A1.json #60 data/orations.js Nat1/se/0** (M39 p. 27 (pdf 47)): p. 27 (pdf 47) prints 'obtíneat' (accented); new has 'obtineat'. Rest (punctuation change) as printed.
- **#17 A1.json #183 data/orations.js Quad2/or/0** (M39 p. 79 (pdf 73)): p. 79 (pdf 73): body as printed, but the print ends 'mundémur in mente : Per Dóminum.' (colon before the conclusion); new has 'in mente. Per Dóminum' (mark before the conclusion, not canon()-handled)
- **#18 A1.json #193 data/orations.js Adv3f/en_src** (M39 p. 9 (pdf 38)): Labels Adv3f Secret English 'ai', but the St Dominic Missal 1959 does print English for this Latin (Ember Friday of Advent, DM key T4: 'Having received our gifts and prayers, we beseech You, Lord, to cleanse us by these heavenly mysteries and mercifully to hearken to us: through our Lord.' per tools/orat39/dm_prayers.json); RULINGS allow AI only where DM 1959 has none. (dm.pdf scan itself not on this machine.)
- **#19 A1.json #194 data/orations.js 7a/se/1** (M39 p. 49 (pdf 58)): English matches its Latin, but it is an AI translation where the St Dominic Missal 1959 has English for the same Secret (Septuagesima Sunday T19 has the Latin; same Latin with English in T4 Ember Friday of Advent: 'Having received our gifts and prayers...'); RULINGS: use DM 1959 verbatim. Latin (Muneribus nostris) checked p. 49 not needed.
- **#20 A2.json #2 data/orations.js Quad5s/pc/0** (M39 pp. 136-137 (pdf 102)): p. 136-137 (pdf 102) prints 'satiáti, quǽsumus Dómine Deus noster; ut hujus' - no comma after Dómine; new has 'quǽsumus Dómine, Deus noster;'
- **#41 A2.json #223 data/readings33.js SCJ/0/la** (M39 suppl. p. 7 (pdf 362R)): Suppl. p. 7 (pdf 362) prints 'in cæléstibus per Ecclésiam multifórmis sapiéntia Dei' and 'omnis patérnitas in cælis et in terra nominátur' - no comma after 'Ecclésiam' nor after 'cælis'; new adds both commas. Rest as printed.
- **#53 A3.json #87 data/readings33.js S1220** (M39 p. 338 (pdf 208) and pp. 25*-26* (pdf 380-381)): Minor, English only. Choice of readings agrees with rubric p. 338 ('Os justi, ut in Comm. unius Abbatis, pag. 25*') and Lesson Latin agrees with p. 25* (pdf 380: 'Dilectus Deo, et hominibus: ... legem vitae et disciplinae'); Gospel p. 26* begins 'In illo tempore: Dixit Petrus ad Jesum: Ecce nos reliquimus'. But the English does not match its Latin: Lesson English begins 'Moses was beloved of God' (Latin has no 'Moyses'); Gospel English 'Then Peter answering, said to him' (Latin 'Dixit Petrus ad Jesum' = 'Peter said to Jesus').
- **#80 A4.json #162 data/readings33.js S0611/0/en** (M39 pp. 464-465 (pdf 271)): English drops the Missal's 'Antiochíæ' in the first sentence: Latin 'Multus númerus credéntium Antiochíæ convérsus est ad Dóminum'; new English 'A great number believing, were converted to the Lord' (the old English had 'at Antioch'). Should read e.g. 'A great number believing at Antioch were converted to the Lord.'
- **#82 A4.json #183 data/readings33.js S0809v/0/en** (M39 p. 523 (pdf 300)): Minor. Print p. 523 (pdf 300): '...quóniam éruis sustinéntes te, et líberas eos de mánibus géntium, Dómine Deus noster.' (no 'Dómine' after 'sustinéntes te'). The new English keeps Douay's 'them that wait for thee, O Lord,' and adds 'O Lord our God' at the end, so the vocative appears twice; it should be 'How thou deliverest them that wait for thee, and savest them out of the hands of the nations, O Lord our God.' (Removal of the Eccli 51:1 heading is right.)
- **#108 A6.json #45 data/readings33.js S0228b/1/en** (M39 p. 38* (pdf 387)): English begins 'At that time: The kingdom of heaven is like...' but the Latin (p. 38*, pdf 387) begins 'Dixit Jesus discípulis suis parábolam hanc: Símile est regnum'; English lacks 'Jesus spoke this parable to his disciples:' (the standard the other fixes apply, e.g. A4 S0825)
- **#112 A6.json #75 data/readings33.js S0904b/1/en** (M39 p. 550 (pdf 314) rubric; readings M39 pp. 30*-31* (pdf 383)): English 'At that time: Then shall the kingdom of heaven be like to ten virgins' but the Latin (p. 30*-31*) is 'Dixit Jesus discípulis suis parábolam hanc: Símile erit regnum cælórum'; English lacks 'Jesus spoke this parable to his disciples:' and keeps Douay 'Then'. Readings choice (Comm. Virg. non Mart. p. 30*) itself agrees with rubric
