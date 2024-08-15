FROM nvidia/cuda:12.4.0-devel-ubuntu22.04

WORKDIR /usr/src/app

ENV USING_DOCKER 1

# Python related environment variables
# pyc create
ENV PYTHONDONTWRITEBYTECODE 1
# python -u: unbuffered binary stdout and stderr
ENV PYTHONUNBUFFERED 1

# install python3.9 and pip
RUN echo "Etc/UTC" > /etc/timezone
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install software-properties-common curl -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update && apt install python3.9 python3.9-dev python3.9-distutils -y
RUN curl https://bootstrap.pypa.io/get-pip.py --output /tmp/get-pip.py && python3.9 /tmp/get-pip.py

# install necessary packages for connecting to the databases
# mssql-tools 18
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
RUN apt update && ACCEPT_EULA=Y apt install -y mssql-tools18 && ACCEPT_EULA=Y apt install -y msodbcsql18

# Install/Upgrade necessary packages
RUN pip install --upgrade pip setuptools
RUN pip install pipenv

COPY ./Pipfile* ./
RUN pipenv install --categories="packages torch" --ignore-pipfile

# Copy source code
COPY ./ ./
RUN chmod +x init.sh

EXPOSE 8000

CMD ["bash", "init.sh"]
