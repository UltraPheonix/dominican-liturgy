#!/bin/bash
# usage: run_day.sh YYYY-MM-DD  -> raw engine output for every hour
d=$1; y=${d:0:4}; m=$((10#${d:5:2})); dd=$((10#${d:8:2}))
out=/home/claude/dl/do_out/$y; mkdir -p $out
cd /home/claude/src/do/web/cgi-bin/horas
for h in Matutinum Laudes Prima Tertia Sexta Nona Vespera Completorium; do
  f=$out/$d.$h.html
  [ -s $f ] && continue
  timeout 60 perl officium.pl "date=$m-$dd-$y&version=Ordo%20Praedicatorum%20-%201962&command=pray$h&lang2=English&content=1" > $f 2>/dev/null
done
