# ---- follow-up: capitals carry no accent in M39 ("Argue", "Angelus", "Alium"); my case fixes had added one
import json as _j
_A=_j.load(open(OUT))
for n in (25,63,65):
    e=_A[n]; new=e['new']
    for a,b in (('Árgue','Argue'),('Ángelus','Angelus'),('Ángelum','Angelum'),('Álium','Alium')): new=new.replace(a,b)
    RAW(e['file'],e['path'],e['new'],new,e['src'],'capital without accent, as printed')
