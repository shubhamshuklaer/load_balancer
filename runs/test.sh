#!/bin/bash -i

num_procs=2
num_tkns=20
delay=5
is_hypercube=""
use_ip=false
self_loop_fraction=""

# http://stackoverflow.com/questions/402377/using-getopts-in-bash-shell-script-to-get-long-and-short-command-line-options
# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":p:t:cis:" opt; do
  case $opt in
    p)
      num_procs=$OPTARG
      ;;
    t)
      num_tkns=$OPTARG
      ;;
    i)
      use_ip=true
      ;;
    s)
      self_loop_fraction="--self_loop_fraction "$OPTARG
      ;;
    c)
      is_hypercube="--hypercube"
      num_procs=$((2 ** $num_procs))
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

echo "Num hosts: $num_procs"
echo "Num tkns: $num_tkns"

# load_balancer_build is an alias I use for doing docker build dir_name, with
# proxy settings
load_balancer_build

# So that ip address allocation starts from begining
# So that I can send tokens to 172.17.0.2
sudo systemctl restart docker

sleep $delay

for i in `seq 1 $(($num_procs + 1))`
do
    # http://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and
    if [ $i -ne $(($num_procs + 1)) ]
    then
        xterm -e docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/host.py `echo $self_loop_fraction` `echo $is_hypercube` &
    else
        # We need 172.17.0.2 as a host not log_server
        sleep $delay
        # To disable X server access control use xhost + , clients can connect
        # from any host To go to original use "xhost -"
        xhost +
        # Running GUI inside docker
        # https://blog.jessfraz.com/post/docker-containers-on-the-desktop/
        # http://stackoverflow.com/questions/25281992/alternatives-to-ssh-x11-forwarding-for-docker-containers
        # Mayavi used in showing 3d graph use accelerated graphics so /dev/dri is required
        # Without /dev/dri you get the following error
        # libGL error: failed to open drm device: No such file or directory
        # libGL error: failed to load driver: i965

        xterm -e docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=unix$DISPLAY --device /dev/dri -P shubhamshuklaerssss/load_balancer python -u load_balancer/host.py --log_server &
    fi

    # http://www.thegeekstuff.com/2010/06/bash-array-tutorial/
    pids[$(($i - 1))]=$!

    # This delay is important cause if we don't give any delay then its not
    # certain that the program which I start in background first will get
    # container first. In command I am assuming the Ip of containers
    # according to order of code, but actually the ip is according to which
    # gets the container first

    # You will need delay between last loop and client one too.
done

sleep $(( 2 * $delay ))
echo "Pids ${pids[@]}"
ip_flag=""
# http://stackoverflow.com/questions/3810709/how-to-evaluate-a-boolean-variable-in-an-if-block-in-bash
if $use_ip
then
    # 172.17.0.1 is for host
    ip_flag="--ip 172.17.0.2"
fi
docker run -P shubhamshuklaerssss/load_balancer python -u load_balancer/client.py $(echo $ip_flag) -s -c load_balancer/clients/test.py -w load_balancer/workers/square.py -- -l $(echo $num_tkns)
# No need to kill the ${pids} as they are automatically killed when we do ctrl+c on the script
xhost -
