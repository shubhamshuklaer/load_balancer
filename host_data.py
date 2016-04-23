#!/usr/bin/env python
from threading import Lock
import os
import hashlib
import sys
import threading
import imp
import config
from token_client import run_token_client
from user_token import User_token,get_ip_address
import ipaddress
import copy
import networkx as nx
import subprocess
import shlex

neighbors=[]
tokens_list=[]
log_servers=[]
log_servers_lock=Lock()
tokens_list_lock=Lock()
workers_hash_lock=Lock()
neighbors_lock=Lock()
prev_index=0
is_hypercube=False
own_ip=get_ip_address()
if sys.version_info < (3, 0):
    own_ip=own_ip.decode('utf8')

# Ip assigned to with docker starts from 2, but grey code should start from 0
ip_sub=2

# For log server
plt=None
np=None
mlab=None
do_after=None
log=None
log_lock=None
pos=None
update_pos=False
xyz=None
scalars=None
v_list=None
vertex_map=None
LOG_SERVICE_BROADCAST_DELAY=10000
DRAW_LOG_DELAY=1000
workers_hash=dict()
workers_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)),"workers")


def get_rtt(ip_addr):
    cmd="ping -c2 -q "+ip_addr
    pint_out=""
    try:
        ping_out=subprocess.check_output(shlex.split(cmd))
    except subprocess.CalledProcessError:
        # Not reachable
        return 1000
    else:
        for line in ping_out.splitlines():
            line=str(line)
            if "rtt min/avg/max/mdev =" in line:
                line_split=line.split("=",2)
                avg_rtt=line_split[1].split("/")[1]
                return float(avg_rtt)

def get_fastest_neighbor():
    tmp_neighbors=[]
    with neighbors_lock:
        tmp_neighbors=copy.deepcopy(neighbors)
    if len(tmp_neighbors)==0:
        return None
    rtts=[]
    for neighbor in tmp_neighbors:
        rtts.append((neighbor,get_rtt(neighbor)))

    rtts=sorted(rtts,key=lambda tmp: tmp[1])
    print("Rtts: "+str(rtts))
    return rtts[0][0]

def log_service_broadcast():
    run_token_client("<broadcast>",[User_token("",User_token.LOG_SERVICE_BROADCAST)])
    do_after(LOG_SERVICE_BROADCAST_DELAY,log_service_broadcast)


def init_log():
    global log
    global log_lock
    log=nx.Graph()
    log_lock=Lock()
    # http://stackoverflow.com/questions/11990556/python-how-to-make-global-imports-from-a-function
    global plt
    global np
    global mlab
    global do_after

    #  import matplotlib.pyplot as plt
    import numpy as np
    from mayavi import mlab
    from pyface.timer.do_later import do_after

    mlab.figure(1)
    mlab.clf()
    do_after(DRAW_LOG_DELAY,draw_log)
    log_service_broadcast()
    do_after(LOG_SERVICE_BROADCAST_DELAY,log_service_broadcast)
    mlab.show()

# Update log will be called from a thread(from Token_server) but we cannot draw
# plt from thread so draw_log and update_log are seperate
def update_log(ip,num_tkns,ip_neighbors):
    if log_lock is None:
        # The token serv is started before log is initialized
        return
    with log_lock:
        global pos
        global update_pos
        # Adding existing nodes and edges doesn't do anything
        if ip not in log.node:
            update_pos=True
            log.add_node(ip)
        log.remove_edges_from(log.edges(ip))
        for neighbor in ip_neighbors:
            if neighbor not in log.node:
                update_pos=True
                log.add_node(neighbor)
            if 'num_tkns' not in log.node[neighbor]:
                log.node[neighbor]['num_tkns']=0
            log.add_edge(ip,neighbor)
        log.node[ip]['num_tkns']=num_tkns


# https://www.udacity.com/wiki/creating-network-graphs-with-python
# Draw 3d graphs with mayavi
def draw_log(graph_colormap='winter', bgcolor = (1, 1, 1),
                 node_size=0.005,
                 edge_color=(0.8, 0.8, 0.8), edge_size=0.001,
                 text_size=0.008, text_color=(0, 0, 0),pos_scale=0.3):
    with log_lock:
        global update_pos
        global pos
        global xyz
        global scalars
        global v_list
        global mlab
        global vertex_map
        if update_pos:
            update_pos=False
            # http://networkx.readthedocs.org/en/stable//reference/generated/networkx.drawing.layout.spring_layout.html
            pos=nx.spring_layout(log, dim=3,scale=pos_scale)
            v_list=[]
            pos_list=[]
            vertex_map=dict()
            for v,v_data in log.nodes(data=True):
                vertex_map[v]=len(v_list)
                v_list.append(v)
                pos_list.append(pos[v])
            xyz=np.array(pos_list)
            # the + 5 will add 5 to each element of array
            scalars=np.array(range(1,len(log.nodes())+1))+5

        if xyz == None:
            # The data has not yet been added
            return

        mlab.clf()
        pts = mlab.points3d(xyz[:,0], xyz[:,1], xyz[:,2], scalars, scale_factor=node_size, scale_mode='none', colormap=graph_colormap, resolution=20)
        label_list=[]
        loads=[]
        for v in v_list:
            label_list.append(v+"("+str(log.node[v]['num_tkns'])+")")
            loads.append(log.node[v]['num_tkns'])

        for i, (x, y, z) in enumerate(xyz):
            label = mlab.text3d(x, y, z, label_list[i],scale=text_size, color=text_color)

        tmp_edges=[]
        for a,b in log.edges():
            tmp_edges.append((vertex_map[a],vertex_map[b]))

        avg_discrepency=0.0
        max_discrepency=0
        count=0
        for i in range(len(loads)):
            for j in range(i+1,len(loads)):
                discrepency=abs(loads[i]-loads[j])
                avg_discrepency=avg_discrepency+discrepency
                max_discrepency=max(max_discrepency,discrepency)
                count=count+1

        if count!=0:
            avg_discrepency=avg_discrepency/count

        # The space in the end is put so that the last letter does not look cut at the end
        mlab.text(10*text_size,1-0.03,"Avg discrepency: "+"{0:.2f}".format(avg_discrepency)+'  ',width=text_size*30,color=text_color)
        mlab.text(10*text_size,1-0.08,"Max discrepency: "+str(max_discrepency)+'  ',width=text_size*30,color=text_color)

        pts.mlab_source.dataset.lines = np.array(tmp_edges)
        tube = mlab.pipeline.tube(pts, tube_radius=edge_size)
        mlab.pipeline.surface(tube, color=edge_color)
        do_after(DRAW_LOG_DELAY,draw_log)
        mlab.show()


def is_hypercube_neighbor(ip):
    # ipaddress.IPv4Address needs unicode(eg utf8) string
    # In python2 string is ascii and to convert it to unicode we have to do
    # some_str.decode('utf8') for unicode to ascii we have to do
    # some_str.encode('ascci')
    # Literal strings are unicode by default in Python3
    if sys.version_info < (3, 0):
        ip=ip.decode('utf8')

    own_ip_bin=bin(int(ipaddress.IPv4Address(own_ip)-ip_sub))
    ip_bin=bin(int(ipaddress.IPv4Address(ip)-ip_sub))
    num_diff=0
    for i in range(len(own_ip_bin)):
        if own_ip_bin[i] != ip_bin[i]:
            num_diff=num_diff+1
    if num_diff == 1:
        return True
    else:
        return False

def insert_log_server(ip):
    with log_servers_lock:
        if ip not in log_servers:
            log_servers.append(ip)

def send_log():
    data=dict()
    data["num_tokens"]=len(tokens_list)
    data["neighbors"]=neighbors
    tkn=User_token(data,User_token.LOG)
    with log_servers_lock:
        for ip in log_servers:
            run_token_client(ip,[tkn],config.log_serv_port)


def insert_neighbor(ip):
    if ip != get_ip_address():
        with neighbors_lock:
            if ip not in neighbors:
                neighbors.append(ip)


def broadcast_service():
    tkn=User_token("",User_token.SERVICE_BROADCAST)
    run_token_client("<broadcast>",[tkn])
    run_token_client("<broadcast>",[tkn],config.solved_token_serv_port)


def calc_file_hash(file_path):
    file_path=os.path.expanduser(file_path)
    if not os.path.exists(file_path):
        return None
    else:
        # http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file/3431835#3431835
        # I think block size is only so that we don't have to store the entire huge file in a string.
        # I don't think it has anythin to do with the library
        # https://docs.python.org/3/library/hashlib.html
        # Its written that Repeated calls are equivalent to a single call with
        # the concatenation of all the arguments: m.update(a); m.update(b) is
        # equivalent to m.update(a+b).
        blocksize=65536
        hasher=hashlib.sha256()
        with open(file_path,"r") as f:
            buf = f.read(blocksize)
            while len(buf) > 0:
                #  http://stackoverflow.com/questions/7585307/typeerror-unicode-objects-must-be-encoded-before-hashing
                hasher.update(buf.encode("utf-8"))
                buf = f.read(blocksize)
        return hasher.digest()

def insert_worker_hash(file_path):
    hash_val=calc_file_hash(file_path)
    with workers_hash_lock:
        workers_hash[hash_val]=file_path

def insert_worker(file_name,content):
    file_path=os.path.join(workers_dir,file_name)
    hasher=hashlib.sha256()
    hasher.update(content.encode("utf-8"))
    hash_val=hasher.digest()
    if hash_val in workers_hash:
        #  print("worker exists")
        return False

    with open(file_path,"w") as worker_file:
        worker_file.write(content)
    host_data.insert_worker_hash(file_path)
    return True

def send_worker_to_all(tkn):
    with neighbors_lock:
        for ip in neighbors:
            run_token_client(ip,[tkn])



def append_tokens(user_tokens):
    with tokens_list_lock:
        tokens_list.extend(user_tokens)

def print_tokens():
    with tokens_list_lock:
        print(str(len(tokens_list))+" : "+str(tokens_list))


def gen_all_hash():
    for file_name in os.listdir(workers_dir):
        split=os.path.splitext(file_name)
        # possiblility of generation of pyc
        if len(split)==2 and split[1] == ".py":
            file_path=os.path.join(workers_dir,file_name)
            workers_hash[calc_file_hash(file_path)]=file_path

def solve_data(tkn,worker_path):
    mod = imp.load_source("tmp_worker",worker_path)
    run_token_client(tkn.ip,[User_token(mod.solve(tkn.data),User_token.SOLVED)],config.solved_token_serv_port)

def solve_one_token():
    tmp_tkn=None
    with tokens_list_lock:
        if len(tokens_list) != 0:
            tmp_tkn=tokens_list.pop()
    if tmp_tkn != None:
        if tmp_tkn.worker_hash in workers_hash:
            # http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
            threading.Thread(target=solve_data,args=[tmp_tkn,workers_hash[tmp_tkn.worker_hash]]).start()
        else:
            with tokens_list_lock:
                tokens_list.append(tmp_tkn)
