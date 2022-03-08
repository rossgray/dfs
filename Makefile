.PHONY: service client test

workers?=1

service:
	docker compose up -d --build --scale worker=${workers}

service-down:
	docker compose down

client:
	docker compose run client

test:
	ENV=test python -m pytest tests
