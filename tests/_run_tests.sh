#!/usr/bin/env bash

# Author: NewtCode Anna Burova
# Created: 2024-06
# Updated: 2026-11

# Run:
# chmod +x /mnt/d/VS_Code/dev-newtutils/tests/_run_tests.sh
# /mnt/d/VS_Code/dev-newtutils/tests/_run_tests.sh

# Run selected test modules in configured virtual environments across four pytest modes.

# ===================================================================== ======= =================== ====================

set +e  # continue on error

# Directory containing virtual environments
WORKSPACE_DIRECTORY="/mnt/d/VS_Code"

ENVIRONMENTS=(
    "venvWSL314"
)

MODULES=(
    "console_stringify_value"
    # "utility"
    # "files"
    # "sql"
    # "network"
)

# --------------------------------------------------------------------- ------- ------------------- --------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1
# /mnt/d/VS_Code/dev-newtutils/tests

# Ensure output directory exists
OUTPUT_DIRECTORY="${SCRIPT_DIR}/output"
mkdir -p "$OUTPUT_DIRECTORY"

echo ""

# --------------------------------------------------------------------- ------- ------------------- --------------------

for ENVIRONMENT in "${ENVIRONMENTS[@]}"; do

    PYTEST_PATH="${WORKSPACE_DIRECTORY}/.${ENVIRONMENT}/bin/pytest"

    # Skip environment if pytest executable is not found
    if [[ ! -f "$PYTEST_PATH" ]]; then
        printf "\nSkipping %s : pytest not found\n" "$ENVIRONMENT"
        continue
    fi

    # ----------------------------------------------------------------- ------- ------------------- --------------------

    for MODULE in "${MODULES[@]}"; do

        TEST_FILE="test_${MODULE}.py"

        for MODE in 1 2 3 4; do

            echo "tests/${TEST_FILE}: mode ${MODE}, environment ${ENVIRONMENT}"

            case "$MODE" in
                1) MODE_ARGS=() ;;
                2) MODE_ARGS=("-vv") ;;
                3) MODE_ARGS=("-s") ;;
                4) MODE_ARGS=("-s" "-vv") ;;
            esac

            OUTPUT_FILE="${OUTPUT_DIRECTORY}/${ENVIRONMENT}_test_${MODULE}_${MODE}.txt"

            # Run pytest, capture stdout/stderr, and strip execution time from summary line
            "$PYTEST_PATH" "$TEST_FILE" "${MODE_ARGS[@]}" 2>&1 |
                sed -E 's/(passed|ran) in [0-9.]+s( ={10,})$/\1\2/' > "$OUTPUT_FILE"
        done
    done
done

# --------------------------------------------------------------------- ------- ------------------- --------------------

cd "$WORKSPACE_DIRECTORY" || exit 1

echo ""

# ===================================================================== ======= =================== ====================
