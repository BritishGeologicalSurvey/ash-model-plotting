"""Analyse REFIR outputs to extract maximum concentration and affected area."""
import iris


def main():
    # TODO: write this...
    # list directories for each model run
    # for each one, get the max_concentration_data
    # and the affected area
    # write the value to csv
    return


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


if '__name__' == '__main__':
    main()
