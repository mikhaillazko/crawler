FROM python:3.8-slim
RUN pip -q install --user pipenv && useradd -m optifino
ENV PIPENV_VENV_IN_PROJECT=1
WORKDIR /app
COPY Pipfile* ./
COPY . .
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "optifino.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
