"""Analyse REFIR outputs to extract maximum concentration and affected area."""


def main():
    # TODO: write this...
    # list directories for each model run
    # for each one, get the max_concentration_data
    # and the affected area
    # write the value to csv
    return


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
        time = xy_slice.coord('time').points[0]
        if xy_slice.data.max() == max_concentration:
            break

    data = {'flight_level': flight_level,
            'time': time,
            'max_concentration': max_concentration}

    return data


if '__name__' == '__main__':
    main()
