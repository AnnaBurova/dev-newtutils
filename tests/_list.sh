#!/usr/bin/env bash
set +e  # continue on error

# > — Creates (or overwrites) the output.txt file.
# >> — Appends output to the end of an existing file.

# $ cd dev-newtutils/tests/
# $ ./_list.sh

cd "$(dirname "$0")" || exit 1

IS_LINUX=false
[[ "$OSTYPE" == "linux"* ]] && IS_LINUX=true
IS_WSL=false
[[ -d "/mnt/c" ]] && IS_WSL=true

# === List of test modules ===
# modules=("console")
# modules=("utility")
# modules=("files")
# modules=("sql")
# modules=("network")
modules=("console" "utility" "files" "sql" "network")

# === List of virtual environments ===
if $IS_LINUX || $IS_WSL; then
  env_venv=("venvLinux312")
else
  env_venv=("venv314" "venv313" "venv312" "venv311" "venv310")
fi

# === Loop each env_venv ===
for venv in "${env_venv[@]}"; do
  if [[ "$venv" == *"Linux"* ]]; then
    PYTEST="/mnt/d/VS_Code/.${venv}/bin/pytest"
  else
    PYTEST="D:/VS_Code/.${venv}/Scripts/pytest"
  fi

  if [ ! -f "$PYTEST" ]; then
    echo "⚠️  Skipping $venv = pytest not found"
    continue
  fi

  # === Loop each module ===
  for mod in "${modules[@]}"; do
    echo "Running tests for: $mod in $venv"

    base_path="test_${mod}.py"

      echo "-----------------------------------------"
      for n in 1 2 3 4; do
          echo "tests/test_${mod} $n $venv"
          case $n in
            1)
              "$PYTEST" "$base_path" > "output/${venv}_test_${mod}_${n}.txt" 2>&1
              ;;
            2)
              "$PYTEST" "$base_path" -v > "output/${venv}_test_${mod}_${n}.txt" 2>&1
              ;;
            3)
              "$PYTEST" "$base_path" -s > "output/${venv}_test_${mod}_${n}.txt" 2>&1
              ;;
            4)
              "$PYTEST" "$base_path" -s -v > "output/${venv}_test_${mod}_${n}.txt" 2>&1
              ;;
          esac

          # Convert to LF
          if [[ "$venv" != *"Linux"* ]]; then
            dos2unix --force "output/${venv}_test_${mod}_${n}.txt"
          fi
      done
      echo "-----------------------------------------"
  done
done

echo "✅ Done. Check output files (UTF-8 + LF)."
