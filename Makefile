COMPOSE=docker-compose
FILE=docker-compose.yaml

build:
	$(COMPOSE) -f $(FILE) up --build -d --remove-orphans

up:
	$(COMPOSE) -f $(FILE) up

down:
	$(COMPOSE) -f $(FILE) down

down_volumes:
	$(COMPOSE) -f $(FILE) down -v

show_logs:
	$(COMPOSE) -f $(FILE) logs

black-check:
	$(COMPOSE) -f $(FILE) exec api black --check --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

black-diff:
	$(COMPOSE) -f $(FILE) exec api black --diff --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

black:
	$(COMPOSE) -f $(FILE) exec api black --exclude=migrations --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

isort-check:
	$(COMPOSE) -f $(FILE) exec api isort . --check-only --skip /app/env --skip migrations --skip /app/venv

isort-diff:
	$(COMPOSE) -f $(FILE) exec api isort . --diff --skip /app/env --skip migrations --skip /app/venv

isort:
	$(COMPOSE) -f $(FILE) exec api isort . --skip /app/env --skip migrations --skip /app/venv

