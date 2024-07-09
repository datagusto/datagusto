#!/bin/bash

# database migration
pipenv run alembic upgrade head

# start server
pipenv run uvicorn main:app --host 0.0.0.0 --port 8000 --log-config logging.yaml --timeout-keep-alive 3600 --workers 1
