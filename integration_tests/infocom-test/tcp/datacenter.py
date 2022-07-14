import random

from geopy import distance


DATACENTERS = [
    {
        'region': 'Bahrain',
        'latitude': 26.061511,
        'longitude': 50.534737,
    },
    {
        'region': 'Cape Town',
        'latitude': -33.926226,
        'longitude': 18.420863,
    },
    {
        'region': 'London',
        'latitude': 51.502339,
        'longitude': -0.058766,
    },
    {
        'region': 'Mumbai',
        'latitude': 19.050027,
        'longitude': 72.883578,
    },
    {
        'region': 'North California',
        'latitude': 40.760744,
        'longitude': -123.291029,
    },
    {
        'region': 'Sao Paulo',
        'latitude': 1.344019,
        'longitude': 103.855261,
    },
    {
        'region': 'Sydney',
        'latitude': -33.877200,
        'longitude': 151.220916,
    },
    {
        'region': 'Tokyo',
        'latitude': 35.696570,
        'longitude': 139.817398,
    },
]


def get_datacenters():
    """
    @return: a list of datacenters
    """
    return DATACENTERS


def random_choose_dc(datacenters, destinations):
    chosen_dc = []
    for i in range(len(destinations)):
        dc = random_choose_dc_by_distance(datacenters, destinations[i])
        chosen_dc.append(dc)
    return chosen_dc


def random_choose_dc_by_distance(datacenters, destination):
    """
    @param datacenters: a list of datacenters to choose from
    @param destination:
    @param gs_for_dest: the ground station for the destination.
                        The closest ground station to the chosen datacenter
                        cannot be the same as the ground station for the
                        destination.
    @return: a chosen datacenter as the traffic source
    """
    # Remove the datacenter that has the same closest gs as the destination
    for dc in datacenters:
        if dc['closest_gs']['id'] == destination['closest_gs']['id']:
            datacenters.remove(dc)

    total_distance = 0
    dc_distance = []
    for dc in datacenters:
        _distance = distance.distance(
            (destination['latitude'], destination['longitude']),
            (dc['latitude'], dc['longitude'])
        )
        dc_distance.append(_distance.km)
        total_distance += _distance.km

    dc_weights = []
    for dist in dc_distance:
        dc_weights.append(dist / total_distance)

    chosen_dc = random.choices(datacenters, weights=dc_weights, k=1)[0]
    return chosen_dc
