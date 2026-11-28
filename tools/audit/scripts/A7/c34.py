from clus import *; from fx import get
RR = [('sǽculi: exíbunt ángeli', 'sǽculi: Exíbunt Angeli'), ('ignis: ibi erit', 'ignis: Ibi erit')]
w = "as printed: 'sǽculi : Exíbunt Angeli', 'ignis : Ibi erit fletus, et stridor' (seen on the scan)"
canon_entry('C45s', 1, RR, 'M39 p. 27* (pdf 381)', w)
canon_entry('C55s', 1, RR, 'M39 p. 33* (pdf 384)', w)
for k, p in (('S1202', 'M39 p. 326 (pdf 201)'), ('S1213', 'M39 p. 337 (pdf 207)')):
    canon_entry(k, 1, RR, p, 'own print: ' + w)
canon_entry('S0118', 1, [('exíbunt ángeli', 'exíbunt Angeli')], 'M39 suppl. leaf 1943, p. [2] (pdf 360)',
            "own print on the supplement leaf: 'sǽculi: exíbunt Angeli' and 'ignis: ibi erit' (lower case there, capital Angeli; seen on the scan)")
# 38*: Gaudeamus nec Virg. nec Mart.
la = canon_entry('S0103b', 1, [('ignis: ibi erit', 'ignis: Ibi erit')], 'M39 p. 38* (pdf 387)', "Commune copy (Matth. 13: 44-52, p. 38*): 'ignis : Ibi erit fletus et stridor' (capital, no comma there; seen on the scan)")
copies(la, None, None, [('S0228b', 1), ('S0808b', 1), ('S0309', 1), ('S0726', 0), ('S0821', 0), ('S0417b', 0)], 'M39 p. 38* (pdf 387)',
       "Commune copy (Matth. 13: 44-52 of Gaudeamus nec Virg. nec Mart., p. 38*; rubric 'ut in Communi nec Virg. nec Mart., pag. 36*'): 'sagénæ missæ in mare' (not 'iri'), 'invénit', 'litus', 'sǽculi : Exíbunt Angeli', 'ignis : Ibi erit fletus et stridor' (no comma on p. 38*; seen on the scan; CHECK.md #87)", '')
