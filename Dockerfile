ARG PYTHON_VERSION=3.8.12
FROM python:$PYTHON_VERSION-slim

ENV PYTHONPATH /app/src:/app/tests
ENV PATH /root/.local/bin:$PATH

WORKDIR /app

RUN apt-get update \
      && apt-get install -y --no-install-recommends curl \
      && rm -rf /var/lib/apt/lists/* \
      && pip install --upgrade pip \
      && adduser -u 1000 --gecos "" --disabled-password fever \
      && chown -R fever:fever /app \
      && curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.2.0 python - \
      && poetry config virtualenvs.create false

COPY . ./

RUN poetry install --no-root

ENTRYPOINT ["poetry", "run"]
