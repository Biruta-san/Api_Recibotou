run:
	uvicorn app.main:app --reload

migrate:
	alembic upgrade head

revision:
	alembic revision -m "msg" --autogenerate

test:
	pytest -q

lint:
	ruff check . || true