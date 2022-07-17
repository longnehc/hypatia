rm -rf dataset
rm -f *.csv
killall screen
mkdir dataset
count=10
i=0
while(($i < $count))
do
    echo "The $i-th round starts at `date`"
    mkdir dataset/data$i
    dir=dataset/data$i
    python step_2_generate_runs.py --n_ms_flows 100 --n_bg_flows 1000
    python step_3_tcp_run.py
    python data_construction.py
    # cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_delay.csv $dir/
    # cp temp/runs/starlink_550_isls_none_tcp/logs_ns3/gsl_dev_queue_length.csv $dir/
    mv node_info.csv $dir/
    mv edge_info.csv $dir/
    mv label.csv $dir/
    let "i++"
    echo "The $i-th round ends at `date`"
done