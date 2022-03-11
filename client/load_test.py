"""Runs a load test against our distributed service.

Arguments:
    csv_file: Writes results to provided CSV file path
    workers: Number of workers service is using (this is only used to record
        results and doesn't have any affect on the test itself)
"""
import argparse
import concurrent.futures
import csv
import logging
import time

from client.functions import func

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

NUM_TESTS_TO_RUN = 8


def run(csv_file: str, workers: int):
    """Run a load test by increasing the number of functions we attempt to run
    exponentially, up to a maximum of 2^(NUM_TESTS_TO_RUN-1).

    We time how long each test takes to run, so that we can calculate the
    average throughput (number of functions run / second).
    """
    results = {}
    for exp in range(NUM_TESTS_TO_RUN):
        num_functions = pow(2, exp)
        start = time.time()
        run_individual_test(num_functions)
        end = time.time()
        total_time = end - start
        avg_throughput = num_functions / total_time
        results[num_functions] = avg_throughput

    write_results(csv_file=csv_file, results=results, workers=workers)


def run_individual_test(num_functions: int):
    """Runs an individual test by calling 'func_to_run' multiple times using
    multithreading ThreadPoolExecutor
    """
    logger.info(f'Running load test with {num_functions} functions...')

    func_to_run = func(2)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_functions) as executor:
        futures = []
        for _ in range(num_functions):
            futures.append(executor.submit(func_to_run.run))
        for future in concurrent.futures.as_completed(futures):
            future.result()


def write_results(csv_file: str, results: dict, workers: int):
    with open(csv_file, mode='a') as results_file:
        writer = csv.writer(results_file, delimiter=',', quotechar='"')
        for num_functions, avg_throughput in results.items():
            writer.writerow([workers, num_functions, avg_throughput])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True)
    parser.add_argument('--workers', type=int, required=True)
    args = parser.parse_args()
    run(**vars(args))
