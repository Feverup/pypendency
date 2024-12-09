ARG PYTHON_VERSION="3.8"

FROM python:${PYTHON_VERSION}-slim

ENV PYTHONPATH=/usr/src/app/src

WORKDIR /usr/src/app

COPY Pipfile /usr/src/app/Pipfile
COPY Pipfile.lock /usr/src/app/Pipfile.lock

RUN apt-get update && \
    apt-get install make -y && \
    pip install pipenv

RUN pipenv install --dev
