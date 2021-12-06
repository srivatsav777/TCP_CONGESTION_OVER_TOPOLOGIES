# TCP Congestion Control Algorithms Performance Over different Topologies

## Environment Setup

1. Select/emulate a Linux machine
2. Install mininet and dependencies
3. Install Bird
4. Install IPerf and dependencies
5. Install Xterm or other visualizing tools
6. Enable X11 forwarding
7. Enable BBR algorithm in the OS level


## Topologies
1. Star Topology
2. Ring Topology
3. Dumbell Topology

# Steps to run the experiment

1. After mininet is installed on your system run,

    python dumbell.py
        or
    python star.py
        or
    python ring_topology.py

    to setup the respective topologies

2. After setting up the topology, you will enter the mininet terminal where you can run 

    pingall

    to check whether all the hosts all reachable to all other hosts or not.

3. Open the xterm terminals for the hosts, (Here is an example for dumbell topology)

    xterm h1 h1 h2 h5

    opens 4 terminals 2 for h1 , 1 for h2 and other for h5

4. In the h5 terminal, run two simple servers in the background using the iperf3 command

    iperf3 -s -p 5510 -i 1 &
    iperf3 -s -p 5520 -i 1 &

5. In the h1 terminal, open a client connection with the iperf3,

    iperf3 -c 147.0.1.1 -p 5510 -t 40 -C <reno|cubic|bbr> &

    In the other h2 terminal run the bash script

    bash ss-output.sh 147.0.1.1 h1.txt h1.csv

    hit ctrl+c to exit from the script after the iperf3 test is done

    20 seconds from the start of iperf3 test on h1, run a client connection on h2

    iperf3 -c 147.0.1.1 -p 5520 -t 20 -C <reno|cubic|bbr> &


6. Once the tests are completed, use the plot.py to convert the csv generated in the above to plots

    python plot.py h1.csv

    python plot_rtt.py h1.csv

One graph with ts vs CWND and another graph ts vs rtt are plotted. 
