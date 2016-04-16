# FROM python was causing problems it has linked python to python3 but while
# installing things using apt-get install python-matplotlib it was python2
# So installations from pip(pip3) and apt-get were not matching
FROM ubuntu
MAINTAINER Shubham Shukla

# RUN pip install twisted networkx
ADD apt.conf /etc/apt/apt.conf
RUN apt-get update

# RUN pip install twisted networkx matplotlib ipaddress

# The pip install matplotlib doesn't provide all dependensies like gtk for
# matplotlib
RUN apt-get install -y python python-pip python-matplotlib python-twisted python-networkx python-qt4 libqt4-dev
RUN pip install ipaddress


RUN mkdir load_balancer
ADD . load_balancer/
# No need to EXPOSE here if we are EXPOSING all ports using -P in docker run
# command.
# EXPOSE 8007 8008 8009
