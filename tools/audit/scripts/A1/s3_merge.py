import sys, json; sys.path.insert(0,'/tmp/A1')
exec(open('/tmp/A1/s3lib.py').read())
import glob,os
for f in sorted(glob.glob('/tmp/A1/s3_part*.py')): exec(open(f).read())
old=json.load(open(FN))
keep=[e for e in old if not e.get('s3')]
# no s3 entry may target a path an older entry also targets with a different "old" (chain is fine); report
json.dump(keep+ENTRIES,open(FN,'w'),ensure_ascii=False,indent=1)
print('kept',len(keep),'s3',len(ENTRIES))
