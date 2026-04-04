#!/usr/bin/env bash
# Used if you set Build Command to: bash render-build.sh
set -euo pipefail
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
