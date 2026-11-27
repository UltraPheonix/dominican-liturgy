import pickle, warnings
warnings.filterwarnings('ignore')
exec(open('/tmp/dmv/extract.py').read().split('for pno in map')[0])
out=[rows_of(doc[p]) for p in range(doc.page_count)]
pickle.dump(out, open('/tmp/dmv/rows.pkl','wb'))
print('ok', len(out))
