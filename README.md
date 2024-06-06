<h1 align="center">datagusto</h1>
<div align="center">
 <strong>
   Access siloed data from one place, extract it your way without data-mapping
 </strong>

No more SQL for data mart or data migration. No dependency on architecture.
</div>

<div align="center">
  <h4>
    <a href="https://www.datagusto.ai">
      Homepage
    </a>
    |
    <a href="https://github.com/datagusto/datagusto/wiki/">
      Documentation (Wiki)
    </a>
  </h4>
</div>

## Quick Start: Local Docker Deployment

### Pre-requisites

This project assumes you have:

- `docker` and `docker-compose`
- API credentials for OpenAI API or Azure OpenAI

### Procedure

#### 1. Clone this repository

```shell
git clone https://github.com/datagusto/datagusto.git
```

#### 2. Setup environment variables

**2.1 For Backend:**

Create a `.env` file by copying `backend/.env.example` file
Then replace necessary values with your own.

##### 2.1.a Using CPU or Accelerator for Embedding and Generation

Set what processing unit to use for embedding and generation:

```
USE_GPU = "cpu"
```

If you want to use Apple Silicon GPU, set `USE_GPU = "mps"`.

In order to use Apple Silicon GPU for locally running LLM model, install following programs:

```shell
# install RUST
$ curl — proto ‘=https’ — tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Then restart your terminal.

##### 2.1.b LLM Usage

To use OpenAI APIs:

```
LLM_USAGE_TYPE = OPENAI
OPENAI_KEY = xxxxxxx
OPENAI_MODEL_NAME = xxxxxxx
```

To use Azure OpenAI:

```
LLM_USAGE_TYPE = AZURE_OPENAI
OPENAI_API_VERSION = xxxxxxx
AZURE_OPENAI_ENDPOINT = xxxxxxx
AZURE_OPENAI_API_KEY = xxxxxxx
AZURE_OPENAI_MODEL_NAME = xxxxxxx
```

To run LLM locally:

```
LLM_USAGE_TYPE = LOCAL
# HUGGING_FACE_MODEL_NAME can be model name or path to the model
#HUGGING_FACE_MODEL_NAME = ./models/gemma-1.1-2b-it | google/gemma-7b
HUGGING_FACE_ACCESS_TOKEN = xxxxxxxx
```

##### 2.1.c Additional configs

In addition, you can set the following environment variables:

- Which Vector storage to use: VECTOR_DB_USAGE_TYPE = `FAISS` | `WEAVIATE_SERVER` | `WEAVIATE_EMBEDDED`
- Which database to use (save general information including data source, column info):
  DATABASE_USAGE = `POSTGRESQL` | `SQLITE3`

**2.2 For Frontend:**

Create a `.env` file by copying `frontend/.env.example` file.
Then make sure `BACKEND_ENDPOINT` points to `backend` container.

```shell
BACKEND_ENDPOINT = http://backend:8000
```

#### 3. Setup Docker Compose Services

We have 3 docker compose files:

1. `docker-compose.yml`: main docker containers
2. `docker-compose.test.yml`: test database server

Based on your usage, please run following command to start system:

```shell
cd path/to/datagusto

# only main containers
docker compose up -d
```

This command will pull the necessary docker images and build datagusto's containers.
It will take about 5 min for the first time.

You can confirm that all containers are running up with command `docker-compose ps`.

```shell
$ docker compose ps
CONTAINER ID   IMAGE                                             COMMAND                  CREATED         STATUS                            PORTS                                              NAMES
64c058c7507e   datagusto-frontend                                "streamlit run main.…"   5 seconds ago   Up 3 seconds (health: starting)   0.0.0.0:8501->8501/tcp                             datagusto-frontend
1a42bff396b9   datagusto-backend                                 "bash init.sh"           5 seconds ago   Up 4 seconds                      0.0.0.0:8000->8000/tcp                             datagusto-backend
453705eabab3   postgres                                          "docker-entrypoint.s…"   5 seconds ago   Up 4 seconds                      0.0.0.0:5432->5432/tcp                             datagusto-postgres
114d6b227a25   cr.weaviate.io/semitechnologies/weaviate:1.24.6   "/bin/weaviate --hos…"   5 seconds ago   Up 4 seconds                      0.0.0.0:8005->8005/tcp, 0.0.0.0:50056->50051/tcp   datagusto-weaviate
```

In a few second, you should be able to access the datagusto UI at http://localhost:8501

## Documentation

For the full documentation, please see the Repo's Wiki page.

## Roadmap

TBA

## Remarks

### Running on CUDA
Because of the `pipenv` restriction ([here](https://github.com/pypa/pipenv/issues/3702)), you need to install following way:
```shell
# go to backend folder
cd backend
# delete Pipfile.lock
rm Pipfile.lock

# install with CUDA 12
pipenv install --categories="torch_cu121 packages"
# install with CUDA 11
pipenv install --categories="torch_cu118 packages"
```

### Running LLM locally

Running LLM locally generally requires a lot of resources (cpu, gpu, memory) especially for large models.
We have conducted some experiments with some popular open source LLM models:

| Model Name                         | Model size | Required memory | 1 request response time | Response value | |
|------------------------------------|------------|-----------------|-------------------------|----------------|-|
| microsoft/phi-1_5                  | 1.3b       | 8GB             | 20 sec                  | Bad            | |
| microsoft/Phi-3-mini-4k-instruct   | 3.8b       | 16GB            | 20 sec                  | Good           | |
| mistralai/Mistral-7B-v0.1          | 7b         | 30GB            | 100 sec                 | Good           | |
| openai-community/gpt2              | 124M       | 1.6GB           | 3 sec                   | Bad            | |
| mistralai/Mistral-7B-Instruct-v0.3 | 7b         | 30GB            | 31 sec                  | Good           | |
| bofenghuang/vigogne-2-7b-chat      | 7b         | 27GB            | 31 sec                  | Good           | |
| google/gemma-2b-it                 | 2b         | 12GB            | 20 sec                  | Good           | |
| google/gemma-1.1-2b-it             | 2b         | 11GB            | 10 sec                  | Good           | |

Response is validated by sending table and column information to LLM and check if it can generate meaningful
description for the column.
Please use appropriate model based on your system resources and generation accuracy.

Experiment has done on:

| Name                  | Description                                | |
|-----------------------|--------------------------------------------|-|
| Server                | Virtual Machine On Azure                   | |
| VM size               | Standard E8bds v5 (8 vcpus, 64 GiB memory) | |
| Processing archicture | only CPU                                   | |
| Operating System      | Ubuntu 20.02 LTS                           | |
| Python version        | 3.9.14                                     | |

Multilanguage test and GPU test will be conducted in the future.
- Response time was about half the size of CPU on Apple Silicon GPU for `google/gemma-2b-it` and `google/gemma-1.1-2b-it`.

### Deploy a test database to connect

If you need a database to try datagusto, we offer a test database container. In the step **3. Setup Docker Compose
Services**, run the below command instead of `docker-compose up -d`.

```shell
# run system with test servers (mysql)
docker-compose -f docker-compose.yml -f docker-compose.test.yml up -d
```

### Connecting to localhost DB server from Docker container

If you are running your test database on your laptop and want to connect
to it from a Docker container, you need to use `host.docker.internal` as
the host name.
For example, if you are running a MySQL server on your laptop and want to connect then input following information:

```text
host: host.docker.internal
port: 3306
username: root
password: password
```
