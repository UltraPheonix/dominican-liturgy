cd /tmp/A5 && python3 -c "
import sys; sys.path.insert(0,'/tmp/A5')
import fixes_src
from fx import save; save()" && cd /home/claude/dominican-liturgy && python3 tools/audit/apply_fixes.py --dry
