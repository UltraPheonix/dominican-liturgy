#!/bin/bash
# refreeze.sh KEY LO-HI : rerun one Mass restricted to pdf pages (0-based) and merge into items_frozen/loc_all
cd /tmp/A1
A1RANGE=$2 python3 -W ignore run.py $1 >/dev/null
python3 - $1 <<'P'
import json,sys
k=sys.argv[1]
F=json.load(open('items_frozen.json')); I=json.load(open('items_%s.json'%k)); F[k]=I[k]; json.dump(F,open('items_frozen.json','w'),ensure_ascii=False,indent=0)
L=json.load(open('loc_all.json')); l=json.load(open('loc_%s.json'%k)); L[k]=l[k]; json.dump(L,open('loc_all.json','w'))
P
