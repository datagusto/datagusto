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
#isort genai_core/embeddings.py genai_core/semantic_search.py genai_core/opensearch/query.py

#ruff format genai_core/embeddings.py genai_core/semantic_search.py genai_core/opensearch/query.py
#pipenv run ruff format ${lint_files[@]}

# ruff genai_core/ --check
#pipenv run ruff check ${lint_files[@]} --fix
