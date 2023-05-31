teste:
	python3 -m pytest -vv --cov=app --cov-report=term-missing -W ignore

run:
	cd app && uvicorn main:app --reload