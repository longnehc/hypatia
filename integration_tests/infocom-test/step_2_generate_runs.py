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

import argparse
import exputil
import random
from tcp import generate_tcp_schedule
from util import util


try:
    from .run_list import *
except (ImportError, SystemError):
    from run_list import *

local_shell = exputil.LocalShell()

local_shell.remove_force_recursive("temp/runs")
local_shell.remove_force_recursive("temp/pdf")
local_shell.remove_force_recursive("temp/data")

# TCP runs
for run in get_tcp_run_list():

    # Prepare run directory
    run_dir = "temp/runs/" + run["name"]
    local_shell.remove_force_recursive(run_dir)
    local_shell.make_full_dir(run_dir)

    # config_ns3.properties
    local_shell.copy_file("templates/template_tcp_a_b_config_ns3.properties", run_dir + "/config_ns3.properties")
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SATELLITE-NETWORK]", str(run["satellite_network"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE]", str(run["dynamic_state"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE-UPDATE-INTERVAL-NS]", str(run["dynamic_state_update_interval_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SIMULATION-END-TIME-NS]", str(run["simulation_end_time_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ENABLE-ISL-UTILIZATION-TRACKING]", "true" if run["enable_isl_utilization_tracking"] else "false")
    if run["enable_isl_utilization_tracking"]:
        local_shell.sed_replace_in_file_plain(
            run_dir + "/config_ns3.properties",
            "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]",
            "isl_utilization_tracking_interval_ns=" + str(run["isl_utilization_tracking_interval_ns"])
        )
    else:
        local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                              "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]", "")
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[TCP-SOCKET-TYPE]", str(run["tcp_socket_type"]))

    # Generate TCP flows
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_ms_flows', action="store", dest="n_ms_flows", type=int, default=100)
    parser.add_argument('--n_bg_flows', action="store", dest="n_bg_flows", type=int, default=200)
    args = parser.parse_args()

    gen_data_dir = "temp/gen_data/" + run['satellite_network']
    num_sats = util.count_sat_in_tles(gen_data_dir + "/tles.txt")
    num_gs = util.count_gs_in_file(gen_data_dir + '/ground_stations.txt')
    ms_flow_endpoints, ms_flow_ids = generate_tcp_schedule(
        start_id=num_sats,
        end_id=num_sats + num_gs - 1,
        duration_seconds=int(run['simulation_end_time_ns'] / 1000 / 1000 / 1000),
        n_ms_flows=args.n_ms_flows,
        n_bg_flows=args.n_bg_flows,
        is_unique=True,
        output_dir="temp/runs/" + get_tcp_run_list()[0]["name"],
        gs_path=gen_data_dir + "/ground_stations.txt",
    )

    # enable ping and tcp run at the same time
    ping_pairs = ms_flow_endpoints  # Use the same end-points as TCP flows
    with open(run_dir + "/config_ns3.properties", 'a') as f:
        f.write('tcp_flow_enable_logging_for_tcp_flow_ids=set(')
        for i in range(len(ms_flow_ids)):
            f.write(str(ms_flow_ids[i]))
            if i != len(ms_flow_ids)-1:
                f.write(',')    
        f.write(')\n')
        f.write('pingmesh_endpoint_pairs=set(')
        for i in range(len(ping_pairs)):
            f.write( str(ping_pairs[i][0]) + '->' + str(ping_pairs[i][1]) )
            if i != len(ping_pairs) - 1:
                f.write(',')
        f.write(')')
    print('100 ping pairs are generated with the same TCP end-point pairs at {}/config_ns3.properties.'
          .format(run_dir))

# Print finish
print("Success: generated ns-3 tcp runs")

# Ping runs
for run in get_pings_run_list():

    # Prepare run directory
    run_dir = "temp/runs/" + run["name"]
    local_shell.remove_force_recursive(run_dir)
    local_shell.make_full_dir(run_dir)

    # config_ns3.properties
    local_shell.copy_file("templates/template_pings_a_b_config_ns3.properties", run_dir + "/config_ns3.properties")
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SATELLITE-NETWORK]", str(run["satellite_network"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE]", str(run["dynamic_state"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE-UPDATE-INTERVAL-NS]", str(run["dynamic_state_update_interval_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SIMULATION-END-TIME-NS]", str(run["simulation_end_time_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ENABLE-ISL-UTILIZATION-TRACKING]", "true" if run["enable_isl_utilization_tracking"] else "false")
    if run["enable_isl_utilization_tracking"]:
        local_shell.sed_replace_in_file_plain(
            run_dir + "/config_ns3.properties",
            "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]",
            "isl_utilization_tracking_interval_ns=" + str(run["isl_utilization_tracking_interval_ns"])
        )
    else:
        local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                              "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]", "")
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[PINGMESH-INTERVAL-NS]", str(run["pingmesh_interval_ns"]))
    ping_pairs = []
    for i in range(0, 77):
        for j in range(0, 77):
            if i != j: 
                ping_pairs.append([i,j]) 
    index_list = random.sample(range(0, len(ping_pairs)), 100)
    for i in range(len(index_list)):
        pass
        #print(str(ping_pairs[index_list[i]][0] + 22 * 72) + '->' +  str(ping_pairs[index_list[i]][1] + 22 * 72))
    with open(run_dir + "/config_ns3.properties", 'a') as f:
        f.write('pingmesh_endpoint_pairs=set(')
        for i in range(len(index_list)):
            f.write(str(ping_pairs[index_list[i]][0] + 22 * 72) + '->' +  str(ping_pairs[index_list[i]][1] + 22 * 72))
            if i != len(index_list) - 1:
                f.write(',')
        f.write(')')
    '''
    with open(run_dir + "/config_ns3.properties", 'a') as f:
        f.write('pingmesh_endpoint_pairs=set(')
        for i in range(0, 77):
            for j in range(0, 77):
                if i < j:
                    f.write(str(22 * 72 + i)+'->'+str(22 * 72 + j))
                    if i == 75 and j == 76:
                        pass
                    else:
                        f.write(',')
        f.write(')')
    '''
    '''
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[FROM]", str(run["from_id"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[TO]", str(run["to_id"]))
    '''
# Print finish
print("Success: generated ns-3 ping runs")


# Udp runs
for run in get_udp_run_list():
    # Prepare run directory
    run_dir = "temp/runs/" + run["name"]
    local_shell.remove_force_recursive(run_dir)
    local_shell.make_full_dir(run_dir)

    # config_ns3.properties
    local_shell.copy_file("templates/template_config_ns3_udp.properties", run_dir + "/config_ns3.properties")
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SATELLITE-NETWORK]", str(run["satellite_network"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE]", str(run["dynamic_state"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[DYNAMIC-STATE-UPDATE-INTERVAL-NS]", str(run["dynamic_state_update_interval_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[SIMULATION-END-TIME-NS]", str(run["simulation_end_time_ns"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-DATA-RATE-MEGABIT-PER-S]", str(run["data_rate_megabit_per_s"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ISL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_isl_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[GSL-MAX-QUEUE-SIZE-PKTS]", str(run["queue_size_gsl_pkt"]))
    local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                          "[ENABLE-ISL-UTILIZATION-TRACKING]", "true" if run["enable_isl_utilization_tracking"] else "false")
    if run["enable_isl_utilization_tracking"]:
        local_shell.sed_replace_in_file_plain(
            run_dir + "/config_ns3.properties",
            "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]",
            "isl_utilization_tracking_interval_ns=" + str(run["isl_utilization_tracking_interval_ns"])
        )
    else:
        local_shell.sed_replace_in_file_plain(run_dir + "/config_ns3.properties",
                                              "[ISL-UTILIZATION-TRACKING-INTERVAL-NS-COMPLETE]", "")

    with open(run_dir + "/udp_burst_schedule.csv", "w+") as f_out:
        f_out.write("%d,%d,%d,%.10f,%d,%d,,\n" % (
                            0,
                            run["from_id"],  #src
                            run["to_id"],  #dst
                            run["data_rate_megabit_per_s"],
                            0,
                            1000000000000
                        ))

# Print finish
print("Success: generated ns-3 udp runs")