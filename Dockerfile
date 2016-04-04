FROM python
MAINTAINER Shubham Shukla

RUN pip install twisted
RUN mkdir load_balancer
ADD . load_balancer/
EXPOSE 8007 8008 8009
