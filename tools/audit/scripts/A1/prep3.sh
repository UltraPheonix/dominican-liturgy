#!/bin/bash
cd /tmp/A1
for k in "$@"; do
echo "################ $k"
python3 -W ignore show.py $k | head -1 | cut -c1-300
python3 -W ignore review.py $k
python3 -W ignore rvc.py $k
grep "^## \|TAIL\|NOT FOUND\|  W " diff/$k.txt | cut -c1-260
done
