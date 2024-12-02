FROM python:3.11 AS build

WORKDIR /app

ENV PYTHONPATH=/app

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Install dependencies
COPY ./pyproject.toml /app/
COPY ./wheels /app/wheels/
RUN poetry install --no-root --no-cache --only main

COPY . .

CMD ["python", "main.py"]