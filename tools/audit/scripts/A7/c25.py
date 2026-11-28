from clus import *
s = 'M39 pp. 22*-23* (pdf 379), Comm. Conf. non Pont. (Justus ut palma)'
la = canon_entry('C39s', 0, [('Jesu: quæ', 'Jesu: Quæ'), ('illíus: configurátus', 'illíus: Configurátus'), ('mórtuis: non quod', 'mórtuis: Non quod'), ('sim: sequor', 'sim: Sequor')], s,
                 "capitals after the colon as printed: 'Christi Jesu : Quæ ex Deo', 'illíus : Configurátus', 'ex mórtuis : Non quod', 'perféctus sim : Sequor' (seen on the scan)")
copies(la, None, None, [(k, 0) for k in ('S0215', 'S1105', 'S0116b', 'S0426b', 'S0823b')], s,
       "Commune copy (Phil. 3: 7-12, p. 22*): 'Jesu : Quæ', 'illíus : Configurátus', 'mórtuis : Non quod', 'sim : Sequor' (seen on the scan; CHECK.md Part 3 #8)", '')
