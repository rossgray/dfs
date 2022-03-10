.PHONY: service client dashboard test


service: workers?=1
service:
	docker compose up -d --build --scale worker=${workers}

service-down:
	docker compose down

dashboard:
	open http://localhost:9181

client:
	docker compose run client

load-test:
load-test:
	docker compose run client python -m client.load_test --csv_file results.csv --workers 5

test:
	ENV=test python -m pytest tests
