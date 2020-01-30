#!/bin/bash
cd "$(dirname "$0")";

CURRLOG=./Log/current-log
PREVLOG=./Log/previous-log

if [ -f "$CURRLOG" ]; then
	mv -f "$CURRLOG" "$PREVLOG"
fi

./RPi-ifdownCheck.py > "$CURRLOG" 2>&1
