FROM python:3.9.14

WORKDIR /usr/src/app

# Install/Upgrade necessary packages
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install pipenv

COPY ./Pipfile* ./
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./ ./

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
