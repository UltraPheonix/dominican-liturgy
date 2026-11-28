from clus import *
RR = [('me: a pressúra', 'me: A pressúra'), ('æstuáta: de altitúdine', 'æstuáta: De altitúdine'), ('injústa: laudábit', 'injústa: Laudábit')]
w = "capitals after the colon as printed: 'me : A pressúra', 'æstuáta : De altitúdine', 'injústa : Laudábit' (seen on the scan)"
s = 'M39 p. 29* (pdf 382), Comm. Virg. et Mart. alia Missa (Me exspectaverunt)'
canon_entry('C48s', 0, RR, s, w)
canon_entry('S0121', 0, RR, s, 'Commune copy (Eccli. 51: 1-8, 12, p. 29*): ' + w)
canon_entry('S1125', 0, RR + [('usque ac mortem', 'usque ad mortem')], 'M39 p. 632 (pdf 355)', "own print: " + w + "; 'usque ad mortem' (typo 'ac')")
