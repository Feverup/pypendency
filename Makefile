ifneq ($(docker),0)
    DOCKER_CMD := docker-compose run --rm pypendency
endif

tests:
	$(DOCKER_CMD) python -m unittest

format:
	$(DOCKER_CMD) python -m  black --config=pyproject.toml src/ tests/

flake8:
	$(DOCKER_CMD) python -m flake8 --config=.flake8 src/ tests/

mypy:
	$(DOCKER_CMD) python -m mypy --config-file=pyproject.toml src/ tests/

black:
	$(DOCKER_CMD) python -m black --config=pyproject.toml --check src/ tests/

lint: flake8 black mypy