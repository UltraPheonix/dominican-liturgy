from clus import *; from fx import get, add
# 17* Hebr. 7
la = canon_entry('C30s', 0, [('pópuli: hoc enim', 'pópuli: Hoc enim')], 'M39 p. 17* (pdf 376)', "'deínde pro pópuli : Hoc enim' as printed (seen on the scan)")
en = get(RF, ['S1211', 0, 'en'])
copies(la, en, None, [('S1211', 0)], 'M39 p. 17* (pdf 376)', "Commune copy (Hebr. 7, p. 17*): 'pópuli : Hoc enim' (seen on the scan)", '')
add(RF, ['C30s', 0, 'en'], en, 'M39 p. 17* (pdf 376)', "English as S1211/S0703_2: the Missal's Latin ends 'seípsum offeréndo, Jesus Christus Dóminus noster' (seen), so ', Jesus Christ our Lord.'")
# 18* Eccli. 44-45
la = canon_entry('C32s', 0, [('justus: et in témpore', 'justus: Et in témpore')], 'M39 p. 18* (pdf 377)', "'invéntus est justus : Et in témpore' as printed ('ipsíus : et offérre' lower case, as printed; seen on the scan)")
copies(la, None, None, [(k, 0) for k in ('S0204', 'S0530b', 'S0803b', 'S1126b', 'S0317', 'S0610b', 'S0622b', 'S0707b', 'S0713b')], 'M39 p. 18* (pdf 377)',
       "Commune copy (Eccli. 44-45, Statuit p. 18*): 'justus : Et in témpore' (seen on the scan)", '')
w = "own print: 'justus : Et in témpore' and 'ipsíus : Et offérre' (both capitals seen on the scan; the Commune p. 18* has 'et offérre')"
canon_entry('S1104', 0, [('justus: et in témpore', 'justus: Et in témpore'), ('ipsíus: et offérre', 'ipsíus: Et offérre')], 'M39 p. 614 (pdf 346)', w)
canon_entry('S1111', 0, [('justus: et in témpore', 'justus: Et in témpore'), ('ipsíus: et offérre', 'ipsíus: Et offérre')], 'M39 p. 619 (pdf 348)', w)
canon_entry('S1117', 0, [('justus: et in témpore', 'justus: Et in témpore'), ('ipsíus: et offérre', 'ipsíus: Et offérre')], 'M39 p. 624 (pdf 351)', w)
# 19*-20* Matth. 25: 14-23
la = get(RF, ['C32s', 1, 'la']); en = get(RF, ['C32s', 1, 'en'])
copies(la, en, None, [('S0204', 1), ('S0317', 1)], 'M39 p. 19* (pdf 377)', "Commune copy (Matth. 25: 14-23, p. 19*): 'vocávit servos suos et trádidit' (no comma, seen on the scan)",
       "English as the Commune copy C32s: 'A man going into a far country called' (Latin 'Homo péregre profíciscens'; no 'Even as')")
