import argparse
import exputil
import networkload
import random


# Set up random seeds
random.seed(123456789)
SEED_START_TIMES = random.randint(0, 100000000)
SEED_FROM_TO = random.randint(0, 100000000)
SEED_FLOW_SIZE = random.randint(0, 100000000)


def generate_tcp_schedule(
        start_id, 
        end_id,
        duration_seconds,
        expected_flows_per_s,
    ):
    """
    https://github.com/snkas/networkload/blob/master/example/example.py
    """
    # A set of server IDs
    servers = set(range(start_id, end_id))

    # Traffic start time in ns
    duration_ns = seconds_in_ns(duration_seconds)
    list_start_time_ns = networkload.draw_poisson_inter_arrival_gap_start_times_ns(duration_ns, expected_flows_per_s, SEED_START_TIMES)
    num_starts = len(list_start_time_ns)

    # Get (From, To) tuples for each start time
    list_from_to = networkload.draw_n_times_from_to_all_to_all(num_starts, servers, SEED_FROM_TO)

    # Flow sizes in byte
    list_flow_size_byte = list(
        round(x) for x in networkload.draw_n_times_from_cdf(num_starts, networkload.CDF_PFABRIC_WEB_SEARCH_BYTE, True, SEED_FLOW_SIZE)
    )

    # Write schedule to a csv file
    networkload.write_schedule(
        "schedule.csv",
        num_starts,
        list_from_to,
        list_flow_size_byte,
        list_start_time_ns
    )


def seconds_in_ns(seconds):
    return seconds * 1000 * 1000 * 1000


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a TCP flow schedule csv file.')
    parser.add_argument('--start_id', action="store", dest="start_id", type=int)
    parser.add_argument('--end_id', action="store", dest="end_id", type=int)
    parser.add_argument('--duration_s', action="store", dest="duration_s", default=10, type=int)
    parser.add_argument('--expected_flows_per_s', action="store", dest="expected_flows_per_s", default=100, type=int)
    args = parser.parse_args()

    generate_tcp_schedule(
        args.start_id,
        args.end_id,
        args.duration_s,
        args.expected_flows_per_s,
    )
