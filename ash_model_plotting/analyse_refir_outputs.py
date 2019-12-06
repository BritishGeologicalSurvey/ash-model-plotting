"""Analyse REFIR outputs to extract maximum concentration and affected area."""
import argparse
import matplotlib.pyplot as plt
from pathlib import Path

import iris
import pandas as pd

from ash_model_plotting.ash_model_result import AshModelResult

EXPERIMENTS = ['30MinAv']
MODELS = ['MastinOnly', 'EmpOnly', 'WindOnly', 'AllModels']
RUNS = ['Av', 'Max', 'Min']


def main(data_dir, output_dir):
    # Configure directories
    data_dir = Path(data_dir)
    if output_dir:
        output_dir = Path(output_dir)
        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)
    else:
        output_dir = data_dir

    # Analyse runs
    all_results = []
    for experiment in EXPERIMENTS:
        for model in MODELS:
            for run in RUNS:
                print(experiment, model, run)
                results = analyse_run(data_dir, experiment, model, run)
                all_results.append(results)

    # Convert to dataframe to export csv
    df = pd.DataFrame(all_results)
    df = df.set_index(['experiment', 'model', 'run'])
    df.to_csv(output_dir / 'REFIR_summary.csv')

    # Plot results
    plot_results(df, output_dir)


def plot_results(results_df, output_dir):
    # Plot advisory_area results
    advisory_area = results_df['advisory_area'] / 1e6
    fig, ax = plot_bar_with_errors(advisory_area)
    ax.set_ylabel('Advisory area [km2]')
    plt.tight_layout()
    fig.savefig(output_dir / 'REFIR_advisory_area.png', dpi=450)
    plt.close()

    # Plot advisory_area results
    max_concentration = results_df['max_concentration']
    fig, ax = plot_bar_with_errors(max_concentration)
    ax.set_ylabel('Concentration [g/m3]')
    plt.tight_layout()
    fig.savefig(output_dir / 'REFIR_max_concentration.png', dpi=450)
    plt.close()


def plot_bar_with_errors(df):
    # Prepare data
    heights = df.xs('Av', level='run')
    min_offset = heights - df.xs('Min', level='run')
    max_offset = df.xs('Max', level='run') - heights
    error_bars = [min_offset, max_offset]
    x_pos = range(len(heights))

    # Plot
    fig, ax = plt.subplots()
    plt.bar(x_pos, heights, yerr=error_bars, align='center', alpha=0.5,
            capsize=10)

    # Labels for bars.  Can't use heights.index.levels[1] because Pandas sorts
    # their names in alphabetical order
    ax.set_xticks(x_pos)
    labels = [i[1] for i in heights.index.tolist()]
    ax.set_xticklabels(labels)
    plt.grid()

    return fig, ax


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
            max_flight_level = flight_level
            max_timestamp = timestamp
            max_area = advisory_area

    data = {'flight_level': max_flight_level,
            'time': max_timestamp,
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
