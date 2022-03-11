"""Plots results in CSV file path given by 'csv_file' and outputs image to path
given by 'output_file'

CSV file is expected to be in particular format, having the following columns:
['workers', 'functions', 'throughput']
"""
import argparse

import pandas
import plotly.express as px


def run(csv_file: str, output_file: str):
    df = pandas.read_csv(
        csv_file,
        names=['workers', 'functions', 'throughput'],
    )
    fig = px.line(
        df,
        x="functions",
        y="throughput",
        color='workers',
        labels={'throughput': 'throughput (functions/s)'},
        markers=True,
    )
    fig.write_image(output_file, format='png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file', type=str, required=True)
    parser.add_argument('--output_file', type=str, required=True)
    args = parser.parse_args()
    run(**vars(args))
