#!/usr/bin/env bash

PATHS=(
    "app.py"
    "auth.py"
    "db.py"
    "main.py"
    "user.py"
)

pycodestyle "${PATHS[@]}"
