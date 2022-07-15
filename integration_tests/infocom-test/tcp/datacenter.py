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
    {
        'region': 'Oregon',
        'latitude': 45.006884,
        'longitude': -121.477004,
    },
    {
        'region': 'AWS GovCloud (US-West)',
        'latitude': 42.262954,
        'longitude': -118.298180,
    },
    {
        'region': 'Ohio',
        'latitude': 40.154962,
        'longitude': -82.860364,
    },
    {
        'region': 'AWS GovCloud (US-East)',
        'latitude': 39.022142,
        'longitude': -78.153935,
    },
    {
        'region': 'Northern Virginia',
        'latitude': 39.082352,
        'longitude': -77.697201,
    },
    {
        'region': 'Canada Central',
        'latitude': 46.553088,
        'longitude': -76.491743,
    },
    {
        'region': 'Ireland',
        'latitude': 53.224383,
        'longitude': -7.474220,
    },
    {
        'region': 'Paris',
        'latitude': 48.877008,
        'longitude': 2.371268,
    },
    {
        'region': 'Frankfurt',
        'latitude': 50.089564,
        'longitude': 8.637410,
    },
    {
        'region': 'Milan',
        'latitude': 45.448918,
        'longitude': 9.195937,
    },
    {
        'region': 'Europe (Stockholm)',
        'latitude': 63.719112,
        'longitude': 14.202794,
    },
    {
        'region': 'Ningxia',
        'latitude': 37.251822,
        'longitude': 105.880336,
    },
    {
        'region': 'Beijing',
        'latitude': 39.858346,
        'longitude': 116.397592,
    },
    {
        'region': 'Seoul',
        'latitude': 37.532198,
        'longitude': 126.998110,
    },
    {
        'region': 'Osaka',
        'latitude': 34.674190,
        'longitude': 135.516591,
    },
    {
        'region': 'Hong Kong SAR',
        'latitude': 22.327122,
        'longitude': 114.181792,
    },
    {
        'region': 'Singapore',
        'latitude': 1.340082,
        'longitude': 103.869646,
    },
    {
        'region': 'Jakarta',
        'latitude': -6.191501,
        'longitude': 106.833628,
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
