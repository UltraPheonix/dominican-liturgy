#!/bin/bash
# usage: run_day.sh YYYY-MM-DD  -> engine output for every hour, said without and with a priest
d=$1; y=${d:0:4}; m=$((10#${d:5:2})); dd=$((10#${d:8:2}))
out=${DO_OUT:-/home/claude/dl/do_out}/$y; mkdir -p $out
cd /home/claude/src/do/web/cgi-bin/horas
for h in Matutinum Laudes Prima Tertia Sexta Nona Vespera Completorium; do
  f=$out/$d.$h.html
  [ -s $f ] || timeout 60 perl officium.pl "date=$m-$dd-$y&version=Ordo%20Praedicatorum%20-%201962&command=pray$h&lang2=English&content=1" > $f 2>/dev/null
  f=$out/$d.$h.P.html
  [ -s $f ] || timeout 60 perl officium.pl "date=$m-$dd-$y&version=Ordo%20Praedicatorum%20-%201962&command=pray$h&lang2=English&content=1&priest=1" > $f 2>/dev/null
done
