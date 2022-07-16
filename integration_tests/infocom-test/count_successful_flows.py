def count_successful_flows(filepath):
    total = 0
    counts = 0
    with open(filepath, 'r') as f:
        for line in f:
            total += 1
            split = line.strip().split(',')
            if split[8] == 'YES':
                counts += 1
    print('{:.2f} % YES flows, {} YES flows out of {} total flows.'
          .format(counts / total * 100.0, counts, total))
    return counts


if __name__ == '__main__':
    _counts = count_successful_flows(
        'temp/runs/starlink_550_isls_none_tcp/logs_ns3/tcp_flows.csv'
    )
