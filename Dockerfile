FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    export PATH="/root/.local/bin:$PATH"

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app

#CMD ["poetry", "run", "python", "main.py"]
ENTRYPOINT ["poetry", "run", "python", "-m", "repo_graph.main"]
