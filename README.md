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

To use OpenAI APIs:
```shell
LLM_USAGE_TYPE = OPENAI
OPENAI_KEY = xxxxxxx
```

To use Azure OpenAI:
```shell
LLM_USAGE_TYPE = AZURE_OPENAI
OPENAI_API_VERSION = xxxxxxx
AZURE_OPENAI_ENDPOINT = xxxxxxx
AZURE_OPENAI_API_KEY = xxxxxxx
```

**For Frontend:**
Create a `.env` file by copying `frontend/.env.example` file.
Then make sure `BACKEND_ENDPOINT` points to `backend` container.

```shell
BACKEND_ENDPOINT = http://backend:8000
```

#### 3. Setup Docker Compose Services
Run the below command to deploy the datagusto.

```shell
cd path/to/datagusto
docker-compose up -d
```

This command will pull the necessary docker images and build datagusto's containers.
It will take about 5 min for the first time.

You can confirm that all containers are running up with command `docker-compose ps`.

```shell
$ docker-compose ps
NAME                 IMAGE                COMMAND                  SERVICE             CREATED             STATUS                    PORTS
datagusto-backend    datagusto-backend    "uvicorn main:app --…"   backend             39 minutes ago      Up 39 minutes             0.0.0.0:8000->8000/tcp
datagusto-frontend   datagusto-frontend   "streamlit run main.…"   frontend            39 minutes ago      Up 39 minutes (healthy)   0.0.0.0:8501->8501/tcp
```

In a few second, you should be able to access the datagusto UI at http://localhost:8501


## Documentation
For the full documentation, please see the Repo's Wiki page.


## Roadmap
TBA


## Remarks
### Deploy a test database to connect
If you need a database to try datagusto, we offer a test database container. In the step **3. Setup Docker Compose Services**, run the below command instead of `docker-compose up -d`.

```
docker-compose -f docker-compose.yml -f docker-compose-mysql.yml up -d
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
