FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
    curl \
    supervisor \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry
WORKDIR /app

COPY .env .env 

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --no-root

COPY ./src ./src
COPY ./conf ./conf
COPY ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./certs ./certs

COPY /scripts/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]