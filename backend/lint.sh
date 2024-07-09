#!/bin/bash

lint_files=(
"./core/"
"./database/"
"./endpoints/"
"./schemas/"
"./services/"
"./dependencies.py"
"./main.py"
)

# isort --check-only genai_core/
pipenv run isort ${lint_files[@]}

#ruff format
pipenv run ruff format ${lint_files[@]}

# ruff check
pipenv run ruff check ${lint_files[@]} --fix
