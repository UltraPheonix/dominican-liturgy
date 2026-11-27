# ---- the Commons' Paschal Alleluias for S0812 (p. 30*) and S0821 (p. 37*): votive use
D=F.A.D
for k,pg,pdf in (('S0812','p. 30*','pdf 383'),('S0821','p. 37*','pdf 386')):
    RAW('data/masses.js',['masses',k,'season','pasch'],D['masses'][k]['season']['pasch'],{"al":[{"id":5685,"m39":pg},{"id":5130,"m39":pg}]},f'M39 {pg} ({pdf})',f'{pg} prints Allelúia V. Veni elécta mea; "Tempore Resurr. secundum Allelúia V. Surréxit Dóminus, et occúrrens"; "Tempore Ascens. secundum Allelúia V. Ascéndens". The site had [5526 Ascendens] only (two verses in Paschaltide, Rubr. gen. XIII.1 p. 53). Used only in votive Masses (the feast is in August)')
    FX.append({"file":"data/masses.js","op":"add","path":['masses',k,'season','asc'],"old":None,"new":{"al":[{"id":5685,"m39":pg},{"id":5526,"m39":pg}]},"src":f'M39 {pg} ({pdf})',"why":f'{pg}: "Tempore Ascens. secundum Allelúia V. Ascéndens"'})
