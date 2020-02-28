#!/bin/bash
cd "$(dirname "$0")";

LOGFILENAME=./Log/log_$(date +%FT%T)

./RPi-ifdownCheck.py > "$LOGFILENAME" 2>&1
