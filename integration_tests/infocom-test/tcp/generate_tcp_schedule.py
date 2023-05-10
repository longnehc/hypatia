import argparse
import networkload
import numpy as np
import random
from .world_grid import WorldGrid, get_world_grid
from .datacenter import get_datacenters, random_choose_dc
from .helper import add_closest_gs, get_endpoint_pairs, replace_bg_end_point_pairs, read_ep_pairs


SEED_START_TIMES = random.randint(0, 100000000)
SEED_FROM_TO = random.randint(0, 100000000)
SEED_FLOW_SIZE = random.randint(0, 100000000)


def generate_required_tcp_schedule(
    start_id,
    end_id,
    duration_seconds,
    source_ids,
    dst_ids,
    n_bg_flows,
    output_dir='.',
    gs_path='.',
    ep_filepath=None,
):
    """
    @param start_id: the first id of the end-point id range
    @param end_id: the last id of the end-point id range
    @param duration_seconds: range of flow start time from 0 ns
    @param source_ids: the list of source ids that we want to log
    @param dst_ids: the list of destination ids that we want to log
    @param n_bg_flows: number of background flows to simulate congestion, and we do not want to log them.
    @param output_dir: the path to store the generated TCP schedule.
    @param gs_path: the path to ground_stations.txt
    @param bg_ep_filepath: the file path to the end-point pairs for background flows
    @return: end-point pairs and flow ids for the measurement flows
    """

    # number of measurement flows will be the production of number of sources and destinations
    n_ms_flows = len(source_ids) * len(dst_ids)
    servers = set(range(start_id, end_id + 1))
    list_start_time_ns = generate_start_time_ns(duration_seconds, n_ms_flows, n_bg_flows)
    num_starts = len(list_start_time_ns)

    list_from_to = []

    # Forge measurement flows using srouce and dst ids
    for _src in source_ids:
        for _dst in dst_ids:
            # the _src, _dst here are still the ground station id, convert it to absolute id 
            list_from_to.append((_src + start_id, _dst + start_id))
    ms_flow_endpoints = list_from_to.copy()
    ms_flow_ids = list(range(n_ms_flows))

    # Ramdonly generate background flows
    # !!! A potential bug: the ''generate_bg_flows_by_user_distribution'' might generate measurement flows,
    # which can cause duplication
    bg_end_point_pairs = generate_bg_flows_by_user_distribution(n_bg_flows, gs_path, start_id)
    list_from_to = list_from_to + bg_end_point_pairs

    for i in range(len(ms_flow_ids)):
        if list_from_to[ms_flow_ids[i]] != ms_flow_endpoints[i]:
            raise AssertionError("Measurement flow IDs mismatch their endpoint pairs.")
        
    list_flow_size_byte = generate_flow_size_in_byte(num_starts)
    tcp_schedule_filename = output_dir + "/schedule.csv"
    write_tcp_schedule(num_starts, list_from_to, list_flow_size_byte, list_start_time_ns, tcp_schedule_filename)

    print("{} TCP measurement flows and {} TCP background flows are generated at {}."
          .format(n_ms_flows, n_bg_flows, output_dir ))

    ms_flow_id_filename = output_dir + "/ms_flow_ids.txt"
    write_ms_flow_ids(ms_flow_ids, ms_flow_id_filename)

    print("TCP measurement flow IDs are written to {}.".format(ms_flow_id_filename))

    return ms_flow_endpoints, ms_flow_ids


def generate_tcp_schedule(
        start_id,
        end_id,
        duration_seconds,
        n_ms_flows,
        n_bg_flows,
        is_unique,
        output_dir='.',
        gs_path='.',
        ep_filepath=None,
):
    """
    @param start_id: the first id of the end-point id range
    @param end_id: the last id of the end-point id range
    @param duration_seconds: range of flow start time from 0 ns
    @param n_ms_flows: number of measurement flows that we want to log during simulation.
    @param n_bg_flows: number of background flows to simulate congestion, and we do not want to log them.
    @param is_unique: indicate whether of the measurement flows have unique end-point pairs.
    @param output_dir: the path to store the generated TCP schedule.
    @param gs_path: the path to ground_stations.txt
    @param bg_ep_filepath: the file path to the end-point pairs for background flows
    @return: end-point pairs and flow ids for the measurement flows
    """
    servers = set(range(start_id, end_id + 1))
    list_start_time_ns = generate_start_time_ns(duration_seconds, n_ms_flows, n_bg_flows)
    num_starts = len(list_start_time_ns)

    # If end-point pairs cache is provided, use the cache to generate list_from_to
    if ep_filepath is not None:
        end_point_pairs_cache = read_ep_pairs(ep_filepath)
        list_from_to = random.choices(end_point_pairs_cache, k=n_ms_flows + n_bg_flows)
        print("Select {} pairs out of {} pairs from the cached end point pairs at {}"
              .format(n_ms_flows + n_bg_flows, len(end_point_pairs_cache), ep_filepath))
    else:
        list_from_to = generate_from_to_list(num_starts, servers)

    list_flow_size_byte = generate_flow_size_in_byte(num_starts)

    ms_flow_ids = random_pick_ms_flow_ids(list_from_to, n_ms_flows)
    if is_unique:
        make_endpoint_pair_unique(servers, list_from_to, ms_flow_ids)
    ms_flow_endpoints = get_ms_flow_endpoints(list_from_to, ms_flow_ids)

    # If the end-point pair cache is provided, the user distribution information
    # is already in the cache the frequency of end-point pairs is preserved
    if ep_filepath is None:
        bg_end_point_pairs = generate_bg_flows_by_user_distribution(n_bg_flows, gs_path, start_id)
        list_from_to = replace_bg_end_point_pairs(list_from_to, bg_end_point_pairs, ms_flow_ids)

    for i in range(len(ms_flow_ids)):
        if list_from_to[ms_flow_ids[i]] != ms_flow_endpoints[i]:
            raise AssertionError("Measurement flow IDs mismatch their endpoint pairs.")

    tcp_schedule_filename = output_dir + "/schedule.csv"
    write_tcp_schedule(num_starts, list_from_to, list_flow_size_byte, list_start_time_ns, tcp_schedule_filename)

    print("{} TCP measurement flows and {} TCP background flows are generated at {}."
          .format(n_ms_flows, n_bg_flows, output_dir ))

    ms_flow_id_filename = output_dir + "/ms_flow_ids.txt"
    write_ms_flow_ids(ms_flow_ids, ms_flow_id_filename)

    print("TCP measurement flow IDs are written to {}.".format(ms_flow_id_filename))

    return ms_flow_endpoints, ms_flow_ids


def generate_start_time_ns(duration_seconds, n_ms_flows, n_bg_flows):
    duration_ns = seconds_in_ns(duration_seconds)
    expected_flows_per_s = (n_ms_flows + n_bg_flows) / duration_seconds * 3  # Get enough flows
    list_start_time_ns = networkload.draw_poisson_inter_arrival_gap_start_times_ns(
        duration_ns, expected_flows_per_s, SEED_START_TIMES)
    list_start_time_ns = random.sample(list_start_time_ns, k=n_ms_flows + n_bg_flows)
    list_start_time_ns.sort()
    return list_start_time_ns


def random_pick_ms_flow_ids(list_from_to, n_ms_flows):
    ids = np.arange(len(list_from_to))
    ms_ids = random.sample(list(ids), k=n_ms_flows)
    ms_ids.sort()
    return ms_ids


def make_endpoint_pair_unique(servers, list_from_to, ms_flow_ids):
    unique_endpoints = set()
    for _id in ms_flow_ids:
        unique_endpoints.add(list_from_to[_id])
    # Regenerate to get enough unique ms flow ids
    while len(unique_endpoints) < len(ms_flow_ids):
        more_endpoints = networkload.draw_n_times_from_to_all_to_all(
            len(ms_flow_ids) - len(unique_endpoints), servers, get_new_seed()
        )
        unique_endpoints.update(more_endpoints)
    # Update list_from_to with new unique ms flow end-points
    list_unique_eps = list(unique_endpoints)
    for i in range(len(list_unique_eps)):
        list_from_to[ms_flow_ids[i]] = list_unique_eps[i]


def get_ms_flow_endpoints(list_from_to, ms_flow_ids):
    ms_flow_endpoints = []
    for _id in ms_flow_ids:
        ms_flow_endpoints.append(list_from_to[_id])
    return ms_flow_endpoints


def generate_from_to_list(num_starts, servers):
    # Get (From, To) tuples for each start time
    list_from_to = networkload.draw_n_times_from_to_all_to_all(num_starts, servers, SEED_FROM_TO)
    return list_from_to


def generate_flow_size_in_byte(num_starts):
    list_flow_size_byte = list(
        round(x) for x in networkload.draw_n_times_from_cdf(
            num_starts, networkload.CDF_PFABRIC_WEB_SEARCH_BYTE, True, SEED_FLOW_SIZE)
    )
    return list_flow_size_byte


def generate_bg_flows_by_user_distribution(n_bg_flows, gs_path, start_id):
    world_grid: WorldGrid = get_world_grid()

    destinations = world_grid.random_select_grid_position(n_bg_flows)
    add_closest_gs(destinations, gs_path)

    datacenters = get_datacenters()
    add_closest_gs(datacenters, gs_path)
    chosen_dc = random_choose_dc(datacenters, destinations)

    bg_end_point_pairs = get_endpoint_pairs(chosen_dc, destinations, start_id)

    return bg_end_point_pairs


def write_tcp_schedule(num_starts, list_from_to, list_flow_size_byte, list_start_time_ns, output_filename):
    networkload.write_schedule(
        output_filename,
        num_starts,
        list_from_to,
        list_flow_size_byte,
        list_start_time_ns
    )


def write_ms_flow_ids(ms_flow_ids, filename):
    with open(filename, 'w') as f:
        for _id in ms_flow_ids:
            f.write('{}\n'.format(_id))


def seconds_in_ns(seconds):
    return seconds * 1000 * 1000 * 1000


def get_new_seed():
    return random.randint(0, 100000000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a TCP flow schedule csv file.')
    parser.add_argument('--start_id', action="store", dest="start_id", type=int)
    parser.add_argument('--end_id', action="store", dest="end_id", type=int)
    parser.add_argument('--duration_s', action="store", dest="duration_s", default=10, type=int)
    parser.add_argument('--n_ms_flows', action="store", dest="n_ms_flows", default=1, type=int)
    parser.add_argument('--n_bg_flows', action="store", dest='n_bg_flows', default=0, type=int)
    parser.add_argument('--is_unique', action="store", dest="is_unique", default=False, type=bool)
    args = parser.parse_args()

    generate_tcp_schedule(
        args.start_id,
        args.end_id,
        args.duration_s,
        args.n_ms_flows,
        args.n_bg_flows,
        args.is_unique,
    )
