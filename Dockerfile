FROM python:3.10-slim as builder

RUN pip install poetry
RUN mkdir -p /app

COPY pyproject.toml /app
COPY poetry.lock /app
COPY bot_main.py /app
COPY main_api.py /app
COPY create_db.py /app
COPY config.py /app
COPY .env /app
COPY ./src /app/src

WORKDIR /app
RUN poetry config virtualenvs.in-project true
RUN poetry install

FROM python:3.10-slim as base

COPY --from=builder /app /app

WORKDIR /app

ENTRYPOINT [".venv/bin/python"]