step 1: generate topology：
simulation start time:
    In ```step_1_starlink_generation.py```, specify the simulation start time in the variable ```SIM_START_TIME```.
    Example of simulation start time: ```'2000-01-01 00:00:00.000'```
    If you want to use Hypatia's default (use epoch as the simulation start time), assign ```None``` to ```SIM_START_TIME```.

with isl:
    python step_1_starlink_generation.py 200 1000 isls_plus_grid ground_stations_top_100 algorithm_free_one_only_over_isls ${num_threads}

bent-pipe:
    python step_1_starlink_generation.py 200 1000 isls_none ground_stations_paris_moscow_grid algorithm_free_one_only_gs_relays ${num_threads}
    python step_1_starlink_generation.py 5 1000 isls_none ground_stations_top_100 algorithm_free_one_only_gs_relays 4

load supplemental TLEs:
    Use ```convert_to_hypatia.py``` to convert the supplemental TLEs to Hypatia's TLE file format.
    The converted TLE file is located at the same folder as ```tles.txt```.
    Copy and paste the converted tle to the ```tles.txt``` in ```gen_data``` folder.
    Comment out the TLEs generation code in ```main_helper.calculate```.
    Comment out the same epoch restriction check in ```read_tles.py```
    In ```step_1_starlink_generation.py```, change ```NUM_ORBS``` to ```1```, 
    and change ```NUM_SATS_PER_ORB``` to number of satellites.
    Specify the simulation start time ```SIM_START_TIME``` in ```step_1_starlink_generation.py```.
    Make sure ```SIM_START_TIME``` is after the epoch of all satellites. For example, after one day.

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
