#!/usr/bin/env bash

# > — Creates (or overwrites) the output.txt file.
# >> — Appends output to the end of an existing file.

cd "$(dirname "$0")" || exit 1

"C:/ProgramData/anaconda3/python.exe" "d:/VS_Code/dev-newtutils/tests/console.py" > console_output.txt -Encoding utf8
# & C:/ProgramData/anaconda3/python.exe d:/VS_Code/dev-newtutils/tests/console.py > console_output.txt -Encoding utf8
