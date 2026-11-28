from clus import *; from fx import get
s = 'M39 p. 26* (pdf 381), Comm. Abbatis'
R = [('te: quid ergo', 'te: Quid ergo')]
for k in ('S0207', 'S1220', 'S0321', 'S1103b'):
    canon_entry(k, 1, R, s, "Commune copy (Matth. 19: 27-29, p. 26*): 'secúti sumus te : Quid ergo erit nobis?' (seen on the scan; 'quod vos, qui' with a comma, the text layer's '.' is wrong)")
for k, p in (('S0125', 'M39 p. 364 (pdf 221)'), ('S0212', 'M39 p. 380 (pdf 229)'), ('S1112', 'M39 p. 620 (pdf 349)')):
    canon_entry(k, 1, R, p, "own print: 'sumus te : Quid ergo erit nobis?' (seen on the scan; as the Commune p. 26*)")
en = get(RF, ['S0117', 0, 'en'])
add_ok = __import__('fx').add(RF, ['S0712', 0, 'en'], en, 'M39 pp. 494-495 (pdf 286)',
    "English as the other copies of Eccli. 45: 1-6 (S0117, S0207, S1220 ...): the Missal's Latin begins 'Diléctus Deo' (no 'Moyses') and ends 'legem vitæ et disciplínæ', so no 'Moses was' and no 'that he might teach Jacob his covenant, and Israel his judgments' (CHECK.md #53, the same slip)")
print(add_ok)
