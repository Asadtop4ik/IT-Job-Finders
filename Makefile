# Define the Python interpreter and Django management command
PYTHON = python3
MANAGE = $(PYTHON) manage.py

# Default target: show available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make runserver      Run the Django development server"
	@echo "  make migrate        Apply database migrations"
	@echo "  make makemigrations Create new database migrations"
	@echo "  make test           Run tests"
	@echo "  make shell          Open the Django shell"
	@echo "  make clean          Clean up temporary files"
	@echo "  make createsuperuser Create a superuser"

# Target to run the development server
.PHONY: runserver
runserver:
	$(MANAGE) runserver

# Target to apply database migrations
.PHONY: migrate
migrate:
	$(MANAGE) migrate

# Target to create new database migrations
.PHONY: makemigrations
makemigrations:
	$(MANAGE) makemigrations

# Target to run tests
.PHONY: test
test:
	$(MANAGE) test

# Target to open the Django shell
.PHONY: shell
shell:
	$(MANAGE) shell

# Target to clean up temporary files
.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

# Target to create a superuser
.PHONY: createsuperuser
createsuperuser:
	$(MANAGE) createsuperuser
