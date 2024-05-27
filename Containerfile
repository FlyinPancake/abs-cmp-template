ARG PYTHON_VERSION=3.12
ARG PORT=8842

# create requirements.txt
FROM python:${PYTHON_VERSION}-bookworm as builder

WORKDIR /app

## install pipx and poetry
RUN pip install pipx
RUN pipx install poetry
RUN pipx inject poetry poetry-plugin-export
ENV PATH="${PATH}:/root/.local/bin"

COPY pyproject.toml poetry.lock ./
RUN poetry export --format requirements.txt --output requirements.txt

FROM python:${PYTHON_VERSION}-slim as base
COPY custom_metadata_provider /app
COPY --from=builder /app/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["fastapi", "run" ]

