import argparse
import exputil
import networkload
import random
import os


try:
    from .run_list import *
except (ImportError, SystemError):
    from run_list import *


# Set up random seeds
# random.seed(123456789)
SEED_START_TIMES = random.randint(0, 100000000)
SEED_FROM_TO = random.randint(0, 100000000)
SEED_FLOW_SIZE = random.randint(0, 100000000)
local_shell = exputil.LocalShell()


def generate_tcp_schedule(
        start_id, 
        end_id,
        duration_seconds,
        expected_flows_per_s,
        n_flows,
        is_unique=False,
        n_bg_flows=0,
):
    """
    https://github.com/snkas/networkload/blob/master/example/example.py
    The total number of flows is randomly generated based on the expected_flows_per_s,
    so the total number of flows may vary. If we always want a specific number of flows,
    use n_flows to specify the total number of flows.
    """
    servers = set(range(start_id, end_id + 1))
    list_start_time_ns = generate_start_time_ns(expected_flows_per_s, duration_seconds, n_flows)
    num_starts = len(list_start_time_ns)
    list_from_to = generate_from_to_list(num_starts, servers, is_unique)
    list_flow_size_byte = generate_flow_size_in_byte(num_starts)

    write_tcp_schedule(
        num_starts, list_from_to, list_flow_size_byte, list_start_time_ns,
        "temp/runs/" + get_tcp_run_list()[0]["name"] + "/schedule.csv"
    )

    return list_from_to


def generate_start_time_ns(expected_flows_per_s, duration_seconds, n_flows):
    # Traffic start time in ns
    duration_ns = seconds_in_ns(duration_seconds)
    # If n_flows is specified, return exactly n_flows
    if n_flows > 0:
        expected_flows_per_s = n_flows / duration_seconds * 2  # Multiply by 2 to ensure we have enough flows

    list_start_time_ns = networkload.draw_poisson_inter_arrival_gap_start_times_ns(
        duration_ns, expected_flows_per_s, SEED_START_TIMES)

    if n_flows > 0:
        list_start_time_ns = random.choices(list_start_time_ns, k=n_flows)
        list_start_time_ns.sort()

    return list_start_time_ns


def generate_from_to_list(num_starts, servers, is_unique):
    # Get (From, To) tuples for each start time
    list_from_to = networkload.draw_n_times_from_to_all_to_all(num_starts, servers, SEED_FROM_TO)

    # Ensure the end-point pairs are unique
    if is_unique:
        set_from_to = set(list_from_to)
        while len(set_from_to) < len(list_from_to):
            additional_from_to = networkload.draw_n_times_from_to_all_to_all(
                len(list_from_to) - len(set_from_to), servers, get_new_seed()
            )
            set_from_to.update(additional_from_to)
        list_from_to = list(set_from_to)

    return list_from_to


def generate_flow_size_in_byte(num_starts):
    list_flow_size_byte = list(
        round(x) for x in networkload.draw_n_times_from_cdf(
            num_starts, networkload.CDF_PFABRIC_WEB_SEARCH_BYTE, True, SEED_FLOW_SIZE)
    )
    return list_flow_size_byte


def write_tcp_schedule(num_starts, list_from_to, list_flow_size_byte, list_start_time_ns, output_filename):
    networkload.write_schedule(
        output_filename,
        num_starts,
        list_from_to,
        list_flow_size_byte,
        list_start_time_ns
    )
    print("{} TCP flow(s) have been generated at {}.".format(num_starts, output_filename))


def seconds_in_ns(seconds):
    return seconds * 1000 * 1000 * 1000


def get_new_seed():
    return random.randint(0, 100000000)


if __name__ == '__main__':
    if os.path.exists('schedule.csv'): 
        os.remove('schedule.csv') 
    parser = argparse.ArgumentParser(description='Generate a TCP flow schedule csv file.')
    parser.add_argument('--start_id', action="store", dest="start_id", type=int)
    parser.add_argument('--end_id', action="store", dest="end_id", type=int)
    parser.add_argument('--duration_s', action="store", dest="duration_s", default=10, type=int)
    parser.add_argument('--expected_flows_per_s', action="store", dest="expected_flows_per_s", default=100, type=int)
    parser.add_argument('-n', action="store", dest="n_flows", default=-1, type=int)
    parser.add_argument('--is_unique', action="store", dest="is_unique", default=False, type=bool)
    parser.add_argument('--n_bg_traffic', action="store", dest='n_bg_traffic', default=0, type=int)
    args = parser.parse_args()

    generate_tcp_schedule(
        args.start_id,
        args.end_id,
        args.duration_s,
        args.expected_flows_per_s,
        args.n_flows,
    )
