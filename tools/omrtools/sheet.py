import fitz,sys,warnings; warnings.filterwarnings('ignore')
from PIL import Image
d=fitz.open(sys.argv[1]); dpi=int(sys.argv[3]) if len(sys.argv)>3 else 40; n=len(d)
ims=[Image.frombytes('RGB',(p.width,p.height),p.samples) for p in (d[i].get_pixmap(dpi=dpi) for i in range(n))]
w,h=ims[0].size; cols=min(6,n)
S=Image.new('RGB',(w*cols+10*cols,(h+10)*((n+cols-1)//cols)),'gray')
for i,im in enumerate(ims): S.paste(im,((i%cols)*(w+10),(i//cols)*(h+10)))
S.save(sys.argv[2]); print(n,'pages')
