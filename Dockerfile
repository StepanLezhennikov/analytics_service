FROM python:3.12-slim as builder

LABEL authors="Stepan Lezhennikov"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc musl-dev --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --verbose

FROM python:3.12-slim

ENV PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y \
    libpq-dev gcc musl-dev --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app /app

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --verbose

COPY entrypoint.sh /entrypoint.sh
COPY kowl-config.yml /etc/kowl/config.yml

RUN chmod +x /entrypoint.sh

EXPOSE 8002