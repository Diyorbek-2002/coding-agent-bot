#!/usr/bin/env bash
# Python fayl saqlanganda sintaksisni tekshiradi

FILE="$1"

if [[ "$FILE" == *.py ]]; then
  echo "[hook] Checking syntax: $FILE"
  if python -m py_compile "$FILE" 2>&1; then
    echo "[hook] OK: $FILE syntax is valid"
  else
    echo "[hook] ERROR: syntax error in $FILE — fix before running"
    exit 1
  fi
fi
