# addl.py LISTNAME "text"  -> append to OPEN/QUESTIONS/NOTES in rows.py (no duplicates)
import sys,re
name,txt=sys.argv[1],sys.argv[2]
s=open('/tmp/A2/rows.py').read()
d={}; exec(s,d); L=d[name]
if txt not in L: L.append(txt)
s=re.sub(r'^%s=\[.*\]$'%name,lambda m:'%s=%r'%(name,L),s,flags=re.M)
open('/tmp/A2/rows.py','w').write(s)
