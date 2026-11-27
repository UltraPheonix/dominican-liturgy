import sys,re
k,p,r=sys.argv[1:4]; stop=sys.argv[4] if len(sys.argv)>4 else None
s=open('/tmp/A2/rows.py').read()
line="%r:(%r,%r),"%(k,p,r)
pat=re.compile(r"^%s:\(.*\),$"%re.escape(repr(k)),re.M)
if pat.search(s): s=pat.sub(lambda m:line,s)
else: s=s.replace("ROWS={\n","ROWS={\n"+line+"\n",1)
if stop: s=re.sub(r"^STOP=.*$",lambda m:"STOP=%r"%stop,s,flags=re.M)
open('/tmp/A2/rows.py','w').write(s)
