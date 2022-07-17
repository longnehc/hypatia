def count_successful_flows(filepath):
    total = 0
    counts = 0
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            if split[8] == 'YES':
                counts += 1
    print('{:.2f}% YES flows, {} YES flows out of {} total flows.'
          .format(counts / total * 100.0, counts, total))
    return counts


def output_successful_flow_end_point_pairs(filepath, output_path):
    """
    Go through the tcp_flows.csv and output the success flows
    end-point pairs to a file.
    """
    # Read flow file
    total = 0
    pairs_set = set()
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            if split[8] == 'YES':
                pairs_set.add(
                    (split[1], split[2])
                )
    # Write successful end-point pairs
    pairs_list = list(pairs_set)
    pairs_list.sort()
    with open(output_path, 'w') as f:
        for p in pairs_list:
            f.write('{}, {}\n'.format(p[0], p[1]))

    print('{:.2f}% YES flows, {} YES flows out of {} total flows.'
          .format(len(pairs_list) / total * 100.0, len(pairs_list), total))


if __name__ == '__main__':
    output_successful_flow_end_point_pairs(
        filepath='../temp/runs/starlink_550_isls_none_tcp/logs_ns3/tcp_flows.csv',
        output_path='../ep_pairs_cache.txt',
    )
