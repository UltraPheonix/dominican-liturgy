#!/bin/bash
# usage: push.sh "commit message"
set -e
S=/home/claude/build/site; R=/home/claude/dominican-liturgy; B=/home/claude/build
cp -r "$S"/. "$R"/ && rm -f "$R"/ordo_test.json "$R"/data/office.js "$R"/tools/build_office.py
mkdir -p $R/tools/office && cp $B/do/*.py $B/do/*.sh $R/tools/office/ 2>/dev/null || true
cp $B/build_masses.py $B/complete.py $B/dm_merge.py $B/douay_match.py $B/resolve_m39.py $B/check.js $B/m39_*.py $B/douay_all.py $R/tools/ 2>/dev/null || true
cp $B/m39_fixes.json $B/manual_trans.json $B/own_trans.json $B/douay_all.json $R/tools/ 2>/dev/null || true
cd $R; git add -A
git -c user.name="UltraPheonix" -c user.email="UltraPheonix@users.noreply.github.com" commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Rbf49bkf9too7pRh1sfmcN"
git -c user.name="UltraPheonix" -c user.email="UltraPheonix@users.noreply.github.com" pull --rebase -q origin main 2>&1 | tail -2; git push -q origin main 2>&1 | tail -2; git status -sb | head -1; git log --oneline -1
