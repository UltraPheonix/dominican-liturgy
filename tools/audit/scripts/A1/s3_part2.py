# ---- Missing Epistles (op add)
la_a='Fratres: Rogámus vos per advéntum Dómini nostri Jesu Christi, et nostræ congregatiónis in ipsum: ut non cito moveámini a vestro sensu, neque terreámini, neque per spíritum, neque per sermónem, neque per epístolam tamquam per nos missam, quasi instet dies Dómini. Ne quis vos sedúcat ullo modo: Quóniam nisi vénerit discéssio primum, et revelátus fúerit homo peccáti, fílius perditiónis, qui adversátur, et extóllitur supra omne, quod dícitur Deus, aut quod cólitur, ita ut in templo Dei sédeat osténdens se tamquam sit Deus. Non retinétis quod cum adhuc essem apud vos, hæc dicébam vobis? Et nunc quid detíneat scitis, ut revelétur in suo témpore. Nam mystérium jam operátur iniquitátis: tantum ut qui tenet nunc, téneat, donec de médio fiat. Et tunc revelábitur ille iniquus, quem Dóminus Jesus interfíciet spíritu oris sui, et déstruet illustratióne advéntus sui.'
B2='Ad Thessalonicenses 2'
v=[V(B2,2,n) for n in range(1,9)]
a='And we beseech you, brethren, by'; assert v[0].startswith(a); v[0]='Brethren: We beseech you by'+v[0][len(a):]
assert v[7].endswith('brightness of his coming, him,'); v[7]=v[7][:-len(', him,')]+'.'
en_a=' '.join(v)
note_a='opening "And we beseech you, brethren, by" -> "Brethren: We beseech you by" (Missal "Fratres: Rogámus vos per"); v. 8 ends at "his coming" as the Latin does (Douay\'s ", him," belongs to v. 9)'
add(RD,['Adv3s',6],{'type':'Epistle','ref':'Ad Thessalonicenses 2 2: 1-8','title':'Léctio Epístolæ beáti Pauli Apóstoli ad Thessalonicénses.','title_en':'Lesson from the Second Epistle of blessed Paul the Apostle to the Thessalonians.','la':la_a,'en':en_a,'p33':None,
   'src':'Missale O.P. 1939, pp. 13-14 (pdf 40-41), transcribed from the scan ("iniquus" without accent as printed); English: Douay-Rheims, bible/en 2 Thess 2: 1-8 ; '+note_a},
   'M39 pp. 13-14 (pdf 40-41)','EPISTLE MISSING: the Missal prints the Epistle 2 Thess 2: 1-8 after the Daniel lesson and its collects (title "Léctio Epístolæ beáti Pauli Apóstoli ad Thessalonicénses. 2, c. 2"); masses.js lists it, readings33 lacked it. Latin read from the scan crop; English bible/en')
la_e='Fratres: Habéntes donatiónes secúndum grátiam, quæ data est nobis, differéntes: Sive prophetíam secúndum ratiónem fídei, sive ministérium in ministrándo, sive qui docet in doctrína, qui exhortátur in exhortándo, qui tríbuit in simplicitáte, qui præest in sollicitúdine, qui miserétur in hilaritáte. Diléctio sine simulatióne. Odiéntes malum, adhæréntes bono: Caritáte fraternitátis ínvicem diligéntes: Honóre ínvicem præveniéntes: Sollicitúdine non pigri: Spíritu fervéntes: Dómino serviéntes: Spe gaudéntes: In tribulatióne patiéntes: Oratióni instántes: Necessitátibus sanctórum communicántes: Hospitalitátem sectántes. Benedícite persequéntibus vos: benedícite et nolíte maledícere. Gaudére cum gaudéntibus, flere cum fléntibus: Idípsum ínvicem sentiéntes: Non alta sapiéntes, sed humílibus consentiéntes.'
R12='Ad Romanos'
v=[V(R12,12,n) for n in range(6,17)]
a='And having different gifts'; assert v[0].startswith(a); v[0]='Brethren: Having different gifts'+v[0][len(a):]
c=' Be not wise in your own conceits.'; assert v[-1].endswith(c); v[-1]=v[-1][:-len(c)]
en_e=' '.join(v)
note_e='opening "And having" -> "Brethren: Having" (Missal "Fratres: Habéntes"); v. 16 ends at "consenting to the humble" as the Latin does'
add(RD,['Epi2',1],{'type':'Epistle','ref':'Ad Romanos 12: 6-16','title':'Léctio Epístolæ beáti Pauli Apóstoli ad Romános.','title_en':'Lesson from the Epistle of blessed Paul the Apostle to the Romans.','la':la_e,'en':en_e,'p33':None,
   'src':'Missale O.P. 1939, pp. 40-41 (pdf 54), transcribed from the scan; English: Douay-Rheims, bible/en Rom 12: 6-16 ; '+note_e},
   'M39 pp. 40-41 (pdf 54)','EPISTLE MISSING: the Missal prints the Epistle Rom 12: 6-16 ("Léctio Epístolæ beáti Pauli Apóstoli ad Romános. c. 12"); readings33 had only the Gospel, masses.js only the reference. Latin read from the scan crop; English bible/en')
