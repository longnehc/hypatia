import argparse
import exputil
import networkload
import numpy as np
import random


# Set up random seeds
random.seed(123456789)
SEED_START_TIMES = random.randint(0, 100000000)
SEED_FROM_TO = random.randint(0, 100000000)
SEED_FLOW_SIZE = random.randint(0, 100000000)


def generate_udp_schedule(
        start_id, 
        end_id,
        target_rate_mbps,
        burst_duration_s,
        duration_seconds,
        expected_flows_per_s,
    ):
    """
    Different to the TCP flows, the UDP burst flow is has this burst duration attribute.
    https://github.com/snkas/networkload/blob/master/example/example.py
    """
    # A set of server IDs
    servers = set(range(start_id, end_id + 1))

    # Traffic start time in ns
    duration_ns = seconds_in_ns(duration_seconds)
    list_start_time_ns = networkload.draw_poisson_inter_arrival_gap_start_times_ns(duration_ns, expected_flows_per_s, SEED_START_TIMES)
    num_starts = len(list_start_time_ns)

    # Get (From, To) tuples for each start time
    list_from_to = networkload.draw_n_times_from_to_all_to_all(num_starts, servers, SEED_FROM_TO)

    # Target bit rate for the UDP flow in Mbps
    list_target_rate_mpbs = [target_rate_mbps] * num_starts

    # Burst duration for a UDP flow, using poisson distribution
    burst_duration_ns = seconds_in_ns(burst_duration_s)
    list_burst_duration_ns = np.random.poisson(burst_duration_ns, num_starts)

    # Write schedule to a csv file
    networkload.write_schedule(
        "udp_burst_schedule.csv",
        num_starts,
        list_from_to,
        list_target_rate_mpbs,
        list_start_time_ns,
        list_burst_duration_ns,  # UDP burst duration is written into file as list_extra_parameters
        [','] * num_starts,  # It requires 8 split values, so add a comma here as a hack
    )


def seconds_in_ns(seconds):
    return seconds * 1000 * 1000 * 1000


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a TCP flow schedule csv file.')
    parser.add_argument('--start_id', action="store", dest="start_id", type=int)
    parser.add_argument('--end_id', action="store", dest="end_id", type=int)
    parser.add_argument('--target_rate_mbps', action="store", dest="target_rate_mbps", default=10, type=float, 
                        help="the target bit rate for UDP flow in Mbps")
    parser.add_argument('--burst_duration_s', action="store", dest="burst_duration_s", default=10, type=int, 
                        help="the duration for a UDP burst to contitnue")
    parser.add_argument('--duration_s', action="store", dest="duration_s", default=10, type=int)
    parser.add_argument('--expected_flows_per_s', action="store", dest="expected_flows_per_s", default=100, type=int)
    args = parser.parse_args()

    generate_udp_schedule(
        args.start_id,
        args.end_id,
        args.target_rate_mbps,
        args.burst_duration_s,
        args.duration_s,
        args.expected_flows_per_s,
    )
