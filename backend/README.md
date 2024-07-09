

## Backend Development related


### Prerequisites
This project assumes you have installed `pipenv` and `python3.10`.


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

### Database migration

```shell
# if necessary, enable pipenv environment to make easy to run alembic cli
pipenv shell

# create a new migration
pipenv run alembic revision --autogenerate -m "generation version message"
# apply the migration
pipenv run alembic upgrade head
```

### Generate Pipfile.lock

Start docker container, then run the following command.

```shell
# delete Pipfile.lock
rm Pipfile.lock

# generate Pipfile.lock
pipenv install --categories="packages torch dev-packages"
```
