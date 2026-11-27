# ---- S0731 St Ignatius pp. 510-511 (pdf 294)
P('S0731','r0',[0],'M39 p. 510 (pdf 294)',why='capital as printed (": Sed verbum Dei")')
import json as _j
_fx=[e for e in _j.load(open(OUT)) if e['path']==['S0719',1,'la']][-1]['new']
RAW('data/readings33.js',['S0731',1,'la'],F.A.RD['S0731'][1]['la'],_fx,'M39 pp. 510-511 (pdf 294)','two words were missing ("Designávit Dóminus et álios"; "et locum, quo erat"), plus 8 punctuation/capitals as printed; the text is now identical to the same Gospel as fixed for S0719 (p. 499)')
