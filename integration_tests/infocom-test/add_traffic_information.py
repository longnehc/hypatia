import sys
sys.path.append("../../satgenpy")
import satgen


def extend_ground_stations():
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

if __name__ == '__main__':
    extend_ground_stations()