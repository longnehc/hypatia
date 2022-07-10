step 1: generate topology：
with isl:
    python step_1_starlink_generation.py 200 1000 isls_plus_grid ground_stations_top_100 algorithm_free_one_only_over_isls ${num_threads}

bent-pipe:
    python step_1_starlink_generation.py 200 1000 isls_none ground_stations_paris_moscow_grid algorithm_free_one_only_gs_relays ${num_threads}
    python step_1_starlink_generation.py 5 1000 isls_none ground_stations_top_100 algorithm_free_one_only_gs_relays 4


step 2: generate conig_ns3.properties
    python step_2_generate_runs.py

Expected outputs:
    Success: generated ns-3 tcp runs
    Success: generated ns-3 ping runs
    Success: generated ns-3 udp runs

Flow generation in step 2:
    TCP:
        step 2.1: generate TCP flows：
        python generate_tcp_schedule.py --start_id 1584 --end_id 1650 --duration_s 5 --expected_flows_per_s 10 -n 100

    PING:
        TODO

    UDP:
        step 2.3: generate UDP flows
        python generate_udp_schedule.py --start_id 1584 --end_id 1682 --duration_s 10 --expected_flows_per_s 10 --burst_duration_s 3 --target_rate_mbps 1
  

step3: run
TCP:
    python step_3_tcp_run.py

PING:
    python step_3_ping_run.py

UDP:
    python step_3_udp_run.py


===========
Log file:
    isl_delay.csv
    isl_dev_queue_length.csv
    gsl_delay.csv
    gsl_dev_queue_length.csv

logging location:
    ns3-sat-sim/simulator/scratch/main_satnet/main_satnet.cc
        Add scheduler:
        topology->CollectISLDeviceQueueLength();
        topology->CollectGSLDeviceQueueLength();
        topology->CollectISLDelay();
        topology->CollectGSLDelay();

        Writing log files:
        topology->GetISLDeviceQueueLength();
        topology->GetISLDelay();
        topology->GetGSLDeviceQueueLength();
        topology->GetGSLDelay();

===========
TLEs Visualization

Convert the supplemental TLEsto Hypatia's format using convert_to_hypatia_tles.py

In the visualization folder, run the script
    python visualize_tles.py --tle ../tles.txt

Open tles_visualization.html in the same folder to see the visualization

===========

other useful commands:
run ns3 with gdb
    ./waf --run="main_satnet --run_dir='../../integration_tests/infocom-test/temp/runs/starlink_550_isls_sat_one_17_to_18_with_TcpNewReno_at_10_Mbps'" --gdb

gdb add breakpoints:
（gdb）b ns3-sat-sim/simulator/contrib/basic-sim/model/apps/tcp-flow-send-application.cc:183

satgen based rtt/path analysis:
    step 1: generate topology
        ~/hypatia-master/paper/satellite_networks_state$ 
        python main_starlink_550.py 10 1000 isls_plus_grid ground_stations_top_100 algorithm_free_one_only_over_isls 8

    step 2: analysis rtt
        ~/hypatia-master/satgenpy$ 
        python -m satgen.post_analysis.main_analyze_rtt ../paper/satgenpy_analysis/data ../paper/satellite_networks_state/gen_data/starlink_550_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls 1000 10 > ../paper/satgenpy_analysis/data/command_logs/constellation_comp_rtt_starlink_1000ms_for_10s.log 2>&1

        ~/hypatia-master/satgenpy$ 
        python -m satgen.post_analysis.main_analyze_path ../paper/satgenpy_analysis/data ../paper/satellite_networks_state/gen_data/starlink_550_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls 1000 10 > ../paper/satgenpy_analysis/data/command_logs/constellation_comp_path_starlink_1000ms_for_10s.log 2>&1

        ~/hypatia-master/satgenpy$ 
        python -m satgen.post_analysis.main_analyze_time_step_path ../paper/satgenpy_analysis/data ../paper/satellite_networks_state/gen_data/starlink_550_isls_plus_grid_ground_stations_top_100_algorithm_free_one_only_over_isls 1000 10 > ../paper/satgenpy_analysis/data/command_logs/constellation_comp_time_step_path_starlink_1000ms_for_10s.log 2>&1

# Two-Line Element (TLE) Analysis

To generate a TLE analysis report, run:

```shell
python create_tle_reports.py
```

## Useful Online Resources for TLEs

### Online TLE Parser
https://sat-tle-parser.netlify.app/

This is an online TLE parser where you can paste the TLE directly to retrieve the information.

### Starlink Satellite List

https://orbit.ing-now.com/satellite/74171/2022-062ba/starlink-4171/

You can look up a Starlink satellite by name on this website, which shows the basic orbital information about the satellite, and an animation of the orbit on the map. 
===========
dataset format
gsl_delay.csv
[src_id, dst_id, gsl_delay_0, gsl_delay_1, ...]

gsl_delay_queue_length.csv
[device_id, interface_queue_length_0, interface_queue_length_1, ...]

ping-results.csv
[src_id, dst_id, min_rtt, avg_rtt, max_rtt]

tcp-results.csv
[src_id, dst_id, flow_completion_time_in_seconds, avg_rate]
 
 traffic.csv
[src_id, dst_id, burst_size, start_time] 


node_info.csv
[device_id, interface_queue_length_0, interface_queue_length_1, ..., latitude, longtitude]
if devide is satellite 
   latitude = 0, longtitude = 9
else:
   latitude = ground station latitude
   longtitude = ground station longtitude

edge_info.csv
[src_id, dst_id, gsl_delay_0, gsl_delay_1, ..., burst_size, start_time]
if edge is gsl:
   burst_size = 0, start_time =0
else:
   delay = 10
   burst_size = tcp burst size
   start time = tcp start time
   
label.csv
[src_id, dst_id, flow_completion_time_in_seconds, avg_rate, min_rtt, avg_rtt, max_rtt]

 
===========
generate dataset
nohup bash run.bash > run.log 2>&1 &

compress dataset
tar -zcvf dataset.tar.gz dataset