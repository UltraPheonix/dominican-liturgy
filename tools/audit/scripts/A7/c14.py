from clus import *; from fx import get
s = 'M39 pp. 13*-14* (pdf 374-375), Comm. plurimorum Martyrum (Salus autem)'
la = get(RF, ['S0911', 0, 'la']); en = get(RF, ['S0911', 0, 'en'])
copies(la, en, 'ai', [('C21s', 0), ('S0529b', 0), ('S0602b', 0)], s,
       "Sap. 10: 17-20 as printed p. 13* (= S0911, checked by A4): 'mirábili : Et fuit', 'noctem : Tránstulit', 'per Mare rubrum', 'et victrícem manum' (all seen on the scan)",
       "English as S0911 (AI translation of the Missal's Latin, which begins 'Réddidit Deus' and ends 'Dómine Deus noster', unlike the Vulgate/Douay 'She rendered')")
la = get(RF, ['S0911', 1, 'la'])
copies(la, None, None, [('C21s', 1), ('S0529b', 1), ('S0602b', 1)], s,
       "Luc. 21: 9-19 as printed pp. 13*-14*: 'terréri : Opórtet', 'meum : Contínget', 'vobis : Et éritis', 'meum : Et capíllus' (capitals after the colon, seen on the scan; = S0911)", '')
