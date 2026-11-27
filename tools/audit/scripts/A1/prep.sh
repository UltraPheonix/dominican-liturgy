#!/bin/bash
cd /tmp/A1
for k in "$@"; do
echo "################ $k"
python3 -W ignore show.py $k | head -1 | cut -c1-200
python3 -W ignore review.py $k
python3 -W ignore case.py $k | sed 's/^/C /'
python3 -W ignore concl.py $k
grep "^## ch\|^## or\|^## rd\|TAIL\|NOT FOUND" diff/$k.txt | cut -c1-200
grep "^$k rd" headtail.txt | sed 's/||.*//' | cut -c1-220
done
