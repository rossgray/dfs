import argparse
import concurrent.futures
from client.example import func

import logging
import time
import csv


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

NUM_TESTS_TO_RUN = 3


def run(csv_file: str, workers: int):
    results = {}
    for exp in range(NUM_TESTS_TO_RUN):
        num_functions = pow(2, exp)
        start = time.time()
        run_individual_test(num_functions)
        end = time.time()
        total_time = end - start
        avg_throughput = num_functions / total_time
        results[num_functions] = avg_throughput

    with open(csv_file, mode='w') as results_file:
        writer = csv.writer(results_file, delimiter=',', quotechar='"')
        for num_functions, avg_throughput in results.items():
            writer.writerow([workers, num_functions, avg_throughput])


def run_individual_test(num_functions: int):
    logger.info(f'Running load test with {num_functions} functions...')
    f = func(2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_functions) as executor:
        futures = []
        for _ in range(num_functions):
            futures.append(executor.submit(f.run))
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str)
    parser.add_argument('--workers', type=int)
    args = parser.parse_args()
    run(**vars(args))
