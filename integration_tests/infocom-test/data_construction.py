import sys
sys.path.append("../../satgenpy")
import satgen

number_of_gs=77
simulation_time=5

def add_latitude_longitude():
    ground_stations = satgen.read_ground_stations_basic('input_data/ground_stations_paris_moscow_grid.basic.txt')
    with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/traffic.csv', 'r') as f_in:
        with open('traffic.csv', "w+") as f_out:
            for line in f_in:
                split = line.split(',')
                src = int(split[0]) - 72 * 22
                dst = int(split[1]) - 72 * 22
                src_latitude = ground_stations[src]["latitude_degrees_str"]
                src_longitude = ground_stations[src]["longitude_degrees_str"]
                dst_latitude = ground_stations[dst]["latitude_degrees_str"]
                dst_longitude = ground_stations[dst]["longitude_degrees_str"]
                f_out.write("%s,%s,%s,%s,%s,%s,%s,%s" % (
                    split[0],
                    split[1],
                    src_latitude,
                    src_longitude,
                    dst_latitude,
                    dst_longitude,
                    split[2],
                    split[3]
                    )
                )    


def build_label():
    tcp_results_full_list = []
    tcp_results_id = []
    with open('temp/runs/starlink_550_isls_none_tcp/ms_flow_ids.txt', 'r') as f_in:
        for line in f_in:
            tcp_results_id.append(int(line))
    with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/tcp-results.csv', 'r') as f_in:
        count = 0
        for line in f_in:
            if count in tcp_results_id:
                line = line.replace('\n','')
                split = line.split(',')
                tcp_result = {
                    "src": split[0],
                    "dst": split[1],
                    "fct": split[2],
                    "rate": split[3]
                }
                tcp_results_full_list.append(tcp_result)
            count += 1
    #print(len(tcp_results_full_list))
    with open('label.csv', 'w+') as f_out:
        with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/ping-results.csv', 'r') as f:
            for line in f:
                split = line.split(',')
                if len(split) != 5:
                    raise AssertionError("The results format of ping is wrong")
                src = split[0]
                dst = split[1]
                for tcp_result in tcp_results_full_list:
                    find = False
                    if tcp_result["src"] == src and tcp_result["dst"] == dst:
                         f_out.write("%s,%s,%s,%s,%s,%s,%s" % (
                            tcp_result["src"],
                            tcp_result["dst"],
                            tcp_result["fct"],
                            tcp_result["rate"],
                            split[2],
                            split[3],
                            split[4]
                            )
                        ) 
                    find = True
                    if not find:
                        raise AssertionError("Failed to find a tcp flow")
 


def build_node_info():
    ground_stations = satgen.read_ground_stations_basic('input_data/ground_stations_paris_moscow_grid.basic.txt')
    with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_dev_queue_length.csv', 'r') as f_in:
        with open('node_info.csv', 'w+') as f_out:
            cnt = 0
            for line in f_in:
                temp_line = line
                split = temp_line.split(',')
                line = line.replace('\n','')
                if cnt < 72 * 22:
                    latitude = '0'
                    longtitude = '0'
                else:
                    node_id = int(split[0]) - 72 * 22
                    latitude = ground_stations[node_id]["latitude_degrees_str"]
                    longtitude = ground_stations[node_id]["longitude_degrees_str"]
                f_out.write("%s,%s,%s\n" % (
                            line,
                            latitude,
                            longtitude
                            )
                        ) 
                cnt += 1
            

def build_edge_info():
    with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_delay.csv', 'r') as f_in:
        with open('edge_info.csv', 'w+') as f_out:
            for line in f_in:
                line = line.replace('\n','')
                f_out.write("%s,%s,%s\n" % (
                    line,
                    '0',
                    '0'
                    )
                )
    traffic_list = [] 
    tcp_results_id = []
    with open('temp/runs/starlink_550_isls_none_tcp/ms_flow_ids.txt', 'r') as f_in:
        for line in f_in:
            tcp_results_id.append(int(line))
    with open('temp/runs/starlink_550_isls_none_tcp/logs_ns3/traffic.csv', 'r') as f_in:
        count = 0
        for line in f_in:
            if count in tcp_results_id:
                line = line.replace('\n','')
                split = line.split(',')
                traffic_info = {
                    "src": split[0],
                    "dst": split[1],
                    "burst_size": split[2],
                    "start_time": split[3]
                }
                traffic_list.append(traffic_info)
            count += 1
 
    print("The number of traced traffic flow is", len(traffic_list))
    with open('edge_info.csv', 'a+') as f_out:
        count = 0
        for i in range(number_of_gs):
            for j in range(number_of_gs):
                if i != j:
                    src = i + 72 * 22
                    dst = j + 72 * 22
                    delay = 10
                    burst_size = '0'
                    start_time = '0'
                    sample_delay = ''
                    for traffic in traffic_list:
                        if src == int(traffic["src"]) and dst == int(traffic["dst"]):
                            burst_size = traffic["burst_size"]
                            start_time = traffic["start_time"]
                            count += 1
                    for k in range(simulation_time):
                        sample_delay += str(delay)
                        if k != simulation_time - 1:
                            sample_delay+=','
                    f_out.write("%s,%s,%s,%s,%s\n" % (
                        str(src),
                        str(dst),
                        sample_delay,
                        burst_size,
                        start_time
                        )
                    ) 
    print("The number of flows in edge_info.csv is", count)

if __name__ == '__main__':
    build_label()   
    # add_latitude_longitude()
    build_node_info()
    build_edge_info()