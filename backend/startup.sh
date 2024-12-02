#!/bin/sh
cd /usr/local/app
# Set up environment
set -e

# Install necessary tools
apk add --no-cache curl

# Install Poetry
curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python
ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Disable Poetry's virtual environment creation
poetry config virtualenvs.create false

# Install dependencies
poetry install

poetry shell

# Run the application
python3 main.py