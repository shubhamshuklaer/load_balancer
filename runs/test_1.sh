#!/bin/bash

num_procs=2
if [ $# -eq 1 ]
then
    num_procs=$1
fi
echo "Num hosts: $num_procs"


# Example output '["172.17.0.2","172.17.0.3","172.17.0.4","172.17.0.5"]'
# THere is some problems with outer single quotes. From terminal we must give
# single quotes but in script it is causing problem. We need to remove the
# single quote for script
function get_neighbors(){
    str="["
    for j in `seq 1 $num_procs`
    do
        if [[ $j != $1 ]]
        then
            str="$str\"172.17.0.$j\","
        fi
    done
    str=$(echo $str | sed 's/,$//')
    str="$str]"
    echo $str
}


sudo lxc-start -n load_balancer_lab

# sshpass -p root ssh root@192.168.45.10 "service docker start"
sudo lxc-attach -n load_balancer_lab --clear-env -- service docker start
sudo lxc-attach -n load_balancer_lab --clear-env -- service ssh start

for i in `seq 1 $num_procs`
do
    echo $(get_neighbors $i )
    # Not using lxc-attach because otherwise we will have to enter sudo passwd
    # xterm -hold -e sshpass -p root ssh root@192.168.45.10 docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/host.py --neighbors $(get_neighbors $i ) &
    # http://askubuntu.com/questions/515198/how-to-run-terminal-as-root
    # -H will change to home folder to /root
    sudo -H xterm -hold -e lxc-attach -n load_balancer_lab --clear-env --  docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/host.py --neighbors $(get_neighbors $i ) &
done

echo "Hello"
sudo lxc-attach -n load_balancer_lab --clear-env -- docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/client.py --ip 172.17.0.1 -n 20

sudo lxc-stop -n load_balancer_lab
