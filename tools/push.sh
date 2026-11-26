#!/bin/bash
# Commit first (one new commit on top of origin/main). Then: fetch, rebase, set sw.js VERSION = origin's + 1 (amend), push; retry.
cd "$(dirname "$0")/.."
[ -n "$(git status --porcelain --untracked-files=no)" ] && { echo "commit first"; exit 1; }
for i in 1 2 3 4 5 6; do
  git fetch -q origin
  if ! git rebase -q origin/main 2>/dev/null; then
    git show origin/main:sw.js > sw.js; git add sw.js; GIT_EDITOR=true git rebase --continue >/dev/null 2>&1 || { echo "rebase conflict"; git status --short | head; exit 1; }
  fi
  v=$(git show origin/main:sw.js | grep -o "propria-v[0-9]*" | head -1 | tr -dc 0-9); n=$((v+1))
  sed -i "s/propria-v[0-9]*/propria-v$n/" sw.js; git add sw.js; git commit -q --amend --no-edit
  git -c push.negotiate=true push -q origin main 2>/dev/null && { echo "pushed v$n"; git log --oneline -1; exit 0; }
  sleep 5
done
echo FAILED
