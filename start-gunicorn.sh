#!/usr/bin/env bash
source pypyenv/bin/activate
gunicorn --access-logfile - --error-logfile - -k uvicorn.workers.UvicornH11Worker main:app --reload --timeout 600
