# ---- G502 / S0703 St Irenaeus pp. 476-478 (pdf 277-278)
for fld in ('se','pc'):
    RAW('data/orations.js',['G502',fld,0],F.A.O['G502'][fld][0],F.A.O['S0703'][fld][0],'M39 pp. 477-478 (pdf 277-278)','G502 had the DO text; the Missal prints it as S0703 has it ('+('"suscípere, ut pax a tua pietáte concéssa, christianórum"' if fld=='se' else '"Deus auctor pacis et amátor, quem nosse, vívere, cui servíre, regnáre est"; "Irenǽi"; "nullíus"')+')')
for k in ('G502','S0703'):
    P(k,'r0',[0],'M39 p. 477 (pdf 277)',why='capital as printed ("Evangelístæ")')
    P(k,'r1',[0,1],'M39 p. 477 (pdf 277)',why='punctuation as printed ("occídere; sed"; "potest et ánimam")')
# ---- G502_3 Vigil of SS. Peter & Paul pp. 478-479 (pdf 278)
P('G502_3','r0',[0,1,2,3,4,5],'M39 p. 478 (pdf 278)',manual={5:'écstasi'},why='as printed: "Petrum et Joánnem"; ": In nómine"; "allevávit eum et"; ": Et intrávit"; ": Et impléti"; "écstasi"')
P('G502_3','r1',[1,4,5,6,7,8],'M39 pp. 478-479 (pdf 278)',why='as printed: "Simon Joánnis díligis"; "tértio, Amas me? et dixit ei"; "nosti : tu scis"; ": Cum autem"; "dixit, signíficans"')
