#!/usr/bin/env bash
# Render / CI build: run with Root Directory = backend, e.g. `bash build.sh` or `./build.sh`
set -euo pipefail

cd "$(dirname "$0")"

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
