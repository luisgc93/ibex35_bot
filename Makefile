PROJECT_ROOT_FOLDER := $(shell pwd)
DOCKER_COMPOSE_FILE := $(PROJECT_ROOT_FOLDER)/docker/docker-compose.yml

install-requirements: ## Install project requirements
	pip install -r requirements.txt

## You'll need a command to spin create and run the image and also run migrations (create mentions table)
env-start:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

env-stop:
	docker-compose -f $(DOCKER_COMPOSE_FILE) stop

env-destroy:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down -v --rmi local --remove-orphans

migrate:
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec -T worker python -m src.models

linting: ## Check/Enforce Python Code-Style
	flake8 src/*.py tests/*.py --max-line-length 88
	black src/*.py tests/*.py

test: ## Run tests and generate coverage report
	pytest --cov=src tests/

tweet-article: ## Scrape one of the defined sites and share the article on twitter
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec -T worker python -m src.bot --tweet-article

reply-mentions: ## Reply to twitter mentions
	docker-compose -f $(DOCKER_COMPOSE_FILE) exec -T worker python -m src.bot --reply-mentions

help: ## Display help text
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'