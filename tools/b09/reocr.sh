#!/bin/bash
# re-OCR pdf pages $2..$3 of volume $1 with tesseract (lat, tessdata_best) at 300 dpi; resumable; one txt per page
v=$1; cd /tmp/b09/ocr
for p in $(seq $2 $3); do
  f=$(printf "%s-%04d" $v $p)
  [ -s $f.txt ] && continue
  pdftoppm -f $p -l $p -r 300 -gray -png /tmp/b09/$v.pdf $f.img 2>/dev/null
  tesseract $f.img-*.png $f -l lat --psm 1 2>/dev/null
  rm -f $f.img-*.png
done
