FROM python:3.9.14

WORKDIR /usr/src/app

ENV USING_DOCKER 1

# Python related environment variables
# pyc create
ENV PYTHONDONTWRITEBYTECODE 1
# python -u: unbuffered binary stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install/Upgrade necessary packages
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pipenv

COPY ./Pipfile* ./
RUN pipenv install --system --deploy --categories="packages torch" --ignore-pipfile

# Copy source code
COPY ./ ./
RUN chmod +x init.sh

EXPOSE 8000

CMD ["bash", "init.sh"]
