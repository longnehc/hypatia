from geopy import distance


def add_closest_gs(locations, gs_filepath):
    """
    Find the closest ground station to the given datacenter.
    @param locations: a list of locations containing 'latitude' and 'longitude' keys
    @param gs_filepath: the file path of the ground_stations.txt
    @return: list of datacenters with the closest ground station in
             their attribute
    """
    ground_stations = read_gs_file(gs_filepath)
    closest_ground_stations = []
    for lc in locations:
        closest_gs = find_closest_gs_for(lc, ground_stations)
        closest_ground_stations.append(closest_gs)
        lc['closest_gs'] = closest_gs
    return closest_ground_stations


def find_closest_gs_for(location, ground_stations):
    """
    @param location: a location containing 'latitude' and 'longitude' keys
    @param ground_stations: a ground station
    @return: the closest ground station to the datacenter
    """
    min_distance = float('inf')
    closest_gs = ground_stations[0]
    for gs in ground_stations:
        _distance = distance.distance(
            (location['latitude'], location['longitude']),
            (gs['latitude'], gs['longitude'])
        )
        if _distance.km < min_distance:
            min_distance = _distance.km
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
            gs['id'] = int(split[0])
            gs['location'] = split[1]
            gs['latitude'] = float(split[2])
            gs['longitude'] = float(split[3])
            ground_stations.append(gs)
    return ground_stations


def get_endpoint_pairs(sources, destinations, start_id):
    ed_pairs = []
    for i in range(len(sources)):
        ed_pairs.append(
            (
                sources[i]['closest_gs']['id'] + start_id,
                destinations[i]['closest_gs']['id'] + start_id
            )
        )
    return ed_pairs


def replace_bg_end_point_pairs(list_from_to, bg_end_point_pair, ms_flow_ids):
    bg_pair_counter = 0
    for i in range(len(list_from_to)):
        if i in ms_flow_ids:
            # This is a measurement flow, skip
            continue
        list_from_to[i] = bg_end_point_pair[bg_pair_counter]
        bg_pair_counter += 1
    return list_from_to


def read_ep_pairs(filepath):
    ep_pairs = []
    with open(filepath, 'r') as f:
        for line in f:
            split = line.strip().split(',')
            ep_pairs.append(
                (int(split[0]), int(split[1]))
            )
    return ep_pairs
