FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./

COPY . .

RUN rm -rf .venv

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "main.py"]