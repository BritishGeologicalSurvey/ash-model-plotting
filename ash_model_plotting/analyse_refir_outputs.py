"""Analyse REFIR outputs to extract maximum concentration and affected area."""
import argparse
import matplotlib.pyplot as plt
from pathlib import Path

import iris
import pandas as pd

from ash_model_plotting.ash_model_result import AshModelResult

EXPERIMENTS = ['30MinAv']
MODELS = ['EmpOnly', 'MastinOnly', 'WoodOnly', 'WWOnly']
RUNS = ['Av', 'Max', 'Min']


def main(data_dir, output_dir):
    # Configure directories
    data_dir = Path(data_dir)
    if output_dir:
        output_dir = Path(output_dir)
    else:
        output_dir = data_dir

    # Analyse runs
    all_results = []
    for experiment in EXPERIMENTS:
        for model in MODELS[:-1]:  # WWOnly was broken
            for run in RUNS:
                print(experiment, model, run)
                results = analyse_run(data_dir, experiment, model, run)
                all_results.append(results)

    # Convert to dataframe to export csv
    df = pd.DataFrame(all_results)
    df = df.set_index(['experiment', 'model', 'run'])
    df.to_csv(output_dir / 'REFIR_summary.csv')

    # Plot advisory_area results
    advisory_area = df['advisory_area'] / 1e6
    advisory_area.plot.bar()
    plt.ylabel('Advisory area (>0.002 g/m3)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_dir / 'REFIR_advisory_area.png')
    plt.close()

    # Plot advisory_area results
    df['max_concentration'].plot.bar()
    plt.ylabel('Concentration (g/m3)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_dir / 'REFIR_max_concentration.png')
    plt.close()


def analyse_run(data_dir, experiment, model, run):
    """
    Analyse the outputs from a single model run.

    :param run_dir: str, directory containing NAME *.txt files
    """
    # Locate data
    run_dir = data_dir / experiment / model / run
    name_files = [str(f.absolute()) for f in run_dir.glob("Fields_grid88*.txt")]

    # Calculate outputs
    ash_model_result = AshModelResult(name_files)
    advisory_area_params = advisory_area(ash_model_result)
    max_concentration_params = max_concentration_data(ash_model_result)

    # Prepare for return
    results = {
        "experiment": experiment,
        "model": model,
        "run": run,
        "advisory_area": advisory_area_params['advisory_area'],
        "advisory_area_z": advisory_area_params['flight_level'],
        "advisory_area_t": advisory_area_params['time'],
        "max_concentration": max_concentration_params['max_concentration'],
        "max_concentration_z": max_concentration_params['flight_level'],
        "max_concentration_t": max_concentration_params['time'],
        }

    return results


def advisory_area(ash_model_result, threshold=0.002):
    """
    Extract area and z, t coordinates for maximum area of concentration
    above a given threshold.

    :param ash_model_result: AshModelResult for model run
    :param threshold: threshold concentration
    """
    cube = ash_model_result.air_concentration
    cell_areas = iris.analysis.cartography.area_weights(
        cube.slices(['latitude', 'longitude']).next())
    max_area = 0

    for xy_slice in cube.slices(['latitude', 'longitude']):
        flight_level = xy_slice.coord('flight_level').points[0]
        timestamp = xy_slice.coord('time').points[0]
        timestamp = xy_slice.coord('time').units.num2date(timestamp)

        advisory_area = cell_areas[xy_slice.data > threshold].sum()
        if advisory_area > max_area:
            max_area = advisory_area

    data = {'flight_level': flight_level,
            'time': timestamp,
            'advisory_area': max_area}

    return data


def max_concentration_data(ash_model_result):
    """
    Extract magnitude and z, t, x, y coordinates for maximum air
    concentration.

    :param ash_model_result: AshModelResult for model run
    """
    cube = ash_model_result.air_concentration
    max_concentration = cube.data.max()

    for xy_slice in cube.slices(['latitude', 'longitude']):
        flight_level = xy_slice.coord('flight_level').points[0]
        timestamp = xy_slice.coord('time').points[0]
        timestamp = xy_slice.coord('time').units.num2date(timestamp)
        if xy_slice.data.max() == max_concentration:
            break

    data = {'flight_level': flight_level,
            'time': timestamp,
            'max_concentration': max_concentration}

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Analyse REFIR experiment output files")
    parser.add_argument('data_dir', type=str,
                        help='directory containing REFIR experiment output data')
    parser.add_argument('--output_dir', type=str,
                        help='output directory for results')
    args = parser.parse_args()
    main(args.data_dir, args.output_dir)
