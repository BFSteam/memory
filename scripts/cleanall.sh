#!/bin/bash
MEM="/home/nik/Documents/test/memory"

rm -r "$MEM/tmp/"
find "$MEM" -type d -name __pycache__  -o \( -type f -name '*.py[co]' \) -print0 | 
xargs -0 rm -rf
