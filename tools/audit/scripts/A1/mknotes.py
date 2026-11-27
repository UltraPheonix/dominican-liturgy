import json
N={'stopped':'Done on the scan: Adv1 to Adv3s (see table). Next: Adv4.',
'method':[
 'Orations: word by word and punctuation against the scan (`;` flexa, `:` elevatio, Proc. 1913 p. 405), incl. the `:` the Missal prints before the conclusion. Conclusion type checked against Rubr. gen. XI.2 (M39 p. 52, pdf 28): "Si Oratio dirigatur ad Patrem, concluditur Per Dominum nostrum; et si ad Filium, Qui vivis et regnas cum Deo Patre; si in principio Orationis fiat mentio Filii, terminatur Per eumdem Dominum nostrum; si in fine Orationis fiat ejus mentio, terminatur per Qui tecum vivit". The site type was compared with the abbreviation the Missal prints after each prayer (concl.py). The expanded conclusions themselves are kept as they are.',
 'Readings: word, punctuation and case diff (run.py, case.py), plus the Missal text before/after each reading (headtail.txt) for cuts at start or end; every accepted item seen on a scan crop.',
 'Chants: the gabc text of each id aligned to the Missal (run.py); an id is right when it matches the incipit/verse printed in this Mass.',
 'English: read against the Latin for missing clauses only.',
 'i/j not folded back (left for the site-wide script). Accents on capitals follow the site (e.g. Ángelus) when only the case changes.'],
'mass':{
 'Adv1':['M39 pp. 1-3 (pdf 34-35)','FIXED (earlier pass): orations punct/spelling. Readings OK. Chants OK.'],
 'Adv2':['M39 pp. 4-5 (pdf 34-35)','FIXED: Gospel 2 commas (Jesus, / Joánni,). Orations (from M39) OK; conclusions OK (or Qui tecum = Missal "Qui tecum."). Chants in/gr/al/of/co match pp. 4-5. English OK.'],
 'Adv3':['M39 pp. 5-6 (pdf 36-37)','FIXED (earlier pass): orations punct; Epistle cut ending "Dómino nostro." restored; Gospel punct/case. OPEN: Epistle English lacks "our Lord" at the end.'],
 'Adv3w':['M39 pp. 6-8 (pdf 37-38)','FIXED: or (punct 3, "solémnitas,"), se ("Accépta"), pc (punct 5, "múnere"); Isaias 2 cut ending "Dei nostri." restored, case 2; Isaias 7 "mei"->"mel", "tuo in"; Gospel punct 6, case 11 (Angelus, Benedícta, Sanctum...). Chants OK (Introit #5489 is the same Rorate text, printed elsewhere). OPEN: 2nd collect Festína (p. 7) comes from memoriae.js via app.js, not checked here.'],
 'Adv3f':['M39 pp. 9-10 (pdf 38)','FIXED: or punct 2; se punct + quǽsumus/cæléstibus; pc punct 2; Isaias 11 "nos"->"flos", "injustítia"->"in justítia", punct 6, case 1; Gospel punct 4, case 4. Chants OK. OPEN: Secret has no English.'],
 'Adv3s':['M39 pp. 10-15 (pdf 39-41)','FIXED: or/se/pc punct; Lesson 1 cut ending "Dóminus Deus noster."; Lessons 2 and 3 begin "Hæc dicit Dóminus" (site had "Dicit"); Lesson 2 cut ending "Ait Dóminus omnípotens."; Lesson 3 cut ending ", Dóminus Deus noster."; Daniel 3 missing sentence "Flamma autem … incendébant." added; case 14 (christo, Ecce, Portas…). Chants OK. OPEN: Epistle 2 Thess 2 missing; lesson collects; Daniel English.'],
},
'open':[
 'Adv3 Epistle English: add "our Lord" at the end to match "In Christo Jesu Dómino nostro." (English source needed; not written from memory).',
 'Adv3f Secret and 7a Secret: English is empty (data/orations.js [k].se[1]).',
 '**Missing Epistles** (data/readings33.js lacks the reading; masses.js lists it; a fixes entry cannot add a list item without the whole text and its English): Adv3s 2 Thess 2: 1-8 (M39 p. 13, pdf 40-41); Quad1s 1 Thess 5: 14-23; Epi2 Rom 12: 6-16; Quad2 1 Thess 4: 1-7. For Adv3s and Quad1s the Epistle is not shown at all (m33Readings keeps only the readings33 lessons); for Epi2 and Quad2 only the masses.js reference is left. To verify and transcribe from the scan.',
 'Adv3s Daniel 3 English: the added Latin sentence ("Flamma autem effundebátur … incendébant", Dan 3: 47-48) has no English yet; the ref "Daniel 3: 49-51" in readings33 should then read 47-51 as masses.js has it (the Missal prints only "c. 3").',
 'Ember days Adv3w/Adv3s (and Lent Ember days): the collects the Missal prints after each lesson (e.g. Adv3s pp. 11-13: Concede, Indignos, Præsta, Preces, Deus qui tribus pueris) are not in data/orations.js and are not shown by app.js (only "or" after the Kyrie). Structural; for the coordinator.',
],
'questions':[
 'Expanded conclusions: the site keeps the Divinum Officium form "Qui vivis et regnas cum Deo Patre, in unitáte Spíritus Sancti, Deus, per ómnia sǽcula sæculórum." The Missal prints only "Qui vivis." / "Per Dóminum." in the Masses. RULINGS gives "Patre; in unitáte Spíritus Sancti Deus :". Which printed form (page) should the expanded conclusions follow? I left them unchanged (brief: keep the expanded conclusions).',
],
'leads':[],
'scripts':[
 'stream.py: M39.pdf word layer in reading order -> /tmp/A1/stream.json.',
 'cmp.py, run.py: align and diff each site text with the Missal -> /tmp/A1/diff/KEY.txt, items_all.json, loc_all.json (cp to items_frozen.json).',
 'review.py KEY: numbered P/W items + scan crops /tmp/A1/rv/KEY_n.png. case.py KEY: case differences + crops (case_KEY.json). concl.py KEY: site conclusion vs the Missal abbreviation. show.py KEY: site data. q.py: crop a page.',
 'build_fix.py: builds fixes/A1.json from dec.json (per Mass: rejP, rejC, edits), merging with entries already there; skips Masses whose fixes are already applied.',
 'report.py / mknotes.py: write this report from notes.json.',
]}
import os
if os.path.exists('/tmp/A1/notes.json'):
    old=json.load(open('/tmp/A1/notes.json'))
    if len(old['mass'])>len(N['mass']): N=old
json.dump(N,open('/tmp/A1/notes.json','w'),ensure_ascii=False,indent=1)
