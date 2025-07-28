ENV_FILE=.env
PYTHON=poetry run
APP=app.main:app
PORT=8000

install:
	poetry install

run:
	$(PYTHON) uvicorn $(APP) --reload --port=$(PORT)

migrate:
	alembic upgrade head

# Migration
# Usage: make migration MSG='your message'
migration:
ifeq ($(MSG),)
	@echo "❌ No message provided. Use: make migration MSG='your message'"
	@exit 1
else
	alembic revision --autogenerate -m "$(MSG)"
endif

# Docker
build:
	docker build -t cross-border-payments .

docker-run:
	docker run -it --rm -p 8000:8000 --env-file .env cross-border-payments

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down