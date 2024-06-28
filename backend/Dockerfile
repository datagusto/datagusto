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
RUN apt update && apt install python3.9 python3.9-distutils -y
RUN curl https://bootstrap.pypa.io/get-pip.py --output /tmp/get-pip.py && python3.9 /tmp/get-pip.py

# Install/Upgrade necessary packages
RUN pip install --upgrade pip setuptools
RUN pip install pipenv

COPY ./Pipfile* ./
RUN pipenv install --deploy --categories="packages torch" --ignore-pipfile

# Copy source code
COPY ./ ./
RUN chmod +x init.sh

EXPOSE 8000

CMD ["bash", "init.sh"]
