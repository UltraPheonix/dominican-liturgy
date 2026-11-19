import os, sys, numpy as np
sys.path.insert(0, '/home/claude/dominican-liturgy/tools/pdfomr')
def G(pg, side, pdf='/home/claude/dl/tri/tri.pdf'):
    fn = '/home/claude/build/gcache/%s_%d%s.npy' % (os.path.basename(pdf)[:-4], pg, side)
    if os.path.exists(fn): return np.load(fn)
    from m39app import main
    st, g = main(pdf, pg, side)
    os.makedirs(os.path.dirname(fn), exist_ok=True); np.save(fn, g.astype(np.uint8)); return g
