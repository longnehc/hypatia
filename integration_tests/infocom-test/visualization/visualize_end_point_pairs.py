import folium


def draw_end_point_pairs_on_map(tcp_flows, ground_stations, description):
    start_id = int(description['num_orbits']) * int(description['num_satellites_per_orbit'])
    source_counts, dest_counts = count_end_points(tcp_flows)
    draw_end_points(tcp_flows, ground_stations, dest_counts, start_id, 'destination_map.html', 'red', 500)
    draw_end_points(tcp_flows, ground_stations, source_counts, start_id, 'source_map.html', 'green', 100)


def draw_end_points(tcp_flows, ground_stations, end_point_counts, start_id, filename, color, base_circle_radius=500):
    m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)
    for gs_id, counts in end_point_counts.items():
        dest_gs = ground_stations[gs_id - start_id]

        # Add destination
        folium.CircleMarker(
            location=[dest_gs['latitude'], dest_gs['longitude']],
            popup='{}-{}'.format(dest_gs['id'], dest_gs['location']),
            radius=counts / len(tcp_flows) * base_circle_radius,
            color=color,
            fill=True,
        ).add_to(m)
    # Save the map
    m.save(filename)
    print('The map is saved as {}'.format(filename))


def count_end_points(tcp_flows):
    source_counts = {}
    dest_counts = {}
    for flow in tcp_flows:
        # Count source
        if flow['source'] in source_counts:
            source_counts[flow['source']] += 1
        else:
            source_counts[flow['source']] = 1

        # Count destinations
        if flow['destination'] in dest_counts:
            dest_counts[flow['destination']] += 1
        else:
            dest_counts[flow['destination']] = 1

    return source_counts, dest_counts


def read_tcp_schedule(filepath):
    tcp_flows = []
    with open(filepath, 'r') as f:
        for line in f:
            split = line.split(',')
            tcp_flows.append(
                {
                    'id': split[0],
                    'source': int(split[1]),
                    'destination': int(split[2]),
                }
            )
    return tcp_flows


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


def read_description(filepath):
    description = {}
    with open(filepath, 'r') as f:
        for line in f:
            split = line.strip().split('=')
            description[split[0]] = split[1]
    return description


if __name__ == '__main__':
    _tcp_flows = read_tcp_schedule('../temp/runs/starlink_550_isls_none_tcp/schedule.csv')
    _ground_stations = read_gs_file('../temp/gen_data/starlink_550_isls_none_infocom_test/ground_stations.txt')
    _description = read_description('../temp/gen_data/starlink_550_isls_none_infocom_test/description.txt')
    draw_end_point_pairs_on_map(_tcp_flows, _ground_stations, _description)
