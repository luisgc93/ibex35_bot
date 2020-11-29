help:
	@grep '^[a-zA-Z]' $(MAKEFILE_LIST) | sort | awk -F ':.*?## ' 'NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}'

install-requirements: ## Push and open github pull request page
	pip install -r requirements.txt

make linting:
	flake8 src/*.py tests/*.py --max-line-length 88
	black src/*.py tests/*.py

test: ## Run tests and generate coverage report
	pytest --cov=src tests/

tweet-article: ## Scrape one of the defined sites and share the article on twitter

reply-mentions: ## Reply to twitter mentions
