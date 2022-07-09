rm -rf dataset
killall screen
mkdir dataset
count=10
i=0
while(($i < $count))
do
    echo "The $i-th round starts at `date`"
    mkdir dataset/data$i
    dir=dataset/data$i
    python step_2_generate_runs.py
    python step_3_tcp_run.py
    cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_delay.csv $dir/ 
    cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_dev_queue_length.csv $dir/ 
    cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/traffic.csv $dir/ 
    cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/tcp-results.csv $dir/
    cp temp/runs/starlink_550_isls_none_tcp/ms_flow_ids.txt $dir/
    cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/ping-results.csv $dir/ 
    let "i++"
    echo "The $i-th round ends at `date`"
done