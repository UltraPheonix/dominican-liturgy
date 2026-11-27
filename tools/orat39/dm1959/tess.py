import fitz, sys, subprocess, os, warnings
warnings.filterwarnings('ignore')
doc=fitz.open('/tmp/en_sources/dl/musicasacra/dm.pdf')
part,n=int(sys.argv[1]),int(sys.argv[2])
NEED=[int(x) for x in open('/tmp/dmv/need.txt')]
for p in NEED:
    if p%n!=part: continue
    out=f'/tmp/dmv/tess/{p:04d}'
    if os.path.exists(out+'.tsv'): continue
    png=f'/tmp/dmv/tess/tmp{part}.png'
    doc[p].get_pixmap(dpi=300).save(png)
    subprocess.run(['tesseract',png,out,'-l','eng','--psm','6','tsv'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
