# Distributed Function Service

## Architecture

We are using the Python [rq](https://python-rq.org/) library for queuing jobs are processing them using multiple workers.

Redis is used as the queue backend.

The individual pieces of the service are run using Docker Compose.

Service code is inside `distribute_challenge`.

Client code is inside `client`.

An example of how the service is used is in `client/main.py`

Load testing is done using a simple bash + Python script, with `pandas` + `plotly` for outputting the results.

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

### `make test`

Runs unit tests
