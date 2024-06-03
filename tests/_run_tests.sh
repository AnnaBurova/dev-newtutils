#!/usr/bin/env bash

# SELF RUN:
# $ cd dev-newtutils/
# $ pytest ./tests/ --cov=newtutils --cov-report=html
# $ pytest ./tests/test_console.py -s -vv
# $ pytest ./tests/test_utility.py -s -vv
# $ pytest ./tests/test_files.py -s -vv
# $ pytest ./tests/test_sql.py -s -vv
# $ pytest ./tests/test_network.py -s -vv

# SCRIPT RUN:
# $ cd /mnt/d/VS_Code/dev-newtutils/tests/
# $ cd dev-newtutils/tests/
# Linux: $ chmod +x script.sh
# $ ./_run_tests.sh
# $ ./tests/_run_tests.sh

# HINTS:
# > — Creates (or overwrites) the output.txt file.
# >> — Appends output to the end of an existing file.

set +e  # continue on error

# Move to the script directory
# exit if the directory cannot be found
cd "$(dirname "$0")" || exit 1
# Location now: /d/VS_Code/dev-newtutils/tests/

# Detect Linux and WSL environments
IS_LINUX=false
[[ "$OSTYPE" == "linux"* ]] && IS_LINUX=true
IS_WSL=false
[[ -d "/mnt/c" ]] && IS_WSL=true
# -d = checks whether the path is a regular derectory
# [[ ... ]] = checks a condition like if
# && = runs the next command only if the check succeeds

# ===== List of test modules =====
modules=(
    "console"
    "utility"
    "files"
    "sql"
    "network"
)

# ===== List of virtual environments by platform =====
if [[ "$IS_LINUX" == true || "$IS_WSL" == true ]]; then
    env_venv=(
        "venvLinux312"
    )
else
    env_venv=(
        "venv310"
        "venv311"
        "venv312"
        "venv313"
        "venv314"
    )
fi

# ===== Loop through each virtual environment =====
for venv in "${env_venv[@]}"; do
    # Select the pytest executable for each virtual environment
    if [[ "$venv" == *"Linux"* ]]; then
        PYTEST="/mnt/d/VS_Code/.${venv}/bin/pytest"
        # Example: /mnt/d/VS_Code/.venvLinux312/bin/pytest
    else
        PYTEST="D:/VS_Code/.${venv}/Scripts/pytest"
        # Example: D:/VS_Code/.venv312/Scripts/pytest
    fi

    # Skip environment if pytest file is not found
    if [[ ! -f "$PYTEST" ]]; then
        echo "⚠️  Skipping $venv: pytest not found"
        continue
    fi
    # -f = checks whether the path is a regular file
    # ! = negates the condition

    # ===== Loop through each module =====
    for mod in "${modules[@]}"; do
        echo "----------------------------------------"
        echo "Running tests for: $mod in $venv"
        echo "----------------------------------------"

        base_path="test_${mod}.py"

        for n in 1 2 3 4; do
            echo "tests/test_${mod}.py: mode $n, environment $venv"

            case "$n" in
                1)
                    "$PYTEST" "$base_path" 2>&1 |
                        sed -E 's/passed in [0-9.]+s( ={10,})$/passed\1/' > "output/${venv}_test_${mod}_${n}.txt"
                    ;;
                2)
                    "$PYTEST" "$base_path" -vv 2>&1 |
                        sed -E 's/passed in [0-9.]+s( ={10,})$/passed\1/' > "output/${venv}_test_${mod}_${n}.txt"
                    ;;
                3)
                    "$PYTEST" "$base_path" -s 2>&1 |
                        sed -E 's/passed in [0-9.]+s( ={10,})$/passed\1/' > "output/${venv}_test_${mod}_${n}.txt"
                    ;;
                4)
                    "$PYTEST" "$base_path" -s -vv 2>&1 |
                        sed -E 's/passed in [0-9.]+s( ={10,})$/passed\1/' > "output/${venv}_test_${mod}_${n}.txt"
                    ;;
            esac

            # Convert the output file to LF line endings on Windows
            if [[ "$venv" != *"Linux"* ]]; then
                dos2unix --force "output/${venv}_test_${mod}_${n}.txt"
            fi
        done
    done
done
echo "----------------------------------------"

echo "✅ Done. Check output files (UTF-8 + LF)."
