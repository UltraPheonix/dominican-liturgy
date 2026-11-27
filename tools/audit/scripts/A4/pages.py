import re
L=open('/home/claude/dominican-liturgy/tools/orat39/m39lin.txt',encoding='utf8').read().split('\n')
# blocks: each @@PAGE marker starts a block (half pdf page)
blocks=[]
for i,l in enumerate(L):
    m=re.match(r'@@PAGE (\d+)',l)
    if m: blocks.append([int(m.group(1)),i,None])
for b in blocks:
    i=b[1]
    for l in L[i+1:i+4]:
        m=re.match(r'^\s*(\d{1,3}\*?)\s*$',l.strip()) or re.match(r'^(\d{1,3}\*?)\s',l.strip())
        if m: b[2]=m.group(1); break
        m=re.search(r'\s(\d{1,3}\*?)\s*$',l.strip())
        if m: b[2]=m.group(1); break
