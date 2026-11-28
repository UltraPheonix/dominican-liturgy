import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import os, re, unicodedata, pickle, glob
def W(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not unicodedata.combining(c))
    s=s.replace('æ','ae').replace('œ','oe').replace('Æ','ae').replace('Œ','oe').lower()
    s=re.sub(r'[^a-z]','',s).replace('j','i').replace('v','u').replace('y','i')
    return s.replace('ae','e').replace('oe','e')
R=REPO
files=glob.glob(R+'/bible/la/*')+glob.glob(R+'/data/*.js')+glob.glob(R+'/data/office/**/*.json',recursive=True)+glob.glob(R+'/data/office1909/**/*.json',recursive=True)
from collections import Counter
C=Counter()
for f in files:
    try: t=open(f,encoding='utf8',errors='ignore').read()
    except IsADirectoryError: continue
    for w in re.findall(r'[^\W\d_]+',t): C[W(w)]+=1
print(len(files),len(C))
pickle.dump(C,open(W_('lex.pkl'),'wb'))
