#!/usr/bin/env bash

set -euo pipefail

function run_test() {
    num_workers=${1}
    echo "starting service..."
    make service workers=${num_workers}
    wait_for_service
    echo "service ready!"
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
    num_services=$(docker compose ps --services --status running | wc -l | xargs)
    if [[ "${num_services}" == "3" ]]; then
        echo "true"
    else
        echo "false"
    fi
}


WORKER_STEPS=(1 2 5 10 20)

run_test 1
# for num_workers in ${WORKER_STEPS[@]}; do
#   run_test ${num_workers}
# done