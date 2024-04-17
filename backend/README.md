

## Run backend


### Prerequisites
This project assumes you have installed `pipenv` and `python3.9`.


### Install dependencies

```shell
# go to under datagusto/backend directory
cd datagusto/backend

# install dependencies
pipenv install

# migrate database
pipenv run alembic upgrade head

```

### Run the server

```shell
# go to under datagusto/backend directory
cd datagusto/backend

# run the server
pipenv run uvicorn main:app --reload --log-config logging.yaml --timeout-keep-alive 3600
```

## Development related

### Database migration

```shell
# if necessary, enable pipenv environment to make easy to run alembic cli
pipenv shell

# create a new migration
pipenv run alembic revision --autogenerate -m "generation version message"
# apply the migration
pipenv run alembic upgrade head
```

### Deploy on Ubuntu
General `sentence-transformers` package requires CUDA installed.
If we want to not to use GPU version of `sentence-transformers`, we need
to install `torch` CPU version by adding following line to `backend/Pipfile` file
before running `pipenv install` command.

```shell
$ cat backend/Pipfile
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
install = "*"
fastapi = "*"
uvicorn = "*"
sqlalchemy = "*"
alembic = "*"
pyyaml = "*"
torch = {version = "==2.2.2", file = "https://download.pytorch.org/whl/cpu/torch-2.2.2%2Bcpu-cp310-cp310-linux_x86_64.whl#sha256=02c4fac3c964e73f5f49003e0060c697f73b67c10cc23f51c592facb29e1bd53"}
mysql-connector-python = "*"
langchain = "*"
sentence-transformers = "*"
weaviate-client = "*"
langchain-openai = "*"
pydantic-settings = "*"


[dev-packages]

[requires]
python_version = "3.10"
```
