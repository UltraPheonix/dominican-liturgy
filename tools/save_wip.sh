#!/bin/bash
# Snapshot EVERYTHING in the working tree (tracked + new files, respecting .gitignore) onto the branch
# wip-swarm on GitHub, without touching main, the index or anyone's files. Safe to run any time.
cd "$(dirname "$0")/.."
export GIT_INDEX_FILE=/tmp/wip.index; rm -f $GIT_INDEX_FILE
git read-tree HEAD && git add -A . 2>/dev/null
T=$(git write-tree)
P=$(git rev-parse -q --verify origin/wip-swarm || git rev-parse HEAD)
C=$(echo "WIP snapshot of the agent swarm $(date -u +%FT%TZ) (not live; main is untouched)" | git -c user.name=UltraPheonix -c user.email=UltraPheonix@users.noreply.github.com commit-tree $T -p $P -p HEAD)
git -c push.negotiate=true push -q origin $C:refs/heads/wip-swarm && echo "saved wip-swarm $C"
