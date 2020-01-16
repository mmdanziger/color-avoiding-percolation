#!/usr/bin/python3
from sys import argv
import os
script_path = os.path.dirname(os.path.realpath(__file__))

#vertex_info
vertexfile = os.path.join(script_path,"../real_data/caide-latest-complete-direct-vertex-properties.txt")
edgefile = os.path.join(script_path,"../real_data/caide-latest-complete-direct-edge-list.txt")
if len(argv) <5:
    print("Please call script with args lowerleftcorner_lat lowerleftcorner_lon upperrightcorner_lat upperrightcorner_lon")
    exit()
lllat=float(argv[1])
lllon=float(argv[2])
urlat=float(argv[3])
urlon=float(argv[4])
in_plot={}
with open(vertexfile) as f:
    for line in f:
        try:
            line_list = line.strip().split()
            thisid = int(line_list[0])
            thislat=float(line_list[1])
            thislon=float(line_list[2])
        except ValueError:
            continue
        if lllat<=thislat<=urlat and lllon<thislon<=urlon:
            in_plot[thisid]=1
        else:
            in_plot[thisid]=0
g=open("new_edges.txt","w")
in_plot2={}
with open(edgefile) as f:
    for line in f:
        try:
            sid,tid = line.strip().split()
            sid=int(sid)
            tid=int(tid)
            if in_plot[sid]==1 or in_plot[tid]==1:
                in_plot2[tid]=1
                in_plot2[sid]=1
                g.write(line)
        except ValueError:
            continue
g.close()

for k in in_plot2:
    in_plot[k]=1

g=open("new_vertex_properties.txt","w")
with open(vertexfile) as f:
    for line in f:
        try:
            line_list = line.strip().split()
            thisid = int(line_list[0])
        except ValueError:
            continue
        if in_plot[thisid]==1:
            g.write(line)

g.close()
