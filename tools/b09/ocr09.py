# ocr09.py vol first last : OCR the 1909 Breviary page by page (Latin, automatic column layout) into /tmp/b09/c/<vol>_<idx>.txt
import fitz, subprocess, sys, os
vol=sys.argv[1]; d=fitz.open('/tmp/b09/%s.pdf'%vol)
for i in range(int(sys.argv[2]),min(int(sys.argv[3]),len(d))):
    base='/tmp/b09/c/%s_%04d'%(vol,i)
    if os.path.exists(base+'.txt'): continue
    d[i].get_pixmap(dpi=250).save(base+'.png')
    r=subprocess.run(['tesseract',base+'.png','-','-l','latf','--psm','3'],capture_output=True,text=True,env=dict(os.environ,OMP_THREAD_LIMIT='1'))
    open(base+'.txt','w').write(r.stdout); os.remove(base+'.png')
