FROM python:3.8.0-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y --no-install-recommends install netcat build-essential cargo libpq-dev

RUN pip install --upgrade pip
COPY ./requirements ./requirements
RUN pip install -r ./requirements/dev.txt

COPY . .

CMD ["sh", "/app/docker/entrypoint.sh"]