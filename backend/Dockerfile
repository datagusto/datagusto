FROM python:3.9.14

WORKDIR /usr/src/app

ENV USING_DOCKER 1

# Python related environment variables
# pyc create
ENV PYTHONDONTWRITEBYTECODE 1
# python -u: unbuffered binary stdout and stderr
ENV PYTHONUNBUFFERED 1

ENV SQLALCHEMY_DATABASE_URI postgresql://user:password@postgres:5432/postgres

# Install/Upgrade necessary packages
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pipenv

COPY ./Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile

# Copy source code
COPY ./ ./

EXPOSE 8000

RUN alembic upgrade head

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging.yaml", "--timeout-keep-alive", "3600"]
