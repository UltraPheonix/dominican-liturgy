import json,sys,subprocess
k=sys.argv[1]; CI=json.load(open('/tmp/A1/case_s3.json')).get(k,[])
args=[]
for n,it in enumerate(CI):
    print('C%d %s %s -> %s'%(n,it['lab'][:10],it['site'],it['missal']))
    args.append('C%d %s->%s|%d'%(n,it['site'],it['missal'],it['si']))
for c in range(0,len(args),16):
    subprocess.run(['python3','-W','ignore','/tmp/A1/crop.py','/tmp/A1/rv/%s_c%d.png'%(k,c//16)]+args[c:c+16],stdout=subprocess.DEVNULL)
print('case images:',(len(args)+15)//16)
