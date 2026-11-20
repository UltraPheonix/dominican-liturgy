import pymupdf, sys, re
d = pymupdf.open('/mnt/user-data/uploads/M33.pdf')
def page_text(i):
    p = d[i]; W = p.rect.width
    bl = [b for b in p.get_text('blocks') if b[6] == 0 and b[4].strip()]
    mid = W / 2
    L = sorted([b for b in bl if (b[0] + b[2]) / 2 < mid], key=lambda b: b[1])
    R = sorted([b for b in bl if (b[0] + b[2]) / 2 >= mid], key=lambda b: b[1])
    # header: blocks spanning both columns at top
    return '\n'.join(b[4].strip() for b in L) + '\n||COL||\n' + '\n'.join(b[4].strip() for b in R)
if __name__ == '__main__':
    for i in map(int, sys.argv[1:]): print('===== PAGE', i); print(page_text(i))
