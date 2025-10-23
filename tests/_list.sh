#!/usr/bin/env bash
set -e  # exit on error

# > — Creates (or overwrites) the output.txt file.
# >> — Appends output to the end of an existing file.

cd "$(dirname "$0")" || exit 1

# run console.py and write pure UTF-8 + LF
"C:/ProgramData/anaconda3/python.exe" "d:/VS_Code/dev-newtutils/tests/console.py" > console_output.txt
# & C:/ProgramData/anaconda3/python.exe d:/VS_Code/dev-newtutils/tests/console.py | Out-File console_output.txt -Encoding utf8
echo "d:/VS_Code/dev-newtutils/tests/console_output.txt"

# run files.py and write pure UTF-8 + LF
"C:/ProgramData/anaconda3/python.exe" "d:/VS_Code/dev-newtutils/tests/files.py" > files_output.txt
# & C:/ProgramData/anaconda3/python.exe d:/VS_Code/dev-newtutils/tests/files.py | Out-File files_output.txt -Encoding utf8
echo "d:/VS_Code/dev-newtutils/tests/files_output.txt"

# run utility.py and write pure UTF-8 + LF
"C:/ProgramData/anaconda3/python.exe" "d:/VS_Code/dev-newtutils/tests/utility.py" > utility_output.txt
# & C:/ProgramData/anaconda3/python.exe d:/VS_Code/dev-newtutils/tests/utility.py | Out-File utility_output.txt -Encoding utf8
echo "d:/VS_Code/dev-newtutils/tests/utility_output.txt"

echo "✅ Done. Check if Files are saved with UTF-8 + LF"
