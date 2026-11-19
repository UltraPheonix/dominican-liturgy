import pymupdf, numpy as np, sys
from PIL import Image
d=pymupdf.open('/home/claude/dl/tri/tri.pdf')
def deskew(im):
    best=None
    for ang in np.arange(-1.0,1.01,0.1):
        r=np.array(im.rotate(ang,resample=Image.BICUBIC,fillcolor=255)).astype(float)
        row=(r[:, 400:1300]<140).mean(1); sc=(row**2).sum()
        if best is None or sc>best[0]: best=(sc,ang)
    return im.rotate(best[1],resample=Image.BICUBIC,fillcolor=255)
for idx in map(int, sys.argv[1:]):
    pix=d[idx].get_pixmap(dpi=300); a=np.frombuffer(pix.samples,np.uint8).reshape(pix.h,pix.w,pix.n)[:,:,:3].mean(2).astype(np.uint8)
    W=a.shape[1]
    for side,arr in ((0,a[:, :W//2]),(1,a[:, W//2:])):
        deskew(Image.fromarray(arr)).save('/tmp/rt/page%d.png'%(idx*100+side))
