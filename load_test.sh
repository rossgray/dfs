#!/usr/bin/env bash

# Runs a load test where we run the service with increasing numbers of workers
# and measure the throughput as the number of functions passed to the service
# increases. Script creates a line chart showing the results.

set -euo pipefail

RESULTS_CSV="results.csv"
RESULTS_CHART="results.png"

function run_test() {
    num_workers=${1}
    echo "starting service with ${num_workers} workers..."
    docker compose up -d --build --scale worker=${num_workers}
    wait_for_service
    echo "service ready!"
    echo "running load test..."
	docker compose run client python -m client.load_test --csv_file ${RESULTS_CSV} --workers ${num_workers}
    echo "load test complete"
}

function plot_results() {
	docker compose run client python -m client.plot_results --csv_file ${RESULTS_CSV} --output_file ${RESULTS_CHART}
    open ${RESULTS_CHART}
}

# waits for service to become ready
function wait_for_service() {
    max_time=30
    ready=$(is_service_ready)

    i=0
    while [[ ${ready} != "true" ]]
    do
        echo "waiting for service to become ready..."
        sleep 1
        ready=$(is_service_ready)
        (( i++ ))
        if [[ ${i} == ${max_time} ]]; then
            echo "waited too long"
            exit 1
        fi
    done

}

function is_service_ready() {
    # There should be 3 services running
    # (worker, dashboard, redis)
    expected_services=3
    num_services=$(docker compose ps --services --status running | wc -l | xargs)
    if [[ ${num_services} == ${expected_services} ]]; then
        echo "true"
    else
        echo "false"
    fi
}


WORKER_STEPS=(2 5 10 20)

# remove results CSV file in case it already exists
rm -f ${RESULTS_CSV}
for num_workers in ${WORKER_STEPS[@]}; do
  run_test ${num_workers}
done
plot_results
sleep 2
docker compose down