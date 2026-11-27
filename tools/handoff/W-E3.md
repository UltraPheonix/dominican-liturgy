# W-E3: readings cut at a page break (data/readings33.js). Stopped 27 Nov at the coordinator's request.

## Mechanism (done, tested)
- `tools/m33/tails.json`: a list of {k, ref, new_ref, page, la: [[old_suffix, new_suffix]], en: [[...]]}.
- `tools/m33/tails.py`: suffix replacement. A pair is applied only while the field still ends with `old`, and it is
  skipped if the field already ends with `new`. This makes it idempotent (run twice: "0 tail fixes"). A pair that
  matches neither is logged. `python3 tools/m33/tails.py` patches data/readings33.js in place, and is safe after
  tools/requiem/build.py.
- `tools/m33/run.sh` now calls `tails.apply(out)` just before it writes the file, so a rebuild keeps the fixes.
- **Warning:** a bare `bash tools/m33/run.sh` does NOT reproduce the live file:
  - It drops C114s/C114o, so run tools/requiem/build.py after it.
  - It adds S0924 (Ecclus 24: 14-16).
  - It rewrites tools/m33/readings33b.json.gz with 64 more keys.
  So patch the live file with `python3 tools/m33/tails.py` instead of rebuilding. Backup of the original live file:
  /tmp/rt/readings33.orig.js.

## Fixed and applied (checked against the 1939 scan)
- **Adv2 Rom 15:** + "pópuli. Et rursus Isaías ait: … virtúte Spíritus Sancti."; ref 15: 4-13; English v12-13 from
  Douay. Missal p. 4 (pdf 36).

## Located, not applied (the text-layer @@PAGE n = pdf page n+1; read accents from the scan, pdftoppm -r 150)
| Key | Fix | m39lin @@PAGE |
|---|---|---|
| Epi | drop " Omne"; ref 60: 1-6; English trim after "praise to the Lord." (also "the. strength" -> "the strength") | 50 |
| Quad1h | "vita vivet, ait Dóminus" -> "vita vivet. Ait Dóminus omnípotens."; EN "saith the Lord almighty." | 69 |
| Quad1f | "moriétur in moriétur. Et cum avérterit se ímpius" -> "moriétur in eis: In injustítia, quam operátus est, moriétur. Et cum avérterit se ímpius ab impietáte sua, quam operátus est, et fécerit judícium, et justítiam: ipse ánimam suam vivificábit. Considérans enim, et avértens se ab ómnibus iniquitátibus suis, quas operátus est, vita vivet, et non moriétur. Ait Dóminus omnípotens."; ref 18: 20-28; EN + v28 + "Saith the Lord almighty." | 69 |
| Quad2h | retake whole: "Hæc dicit Dóminus Deus: Maledíctus homo … juxta fructum adinventiónum suárum. Dicit Dóminus omnípotens." (m39lin lines 16912-16940); ref 17: 5-10; EN Douay 17:5-10 + "Saith the Lord almighty." | 76 |
| Quad5m | "et misértus est" -> "Et misértus est pópulo suo Dóminus Deus noster."; EN end "…and the Lord our God had mercy on his people." | 96 |
| Pasc0h | + "Generatiónem ejus quis enarrábit … donec veníret Cæsaréam, nomen Dómini Jesu Christi." (lines 30157-30188); ref 8: 26-40; EN Douay v34-40 | 147-148 |
| Pent0s (3rd Lesson) | + "."; EN trim after "hath given thee." | 165 |
| Pent22 | + " et laudem Dei." (EN already complete) | 189 |
| C30s, S0603, S1211 | + " constítuet eum." (EN complete) | 201, 202, 212 |
| C62s | 1933 p678-679 runs to v29: + "mandu­cáverit panem hunc, vel bíberit cálicem Dómini indígne: reus erit córporis, et sánguinis Dómini. Probet autem seípsum homo: et sic de pane illo edat, et de cálice bibat. Qui enim mandúcat, et bibit indígne, judícium sibi mandúcat, et bibit: non dijúdicans corpus Dómini."; ref 11: 23-29; EN + Douay v28-29 (votive 1939) | 387 |
| C85s | + "Christo Jesu Dómino nostro."; EN "as the truth is in Christ Jesus our Lord." | 400 |
| S0122 | short form (1933 p653-654 = 1939): "…apud próximos suos: et" -> "…apud próximos suos. Et nómine ætérno hereditábit illum, Dóminus Deus noster."; EN trim after "among his neighbours." + "And the Lord our God shall cause him to inherit an everlasting name." | 371 |
| S0424 | + "."; EN drop "Thy hair is as flocks of goats… Galaad. " and trim after "thou shalt be crowned." | 246 |
| S0430 | + "parábolam locútus est eis…eructábo abscóndita a constitutióne mundi."; ref 13: 31-35; EN + Douay v34-35 (confirm which of @@245/250 is S0430) | 245/250 |
| S0822 | + "veritátis: in me omnis spes vitæ, et virtútis. Transíte ad me … vitam ætérnam habébunt."; ref 24: 23-31; EN + Douay v26-31 | 360 |
| S0908, S1207v | + "vocátur Christus." (EN complete) | 314, 204 |
| S0920, S0920v, S1129v, G369 | + " Dóminus corónam glóriæ."; EN last sentence -> "He made an everlasting covenant with him, and girded him about with a girdle of justice, and the Lord put on him a crown of glory." | 320, 198 |
| S0119b | stray " In" is the heading "In festo" (1933 p666): drop it; ref 10: 1-9; EN trim after "is come nigh unto you." | 1933 p666 |
| S0120, S0813 | the Latin is cut: "probáti." -> "probáti invénti sunt: In Christo Jesu Dómino nostro."; EN "…approved by the testimony of faith, were found in Christ Jesus our Lord." | 217, 301 |

## English-only endings (42 readings; list them with /tmp/w3/en.js)
- Trim the English to the Latin:
  - Pasc2w: end at "the son of Joseph."
  - Pent9: end at "in the temple."
  - EmbSatSept: end at "Thus saith the Lord of hosts."
  - S0327/G446: end at "the wages of their labours." (Latin complete, @@240)
  - S0630/G505: end at "the grace that was given to me." (Latin complete, @@220). Also check the Latin "(Qui enim operátus est Petro…" opening, which is lost.
- **S0611:** the English is empty. Build it from Douay Acts 11:21-26 and 13:1-3.
- **The rest:** change the final ":" ";" or "," to ".". Fix the typo in S0815 ("cinnamon. and").

## Resume
1. Read each page in the scan (pdf = @@PAGE+1) and take the accents from it.
2. Add each entry to tails.json, then run `python3 tools/m33/tails.py` twice (the second run must print 0).
3. Run `node /tmp/rt/dump.js`; it must list no cut Latin.
4. Load the pages in headless Chrome, then run mass_sweep on port 8768.
