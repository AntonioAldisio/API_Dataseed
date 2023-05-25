teste:
	python3 -m pytest -vv --cov=app --cov-report=term-missing

run:
	cd app && uvicorn main:app --reload