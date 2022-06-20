step 1: generate topology：
with isl:
    python step_1_starlink_generation.py 200 1000 isls_plus_grid ground_stations_top_100 algorithm_free_one_only_over_isls ${num_threads}

bent-pipe:
    python step_1_starlink_generation.py 200 1000 isls_none ground_stations_paris_moscow_grid algorithm_free_one_only_gs_relays ${num_threads}


step 2: generate conig_ns3.properties
    python step_2_generate_runs.py

Expected outputs:
    Success: generated ns-3 tcp runs
    Success: generated ns-3 ping runs
    Success: generated ns-3 udp runs

Flow generation in step 2:
    TCP:
        step 2.1: generate TCP flows：
        python generate_tcp_schedule.py --start_id 1000 --end_id 1200 --duration_s 120 --expected_flows_per_s 100

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