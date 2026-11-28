# python3 col.py IDX L|R y0 y1 out  (y in pt, page ~ 842 high) -> crop of one column
import fitz,sys,warnings
warnings.filterwarnings('ignore')
D=fitz.open('/home/claude/dl/missal/M39.pdf')
k=int(sys.argv[1]);pg=D[k];W=pg.rect.width
x0,x1=(0,W/2+5) if sys.argv[2]=='L' else (W/2-5,W)
pg.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(x0,float(sys.argv[3]),x1,float(sys.argv[4]))).save(sys.argv[5])
print(pg.rect)
