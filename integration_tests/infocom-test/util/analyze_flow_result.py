def count_successful_flows(filepath):
    total = 0
    counts = 0
    unique_total_pairs = set()
    unique_yes_pairs = set()
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            unique_total_pairs.add((split[1], split[2]))
            if split[8] == 'YES':
                counts += 1
                unique_yes_pairs.add((split[1], split[2]))
    print('{:.2f}% YES flows, {} YES flows out of {} total flows.'
          .format(counts / total * 100.0, counts, total))
    print('{} unique yes pairs out of {} unique total pairs.'
          .format(len(unique_yes_pairs), len(unique_total_pairs)))
    return counts


def count_non_zero_progress_flows(filepath):
    total = 0
    counts = 0
    unique_total_pairs = set()
    unique_non_zero_pairs = set()
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            unique_total_pairs.add((split[1], split[2]))
            if int(split[7]) != 0:
                counts += 1
                unique_non_zero_pairs.add((split[1], split[2]))
    print('{:.2f}% non-zero progress flows, {} non-zero progress flows out of {} total flows.'
          .format(counts / total * 100.0, counts, total))
    print('{} unique non-zero progress pairs out of {} unique total pairs.'
          .format(len(unique_non_zero_pairs), len(unique_total_pairs)))
    return counts


def output_successful_flow_end_point_pairs(filepath, output_path):
    """
    Go through the tcp_flows.csv and output the success flows
    end-point pairs to a file.
    """
    # Read flow file
    total = 0
    yes_pairs_list = list()
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            if split[8] == 'YES':
                yes_pairs_list.append(
                    (split[1], split[2])
                )
    # Write successful end-point pairs
    yes_pairs_list.sort()
    with open(output_path, 'w') as f:
        for p in yes_pairs_list:
            f.write('{}, {}\n'.format(p[0], p[1]))


if __name__ == '__main__':
    tcp_csv_path = '../temp/runs/starlink_550_isls_none_tcp/logs_ns3/tcp_flows.csv'
    count_non_zero_progress_flows(tcp_csv_path)
    count_successful_flows(tcp_csv_path)
    output_successful_flow_end_point_pairs(
        filepath=tcp_csv_path,
        output_path='../ep_pairs_cache.txt',
    )
