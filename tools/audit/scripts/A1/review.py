import json,re,sys,unicodedata,subprocess
D=json.load(open('/tmp/A1/items_frozen.json'))
def fold(x):
    x=x.replace('æ','ae').replace('œ','oe').replace('ǽ','ae').replace('Æ','ae').replace('Œ','oe'); x=unicodedata.normalize('NFD',x); x=''.join(ch for ch in x if not unicodedata.combining(ch))
    return re.sub(r'[^a-z]','',x.lower().replace('j','i').replace('v','u'))
def items(k):
    out=[]
    for it in D[k]:
        if it['lab'].startswith('ch'): continue
        if it['kind']=='W':
            if fold(it['site'])==fold(it['missal']) : continue
            if fold(it['site'])=='amen' and fold(it['missal'])=='arnen': continue
        out.append(it)
    return out
if __name__=='__main__':
    k=sys.argv[1]; its=items(k)
    args=[]
    for n,it in enumerate(its):
        if it['kind']=='P': lab='%d %s %s [%s]->[%s]'%(n,it['lab'][:8],it['word'],it['site'],it['missal'])
        else: lab='%d %s W %s -> %s'%(n,it['lab'][:8],it['site'][:25],it['missal'][:25])
        print(lab if it['kind']=='W' else lab+'   ctx: '+it['ctx'])
        if it['si']>=0: args.append('%s|%d'%(lab,it['si']))
    for c in range(0,len(args),16):
        subprocess.run(['python3','-W','ignore','/tmp/A1/crop.py','/tmp/A1/rv/%s_%d.png'%(k,c//16)]+args[c:c+16],stdout=subprocess.DEVNULL)
    print('images:',(len(args)+15)//16)
