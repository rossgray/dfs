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
	bash load_test.sh

test:
	docker compose run test
