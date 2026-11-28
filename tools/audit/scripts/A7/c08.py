from clus import *
s9 = 'M39 p. 9* (pdf 372-373), Comm. unius Mart. non Pont.'
w8 = "Commune copy (Eccli. 14-15, p. 9*): 'potábit illum : Et firmábitur' (capital after the colon, seen on the scan)"
for k in ('S0122', 'S0115'): canon_entry(k, 0, [('illum: et firmábitur', 'illum: Et firmábitur')], s9, w8)
w9 = "Commune copy (Joan. 12: 24-26, p. 9*): 'perdet eam : Et qui odit', 'me sequátur : Et ubi sum' (capitals after the colon, seen on the scan)"
for k in ('S0122', 'S0115'): canon_entry(k, 1, [('eam: et qui odit', 'eam: Et qui odit'), ('sequátur: et ubi', 'sequátur: Et ubi')], s9, w9)
canon_entry('S0201', 1, [('eam: et qui odit', 'eam: Et qui odit'), ('sequátur: et ubi', 'sequátur: Et ubi')], 'M39 p. 371 (pdf 224)',
            "own print p. 371: 'perdet eam : Et qui odit', 'me sequátur : Et ubi sum' (seen on the scan; as the Commune p. 9*)")
