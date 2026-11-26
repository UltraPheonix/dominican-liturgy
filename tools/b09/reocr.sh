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
# The result is kept in tools/b09/ocr/v1.txt.gz, v2.txt.gz ('\f### <pdf page>\n<text>' per page). To restore /tmp/b09/ocr from them:
#   python3 -c "import gzip,sys;[open('/tmp/b09/ocr/%s-%s.txt'%(v,p[:4]),'w').write(p[5:]) for v in ('v1','v2') for p in gzip.open('tools/b09/ocr/%s.txt.gz'%v,'rt').read().split('\f### ')[1:]]"
