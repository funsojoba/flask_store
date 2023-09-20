build:
	docker-compose -f docker/dev/docker-compose.yml up --build -d --remove-orphans

up:
	docker-compose -f docker/dev/docker-compose.yml up

down:
	docker-compose -f docker/dev/docker-compose.yml down

down_volumes:
	docker-compose -f docker/dev/docker-compose.yml down -v

show_logs:
	docker-compose -f docker/dev/docker-compose.yml logs

black-check:
	docker-compose -f docker/dev/docker-compose.yml exec api black --check --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

black-diff:
	docker-compose -f docker/dev/docker-compose.yml exec api black --diff --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

black:
	docker-compose -f docker/dev/docker-compose.yml exec api black --exclude=/app/venv --exclude=/app/env --exclude=venv --exclude=env .

isort-check:
	docker-compose -f docker/dev/docker-compose.yml exec api isort . --check-only --skip /app/env  --skip /app/venv

isort-diff:
	docker-compose -f docker/dev/docker-compose.yml exec api isort . --diff --skip /app/env --skip /app/venv

isort:
	docker-compose -f docker/dev/docker-compose.yml exec api isort . --skip /app/env --skip /app/venv

test:
	docker-compose -f docker/dev/docker-compose.yml exec api pytest --disable-warnings .
