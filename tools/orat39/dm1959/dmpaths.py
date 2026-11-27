# paths for the St Dominic Missal (1959) pipeline; big intermediates go in work/ (not committed)
import os
D = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(D, '..', '..', '..'))
WORK = os.environ.get('DMV_WORK', os.path.join(D, 'work'))
PDF = os.environ.get('DM_PDF', '/tmp/en_sources/dl/musicasacra/dm.pdf')   # https://media.musicasacra.com/dominican/dm.pdf
os.makedirs(WORK, exist_ok=True)
def W_(name): return os.path.join(WORK, name)
