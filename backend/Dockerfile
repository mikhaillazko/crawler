FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    LANG=C.UTF-8
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy
COPY . .
CMD ["uvicorn", "optifino.asgi:app", "--host", "0.0.0.0", "--port", "${PORT}"]
