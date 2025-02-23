include settings/.env

install-deps:
	poetry install --no-root

run-dev: install-deps
	uvicorn --host $(HOST) --port $(PORT) --reload --factory app.main:init_app

run-prod: install-deps
	gunicorn 'app.main:init_app()' --config settings/gunicorn_conf.py -b $(HOST):$(PORT)

run-test: install-deps
	pytest -s --maxfail=1 -p no:warnings --cache-clear tests/

.PHONY: install-deps run-dev run-prod .run-test
