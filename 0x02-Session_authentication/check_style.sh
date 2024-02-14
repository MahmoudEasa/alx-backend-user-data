#!/usr/bin/env bash

PATHS=(
    "api/v1/app.py"
    "api/v1/views/users.py"
    "api/v1/auth/session_auth.py"
)

pycodestyle "${PATHS[@]}"