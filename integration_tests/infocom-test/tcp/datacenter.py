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


def find_closest_gs(datacenters, gs_filepath):
    """
    Find the closest ground station to the given datacenter.
    @param datacenters: a list of datacenters
    @param gs_filepath: the file path of the ground_stations.txt
    @return: list of datacenters with the closest ground station in
             their attribute
    """
    ground_stations = read_gs_file(gs_filepath)
    for dc in datacenters:
        closest_gs = find_closest_gs_for(dc, ground_stations)
        dc['closest_gs'] = closest_gs
    return datacenters


def find_closest_gs_for(datacenter, ground_stations):
    """
    @param datacenter: a datacenter
    @param ground_stations: a ground station
    @return: the closest ground station to the datacenter
    """
    min_distance = float('inf')
    closest_gs = ground_stations[0]
    for gs in ground_stations:
        _distance = distance.distance(
            (datacenter['latitude'], datacenter['longitude']),
            (gs['latitude'], gs['longitude'])
        )
        if _distance < min_distance:
            min_distance = _distance
            closest_gs = gs
    return closest_gs


def read_gs_file(gs_file_path):
    """
    @param gs_file_path: the path of the ground_stations.txt
    @return: a list of ground stations
    """
    ground_stations = []
    with open(gs_file_path, 'r') as f:
        for line in f:
            gs = {}
            split = line.split(',')
            gs['id'] = split[0]
            gs['location'] = split[1]
            gs['latitude'] = float(split[2])
            gs['longitude'] = float(split[3])
            ground_stations.append(gs)
    return ground_stations
