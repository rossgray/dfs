.PHONY: service client test

workers?=1

service:
	docker compose up --build --scale worker=${workers}

client:
	docker compose run client

test:
	ENV=test python -m pytest tests
