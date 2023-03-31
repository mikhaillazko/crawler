FROM python:3.8-slim as backend
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    LANG=C.UTF-8
WORKDIR /app

FROM backend as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv

FROM backend as runtime
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
CMD ["uvicorn", "optifino.asgi:app", "--host", "0.0.0.0", "--port", "${PORT}"]
