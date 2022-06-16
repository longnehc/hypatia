import exputil
import networkload
import random


# Set up random seeds
random.seed(123456789)
SEED_START_TIMES = random.randint(0, 100000000)
SEED_FROM_TO = random.randint(0, 100000000)
SEED_FLOW_SIZE = random.randint(0, 100000000)


def generate_tcp_schedule(start_id, end_id):
    """
    https://github.com/snkas/networkload/blob/master/example/example.py
    """
    # A set of server IDs
    servers = set(range(start_id, end_id))

    # Traffic start time in ns
    duration_ns = seconds_in_ns(10)
    expected_flows_per_s = 100
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
    generate_tcp_schedule(100, 200)
