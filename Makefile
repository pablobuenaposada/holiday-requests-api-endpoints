DOCKER_IMAGE=holidays
TEST_ENV_VARS:=$(shell cat .env.test | xargs)

venv:
	python3.10 -m venv venv
	venv/bin/pip install -r requirements.txt

format:
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black src
	venv/bin/isort src
	venv/bin/flake8 src

format/check: venv
	venv/bin/pip install -r requirements-tests.txt
	venv/bin/black --verbose src --check
	venv/bin/isort --df -c src
	venv/bin/flake8 src

migrate:
	venv/bin/python src/manage.py migrate

tests: venv
	venv/bin/pip install -r requirements-tests.txt
	$(TEST_ENV_VARS) PYTHONPATH=src venv/bin/pytest src/tests

run/local: venv migrate
	PYTHONPATH=src venv/bin/python src/manage.py createsuperuser --noinput --username user_manager --type manager
	PYTHONPATH=src venv/bin/python src/manage.py createsuperuser --noinput --username user_worker --type worker
	PYTHONPATH=src venv/bin/python src/manage.py drf_create_token user_manager
	PYTHONPATH=src venv/bin/python src/manage.py drf_create_token user_worker
	PYTHONPATH=src venv/bin/python src/manage.py runserver 0.0.0.0:8000

docker/build:
	docker build --no-cache	--tag=$(DOCKER_IMAGE) .

docker/run:
	docker run --name $(DOCKER_IMAGE) -d -p 8000:8000 $(DOCKER_IMAGE)

docker/tests:
	 docker run $(DOCKER_IMAGE) /bin/sh -c 'make tests'