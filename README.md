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

**For Backend:**

Create a `.env` file by copying `backend/.env.example` file
Then replace necessary values with your own.

Set what processing unit to use for embedding:
```shell
USE_GPU = "cpu"
```
If you want to use GPU, set `USE_GPU = "cuda"`.

To use OpenAI APIs:
```shell
LLM_USAGE_TYPE = OPENAI
OPENAI_KEY = xxxxxxx
OPENAI_MODEL_NAME = xxxxxxx
```

To use Azure OpenAI:
```shell
LLM_USAGE_TYPE = AZURE_OPENAI
OPENAI_API_VERSION = xxxxxxx
AZURE_OPENAI_ENDPOINT = xxxxxxx
AZURE_OPENAI_API_KEY = xxxxxxx
AZURE_OPENAI_MODEL_NAME = xxxxxxx
```

In addition, you can set the following environment variables:
- Which Vector storage to use: VECTOR_DB_USAGE_TYPE = `FAISS` | `WEAVIATE_SERVER` | `WEAVIATE_EMBEDDED`
- Which database to use (save general information including data source, column info): DATABASE_USAGE = `POSTGRESQL` | `SQLITE3`

**For Frontend:**

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
### Deploy a test database to connect
If you need a database to try datagusto, we offer a test database container. In the step **3. Setup Docker Compose Services**, run the below command instead of `docker-compose up -d`.

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
