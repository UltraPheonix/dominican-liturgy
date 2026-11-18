import re,sys
s=sys.stdin.read()
s=re.sub(r'(?<=[:.?;,] )J (?=[A-ZÁÉÍÓÚ])','✠ ',s)
s=re.sub(r'(?<=[a-zé]) ✠ ',' : ✠ ',s)
s=s.replace(' S. ',' S ')
print(s,end='')
