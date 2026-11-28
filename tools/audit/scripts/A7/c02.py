from clus import *
# 5* Jac 1 (pdf 370): 'est : Ipse autem', 'peccátum : Peccátum vero' seen
canon_entry('C7s', 0, [('est: ipse autem', 'est: Ipse autem'), ('peccátum: peccátum vero', 'peccátum: Peccátum vero')],
            'M39 p. 5* (pdf 370)', "capitals after the colon as printed: 'malórum est : Ipse autem', 'parit peccátum : Peccátum vero' (seen on the scan)")
# 7* Matt 16 (pdf 371): 'cum Angelis suis'
la = canon_entry('C11s', 1, [('cum ángelis suis', 'cum Angelis suis')], 'M39 p. 7* (pdf 371)', "'in glória Patris sui cum Angelis suis' as printed (capital, unaccented; seen on the scan)")
# S0203 prints the same Epistle and Gospel on its own page, p. 374 (pdf 226)
canon_entry('S0203', 0, [('Deus et ter Dómini', 'Deus et Pater Dómini')], 'M39 p. 374 (pdf 226)', "'Benedíctus Deus et Pater Dómini nostri' as printed (OCR 'ter'; seen on the scan; same as C11s p. 7*)")
canon_entry('S0203', 1, [('cum ángelis suis', 'cum Angelis suis')], 'M39 p. 374 (pdf 226)', "'cum Angelis suis' as printed (seen on the scan)")
# 8* Sap 5 and John 15 (pdf 372); John 15 also 11* (pdf 374), same text
canon_entry('C15s', 0, [('honóre: ecce quómodo', 'honóre: Ecce quómodo')], 'M39 p. 8* (pdf 372)', "'sine honóre : Ecce quómodo' as printed (seen on the scan)")
la = canon_entry('C15s', 1, [('pálmites: qui manet', 'pálmites: Qui manet')], 'M39 p. 8* (pdf 372)', "'vos pálmites : Qui manet' as printed (seen on the scan)")
copies(la, None, None, [('S0410b', 0)], 'M39 pp. 8*, 11* (pdf 372, 374)', "Commune copy (Joan. 15: 1-7, printed alike pp. 8* and 11*): 'vos pálmites : Qui manet' (seen on the scan)", '')
