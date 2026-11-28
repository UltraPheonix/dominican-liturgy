import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from dmpaths import *
import pickle, warnings
warnings.filterwarnings('ignore')
exec(open(os.path.join(D,'extract.py')).read().split('for pno in map')[0])
out=[rows_of(doc[p]) for p in range(doc.page_count)]
pickle.dump(out, open(W_('rows.pkl'),'wb'))
print('ok', len(out))
