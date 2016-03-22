#!/usr/bin/env python

# We are using seperate port for solved_tokens so that we can run both client
# and host on the same ip, we cannot run 2 serivces on same port.
solved_token_serv_port=8008
token_serv_port=8007

# Actually till 8192 bytes (8KB) will work. But lets not push the boundries.
udp_max_data_size=8000
