#!/bin/bash

num_procs=2
num_tkns=20
delay=10

if [ $# -eq 1 ]
then
    num_procs=$1
fi
if [ $# -eq 2 ]
then
    num_procs=$1
    num_tkns=$2
fi
echo "Num hosts: $num_procs"
echo "Num tkns: $num_tkns"

# So that ip address allocation starts from begining
# So that I can send tokens to 172.17.0.2
sudo systemctl restart docker

sleep $delay

for i in `seq 1 $num_procs`
do
    # http://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and
    xterm -e docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/host.py &

    # http://www.thegeekstuff.com/2010/06/bash-array-tutorial/
    pids[$(($i - 1))]=$!

    # This delay is important cause if we don't give any delay then its not
    # certain that the program which I start in background first will get
    # container first. In command I am assuming the Ip of containers
    # according to order of code, but actually the ip is according to which
    # gets the container first

    # You will need delay between last loop and client one too.
done

# This delay is higher so that by the time client is run everyone knows about their neighbors.
sleep $((2 * $delay))
echo "Pids ${pids[@]}"

# 172.17.0.1 is for host
docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/client.py --ip 172.17.0.2 -n $(echo $num_tkns) --file load_balancer/workers/square.py
