# Error check against the St. Dominic Missal (1959)

Every Mass was compared with the Missal. Where its entry is clearly one Mass, the site follows it (38 chants were corrected this way).
The differences below are places where the Missal text could not be read as a single Mass (two Masses printed together, or a page the OCR muddled). Check each against the book and correct it in `tools/build_masses.py` if needed.

## Saints

| Mass | Part | On the site | In the Missal (as read) |
|---|---|---|---|
| 6 Dec. — S. Nicolai, E. C. | gr | Juravit Dominus | Ecce sacerdos. V. Non es |
| 6 Dec. — S. Nicolai, E. C. | co | Semel juravi | Beatus servus |
| 6 Dec. — S. Nicolai, E. C. | al | Inveni David | Justus germinabit |
| Missa «Invocabit Dominum» (c. 6 Maii) | al | Fortitudo mea | Hic est discipulus |
| Nativity of John the Baptist | al | Inter natos | Isti sunt duae olivae, In multitudine |
| Nativity of John the Baptist | co | Tu puer | Etsi coram, Videte quoniam |
| Seven Holy Martyrs | al | Isti sunt qui venerunt | Laudate pueri |
| Missa «Adeamus (ps. Erucvtavit)» (c. 8 Sept.) | gr | Exsultabit cor meum | Propter veritatem |
| Missa «Adeamus (ps. Erucvtavit)» (c. 8 Sept.) | of | Exsultavit spiritus meus | Felix namque es |
| Missa «Gaudeamus... assumptione» (c. 12 Sept.) | of | Felix namque es | Ave Maria, Protege Domine |
| Missa «Gaudeamus... assumptione» (c. 12 Sept.) | al | Nativitas gloriosae Virg | Dulce lignum |
| St. Januarius and Co | gr | Exsultabunt sancti | Gloriosus |
| St. Januarius and Co | al | Te Martyrum | Sancti tui |
| St. Januarius and Co | co | Posuerunt | Dico autem...qui vos per |
| St. Therese of the Child | gr | Justus ut palma | Quasi stella... quasi so |
| 19 Ian. — B. Andreæ a Piscaria O.P. C. | gr | Justus ut palma | Unam petii... Beati |
| 19 Ian. — B. Andreæ a Piscaria O.P. C. | al | Justus germinabit | Omnia detrimentum |
| 19 Ian. — B. Andreæ a Piscaria O.P. C. | co | Beatus servus | Simile est |
| St. John of Cologne and Co., | Gospel | Lucas 21: 9-19 | Lucas 6 |

## Proper of the Time

```
Dec25_2 Christmas, Mass at dawn 
   gr: ours ['Benedictus qui venit'] / Missal ['Viderunt omnes']
Nat1 Sunday within the octave of Christmas 
   al: ours ['Multifarie'] / Missal ['Dies sanctificatus']
Epi2 2nd Sunday after Epiphany 
   al: ours ['Laudate Deum omnes (Al'] / Missal ['Laudate Dominum']
5af Friday after Ash Wednesday 
   gr: ours ['Unam petii... Ut... pr'] / Missal ['Unam petii... Beati']
Quad4t Tuesday in the 4th week of Lent 
   gr: ours ['Exsurge... fer opem'] / Missal ['Exsurge... non praeval']
Quad6h Maundy Thursday 
   gr: ours ['Christus factus est'] / Missal ['Ego autem dum mihi']
   co: ours ['Dominus Jesus'] / Missal ['Adversum me']
Pasc0m Easter Monday 
   gr: ours ['Haec dies... Dicat nun'] / Missal ['Haec dies... Confitemi']
Pasc0w Easter Wednesday 
   in: ours ['Venite benedicti'] / Missal ['Aqua sapientiae', 'Venite benedicti']
   gr: ours ['Haec dies... Dextera'] / Missal ['Haec dies... Confitemi']
   al: ours ['Christus resurgens'] / Missal ['Surrexit Dominus et', 'Christus resurgens']
   co: ours ['Christus resurgens'] / Missal ['Si consurrexistis', 'Christus resurgens']
Pasc0h Easter Thursday 
   gr: ours ['Haec dies... Lapidem'] / Missal ['Haec dies... Confitemi']
CorpusChristi Corpus Christi 
   gr: ours ['Oculi omnium'] / Missal ['Benedictus es']
   al: ours ['Caro mea vere'] / Missal ['Benedictus es', 'Caro mea vere']
   of: ours ['Sacerdotes Domini'] / Missal ['Benedictus sit']
   co: ours ['Quotiescumque'] / Missal ['Benedicimus Deum', 'Quotiescumque']
SCJ Most Sacred Heart of Jesus 
   co: ours ['Unus militum'] / Missal ['Unus militum', 'Si quis sitit']
Temporale paired with the Missal: 68 of 125 ; with differences: 11
```
