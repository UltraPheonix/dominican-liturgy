from clus import *; from fx import get
src = 'M39 pp. 1*-2* (pdf 369), Commune Dedicationis'
la0 = get(RF, ['Dedicatio', 0, 'la']); en0 = get(RF, ['Dedicatio', 0, 'en'])
copies(la0, en0, None, [('S1109', 0), ('S1118', 0)], src, "Commune copy (Dedication Lesson Apoc. 21): as printed p. 2*, 'eórum Deus : Et abstérget' (capital after the colon, seen on the scan)",
       "English as the Commune text: the Missal's Latin begins 'Vidi' (no 'ego Joannes'), so 'I saw', not 'I John saw'")
la1 = get(RF, ['Dedicatio', 1, 'la'])
copies(la1, None, None, [('S1109', 1), ('S1118', 1)], src, "Commune copy (Dedication Gospel Luc. 19): as printed p. 2*, 'ipse dives : Et quærébat' (capital after the colon, seen on the scan)", '')
