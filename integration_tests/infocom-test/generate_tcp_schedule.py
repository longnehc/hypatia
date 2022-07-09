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


# https://github.com/snkas/networkload/blob/master/example/example.py


def generate_tcp_schedule(
        start_id,
        end_id,
        duration_seconds,
        n_ms_flows,
        n_bg_flows,
        is_unique,
):
    """
    @param start_id: the first id of the end-point id range
    @param end_id: the last id of the end-point id range
    @param duration_seconds: range of flow start time from 0 ns
    @param n_ms_flows: number of measurement flows that we want to log during simulation.
    @param n_bg_flows: number of background flows to simulate congestion, and we do not want to log them.
    @param is_unique: indicate whether of the measurement flows have unique end-point pairs.
    @return: end-point pairs and flow ids for the measurement flows
    """
    servers = set(range(start_id, end_id + 1))
    list_start_time_ns = generate_start_time_ns(duration_seconds, n_ms_flows + n_bg_flows)
    num_starts = len(list_start_time_ns)
    list_from_to = generate_from_to_list(num_starts, servers, is_unique)
    list_flow_size_byte = generate_flow_size_in_byte(num_starts)

    output_filename = "temp/runs/" + get_tcp_run_list()[0]["name"] + "/schedule.csv"
    write_tcp_schedule(num_starts, list_from_to, list_flow_size_byte, list_start_time_ns, output_filename)

    print("{} TCP measurement flows and {} TCP background flows are generated at {}."
          .format(n_ms_flows, n_bg_flows, output_filename))

    return list_from_to


def generate_start_time_ns(duration_seconds, n_flows):
    duration_ns = seconds_in_ns(duration_seconds)
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
