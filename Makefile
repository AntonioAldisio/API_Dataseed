teste:
	python3 -m pytest -vv --cov=app --cov-report=term-missing -W ignore

run:
	cd app && uvicorn main:app --reload --host 0.0.0.0 --port 80

createVirtualenv:
	virtualenv api && source api/bin/activate && pip install -r requirements.txt && pip install -r requirements-dev.txt

docker-build:
	docker-compose up --build

docker-up:
	docker-compose up

docker-down:
	docker-compose down