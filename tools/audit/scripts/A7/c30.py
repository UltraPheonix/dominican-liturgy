from clus import *; from fx import get
s = 'M39 p. 25* (pdf 380), Aliud Evangelium Designavit'
la = get(RF, ['S0802', 1, 'la'])
copies(la, None, None, [(k, 1) for k in ('S0119b', 'S0225b', 'S0717b', 'S0428b')], s,
       "Commune copy (Luc. 10: 1-9, p. 25*; = S0802/S0719, A4): 'dómui : Et si', 'vestra : Sin autem', 'sunt : Dignus', 'vobis : Et curáte', ending 'regnum Dei.' (seen on the scan; CHECK.md #105)", '')
