#!/bin/bash
# Push ONLY the named files while many agents keep editing the main working tree.
# usage: tools/push_files.sh MSGFILE file1 file2 ...
# Builds a clean worktree from origin/main, copies the files in, serves it on :8769, runs mass_sweep there,
# bumps sw.js, commits as UltraPheonix, pushes; then moves the main repo's HEAD/index to origin/main
# without touching anyone's working files.
set -e
cd "$(dirname "$0")/.."; R=$(pwd); MSGF="$1"; shift
WT=/tmp/pushwt
git fetch -q origin
git worktree remove --force $WT 2>/dev/null || true; rm -rf $WT; git worktree prune
git worktree add -q --detach $WT origin/main
for f in "$@"; do mkdir -p "$WT/$(dirname "$f")"; cp -p "$R/$f" "$WT/$f"; done
cp "$R/tools/check/mass_sweep.py" $WT/tools/check/mass_sweep.py
cd $WT
( python3 -m http.server 8769 >/dev/null 2>&1 & echo $! > /tmp/pushwt.pid ); sleep 1
r=$(PORT=8769 timeout 1500 python3 tools/check/mass_sweep.py 2>&1 | tail -1)
kill $(cat /tmp/pushwt.pid) 2>/dev/null || true
echo "sweep: $r"
case "$r" in *"flagged 0"*) ;; *) echo "SWEEP FAILED - not pushed"; exit 1;; esac
git add -A -- "$@" tools/check/mass_sweep.py
for i in 1 2 3 4 5; do
  v=$(git show origin/main:sw.js | grep -o "propria-v[0-9]*" | head -1 | tr -dc 0-9); n=$((v+1))
  sed -i "s/propria-v[0-9]*/propria-v$n/" sw.js; git add sw.js
  if [ $i = 1 ]; then git -c user.name=UltraPheonix -c user.email=UltraPheonix@users.noreply.github.com commit -q -F "$MSGF"
  else git -c user.name=UltraPheonix -c user.email=UltraPheonix@users.noreply.github.com commit -q --amend --no-edit; fi
  if git -c push.negotiate=true push -q origin HEAD:main 2>/dev/null; then echo "pushed v$n"; git log --oneline -1; break; fi
  git fetch -q origin; git rebase -q origin/main || { git checkout origin/main -- sw.js; git add sw.js; GIT_EDITOR=true git rebase --continue; }
  [ $i = 5 ] && { echo FAILED; exit 1; }
done
cd $R; git worktree remove --force $WT; git fetch -q origin
git reset -q --mixed origin/main
git checkout origin/main -- sw.js tools/check/mass_sweep.py tools/push_files.sh 2>/dev/null || true
