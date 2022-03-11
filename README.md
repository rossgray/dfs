# Distributed Function Service

## Usage

### `make load-test`

Runs a load test against the service.

We run the service with increasing numbers of workers and measure the throughput as the number of functions passed to the service increases. Script creates a line chart showing the results.

### `make service-down`

Tears down the service.

### `make service workers=N`

Starts the service with N workers.

### `make client`

Simulates usage by a client (i.e. someone submitting a function for execution).

### `make dashboard`

Opens the `rq` monitoring dashboard.

Service code is inside `distribute_challenge`.

Client code is inside `client`.

### `make test`

Runs unit tests
