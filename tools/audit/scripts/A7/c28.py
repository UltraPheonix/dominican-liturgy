from clus import *
s = 'M39 pp. 23*-24* (pdf 379-380), Comm. Conf. non Pont. alia Missa (Os justi)'
la = canon_entry('C42s', 0, [('ætérna: qui pótuit', 'ætérna: Qui pótuit'), ('fecit: ideo', 'fecit: Ideo'), ('omnis ecclésia', 'omnis Ecclésia')], s,
                 "as printed: 'glória ætérna : Qui pótuit', 'non fecit : Ideo stabilíta', 'omnis Ecclésia sanctórum' (seen on the scan; CHECK.md Part 3 notes)")
L = 'S0208 S0214 S0308 S0119b S0124b S0216b S0219b S0225b S0301b S0322b S0514b S0517b S0612b S0724b S0728b S0818b S0819b S0923b S0926b S0928b S1010b S1011b S1021b S1026b S1103b S1114b S1216b S0217b S0304 S0320b S0717b S0730b S0906b_2 S0428b S1201b'.split()
copies(la, None, None, [(k, 0) for k in L], s, "Commune copy (Eccli. 31: 8-11, p. 23*): 'ætérna : Qui pótuit', 'fecit : Ideo', 'omnis Ecclésia' (seen on the scan)", '')
canon_entry('S0605b', 0, [('ætérna: qui pótuit', 'ætérna: Qui pótuit'), ('fecit: ideo', 'fecit: Ideo'), ('omnis ecclésia', 'omnis Ecclésia')], 'M39 pp. 460-461 (pdf 269)',
            "own print of the Os justi Mass (p. 460-461): 'ætérna : Qui pótuit', 'fecit : Ideo', 'omnis Ecclésia' (seen on the scan; 'pecúnia, et' as printed there)")
la = canon_entry('C42s', 1, [('vigilántes: amen dico', 'vigilántes: Amen dico')], s, "'invénerit vigilántes : Amen dico vobis' as printed (seen on the scan)")
G = 'S0208 S0214 S0124b S0216b S0219b S0301b S0322b S0514b S0517b S0612b S0724b S0728b S0818b S0819b S0923b S0926b S0928b S1010b S1011b S1021b S1026b S1114b S1216b S0217b S0304 S0320b S0730b S0906b_2 S1201b'.split()
copies(la, None, None, [(k, 1) for k in G], s, "Commune copy (Luc. 12: 35-40, p. 24*): 'vigilántes : Amen dico' (seen on the scan; CHECK.md #98-#100)", '')
for k, p in (('S0117', 'M39 p. 355 (pdf 217)'), ('S1231', 'M39 p. 349 (pdf 213)'), ('S0605b', 'M39 p. 461 (pdf 269)')):
    canon_entry(k, 1, [('vigilántes: amen dico', 'vigilántes: Amen dico')], p, "own print: 'invénerit vigilántes : Amen dico vobis' (seen on the scan)")
