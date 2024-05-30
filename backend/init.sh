#!/bin/bash

# database migration
alembic upgrade head

# start server
uvicorn main:app --host 0.0.0.0 --port 8000 --log-config logging.yaml --timeout-keep-alive 3600 --workers 1
