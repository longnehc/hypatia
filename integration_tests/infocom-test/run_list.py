# The MIT License (MIT)
#
# Copyright (c) 2020 ETH Zurich
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from util import util

full_satellite_network_isls = "starlink_550_isls_plus_grid_infocom_test"
description_file_path = "temp/gen_data/" + full_satellite_network_isls + "/description.txt"

# Core values
dynamic_state_update_interval_ms = int(util.get_config_value(description_file_path, 'simulation_interval_ms'))
simulation_end_time_s = int(util.get_config_value(description_file_path, 'simulation_end_time_s'))
pingmesh_interval_ns = 1 * 1000 * 1000 * 1000                   # A ping every 1s
enable_isl_utilization_tracking = True                          # Enable utilization tracking
isl_utilization_tracking_interval_ns = 1 * 1000 * 1000 * 1000   # 1 second utilization intervals

# Derivatives
dynamic_state_update_interval_ns = dynamic_state_update_interval_ms * 1000 * 1000
# simulation_end_time_ns = simulation_end_time_s * 1000 * 1000 * 1000
simulation_end_time_ns = 300 * 1000 * 1000 * 1000
# dynamic_state = "dynamic_state_" + str(dynamic_state_update_interval_ms) + "ms_for_" + str(simulation_end_time_s) + "s"

# Use the fixed output directory name
dynamic_state = "dynamic_state_infocom_test"

# Chosen pairs:
# > Manila (17) to Dalian (18)
#full_satellite_network_isls="starlink_550_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls"

# Sami's scr-dst pair:
scr_dst_pairs = [
                 ([100], [104]),    # Cape Town
                 ([100], [4]),     # Mumbai
                 ([100], [63]),    # Singapore
                 ([100], [84]),    # Sydney
                 ([100], [0]),     # Tokyo
                 ([100], [27]),     # London
                 ([100], [105]),     # Bahrain / Ad-Dammam
                 ([100], [3]),     # Sao Paulo
                 ([100], [103]),     # California / San-Francisco
                 ]

# scr_dst_pairs = [
#                  ([100], [101]),
#                  ([100], [60]),
#                  ([100], [102]),
#                  ([100], [103]),
#                  ([100], [56]),
#                  ([100], [74]),
#                  ([100], [50]),
#                  ([100], [84]),
#                  ([100], [27]),
#                  ([100], [6]),
#                  ([100], [0])
#                  ]

# scr_dst_pairs = [
#                  ([100], [101, 60, 102, 103, 56, 74, 50, 84, 27, 6, 0]),
#                  ]


# scr_dst_pairs = [
#                  ([100], [101]),
#                  ]


chosen_pairs = []
for sd in scr_dst_pairs:
    chosen_pairs.append(("starlink_550_isls_plus_grid_{}_{}".format(sd[0][0], sd[1][0]), 
                         sd[0], sd[1], "TcpNewReno", full_satellite_network_isls))

def get_tcp_run_list():
    run_list = []
    for p in chosen_pairs:
        run_list += [
            {
                "name": p[0] + "_tcp",
                "satellite_network": p[4],
                "dynamic_state": dynamic_state,
                "dynamic_state_update_interval_ns": dynamic_state_update_interval_ns,
                "simulation_end_time_ns": simulation_end_time_ns,
                "data_rate_megabit_per_s": 300.0,
                "queue_size_pkt": 100,
                "enable_isl_utilization_tracking": enable_isl_utilization_tracking,
                "isl_utilization_tracking_interval_ns": isl_utilization_tracking_interval_ns,
                "from_id": p[1],
                "to_id": p[2],
                "tcp_socket_type": p[3],
                "n_bg_flows": 200,      # Test 1000 or larger
                "pingmesh_interval_ns": pingmesh_interval_ns,
            },
        ]
    return run_list

def get_pings_run_list():
    run_list = []
    for p in chosen_pairs:
        run_list += [
            {
                "name": p[0] +  "_pings",
                "satellite_network": p[4],
                "dynamic_state": dynamic_state,
                "dynamic_state_update_interval_ns": dynamic_state_update_interval_ns,
                "simulation_end_time_ns": simulation_end_time_ns,
                "data_rate_megabit_per_s": 10000.0,
                "queue_size_pkt": 100000, 
                "enable_isl_utilization_tracking": enable_isl_utilization_tracking,
                "isl_utilization_tracking_interval_ns": isl_utilization_tracking_interval_ns,
                "from_id": p[1],
                "to_id": p[2],
                "pingmesh_interval_ns": pingmesh_interval_ns,
            }
        ]

    return run_list

def get_udp_run_list():
    run_list = []
    for p in chosen_pairs:
        run_list += [
            {
                "name": p[0] + "_udp",
                "satellite_network": p[4],
                "dynamic_state": dynamic_state,
                "dynamic_state_update_interval_ns": dynamic_state_update_interval_ns,
                "simulation_end_time_ns": simulation_end_time_ns,
                "data_rate_megabit_per_s": 1.0, 
                "queue_size_isl_pkt":10,
                "queue_size_gsl_pkt":10,
                "enable_isl_utilization_tracking": enable_isl_utilization_tracking,
                "isl_utilization_tracking_interval_ns": isl_utilization_tracking_interval_ns,
                "from_id": p[1],
                "to_id": p[2],
                "pingmesh_interval_ns": pingmesh_interval_ns,
            }
        ]

    return run_list