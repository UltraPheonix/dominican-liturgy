#!/bin/sh
# Rebuild data/masses.js from the sources in tools/sources.  Run from this folder: sh build.sh
set -e
cd "$(dirname "$0")"
python3 parse_calendar.py > /dev/null
python3 build_temporale.py
python3 align_sanct.py > /dev/null
python3 build_masses.py
