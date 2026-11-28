# zoom.py IDX [IDX2] : 400 dpi crop of stream words IDX..IDX2
import fitz,json,sys,warnings; warnings.filterwarnings('ignore')
S=json.load(open('/tmp/A1/stream.json')); a=int(sys.argv[1]); b=int(sys.argv[2]) if len(sys.argv)>2 else a
ws=S[a:b+1]; D=fitz.open('/home/claude/dl/missal/M39.pdf'); pg=D[ws[0][0]]
pg.get_pixmap(dpi=int(sys.argv[3]) if len(sys.argv)>3 else 400,clip=fitz.Rect(min(w[1] for w in ws)-5,min(w[2] for w in ws)-8,max(w[3] for w in ws)+5,max(w[4] for w in ws)+4)).save('/tmp/A1/s4/z.png'); print('/tmp/A1/s4/z.png')
