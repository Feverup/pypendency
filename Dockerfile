ARG PYTHON_VERSION=3.8.16
FROM python:$PYTHON_VERSION

ENV PYTHONPATH /app/src:/app/tests
ENV PATH /root/.local/bin/:$PYENV_ROOT/bin/:$PATH

WORKDIR /app/
COPY . /app/

RUN apt-get update \
      && apt-get install -y --no-install-recommends curl \
      && rm -rf /var/lib/apt/lists/* \
      && pip install --upgrade pip \
      && adduser -u 1000 --gecos "" --disabled-password fever \
      && chown -R fever:fever /app
RUN pip install pipenv
RUN pipenv install --dev --system

CMD ["python"]
