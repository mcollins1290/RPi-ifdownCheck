#!/bin/bash
cd "$(dirname "$0")";
./RPi-ifdownCheck.py > ./Log/log 2>&1
