import re,sys
for i in sys.argv[1:]:
    s=open('/home/claude/dominican-liturgy/gabc/%s.gabc'%i).read(); h,b=s.split('%%',1)
    t=re.sub(r'\([^)]*\)','',b); t=re.sub(r'<[^>]+>','',t)
    print(i,'|',' '.join(l for l in h.split('\n') if l.startswith(('name','office','book'))),'|',re.sub(r'\s+',' ',t)[:300])
