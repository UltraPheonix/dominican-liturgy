import re,sys
s=sys.stdin.read()
s=re.sub(r'\s+[|!.]\s*(?=[a-záéíóú])',' ',s)          # lone debris tokens
s=re.sub(r'(?<=[a-záéíóúæœ])[.!?](?= [a-záéíóú])','',s)  # a stop before a lower-case word: scan noise
s=re.sub(r'\s*\|\s*',' ',s)
s=re.sub(r'(?<=\w)- (?=[a-záéíóú])','',s)
s=re.sub(r' {2,}',' ',s)
print(s,end='')
