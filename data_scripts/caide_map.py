from __future__ import division
import matplotlib
matplotlib.use("agg")
from mpl_toolkits.basemap import Basemap
import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict,defaultdict
import os
script_path = os.path.dirname(os.path.realpath(__file__))

#vertex_info
vertexfile = os.path.join(script_path,"../real_data/caide-latest-complete-direct-vertex-properties.txt")
edgefile = os.path.join(script_path,"../real_data/caide-latest-complete-direct-edge-list.txt")
draw_edges = False
# position in decimal lat/lon
country={}
countrylat=defaultdict(float)
countrylon=defaultdict(float)
countrycount=defaultdict(int)
kcore={}
lcolor=[]
lat=OrderedDict()
lon=OrderedDict()
G = nx.Graph()

with open(vertexfile) as f:
    for line in f:
        try:
            thisid,thislat,thislon,thiscid,thisccode,thislcolor,thiskcore = line.strip().split()
        except ValueError:
            continue
        thisid = int(thisid)
        thislat=float(thislat)
        thislon=float(thislon)
        if thislcolor == "1":
            lcolor.append(thisid)
        kcore[thisid]=int(thiskcore)
        country[thisid] = thiscid
        countrylat[thiscid]+=thislat
        countrylon[thiscid]+=thislon
        if thislat != 0 and thislon!=0:
            countrycount[thiscid]+=1
        lat[thisid] = thislat
        lon[thisid] = thislon
for cid in countrylat:
    try:
        countrylat[cid]/=countrycount[cid]
        countrylon[cid]/=countrycount[cid]
    except ZeroDivisionError:
        print("No nonzero for cid %s"%cid)


# put map projection coordinates in pos dictionary
m = Basemap(
        projection='robin',
        lon_0=0,
        resolution='h',
        suppress_ticks=True)

pos={}
pos = dict((idx, m(lon[idx],lat[idx]) )
           if lon[idx]!=0 and lat[idx]!=0 else
           (idx, m(countrylon[country[idx]],countrylat[country[idx]]))
           for idx in lon.keys() )

# draw
plt.figure(figsize=(45,25),dpi=600)
nx.draw_networkx_nodes(G,pos,nodelist=lcolor,node_size=12,node_color="green",alpha=0.6)
nx.draw_networkx_nodes(G,pos,nodelist=[i for i in lat if i not in lcolor],node_shape="^",node_size=12,alpha=0.3)


#\(G,pos,node_size=200,node_color='blue')
if draw_edges:
    max_edges = 5000
    with open(edgefile) as f:
        edge_count=0
        for line in f:
            try:
                sid,tid = line.strip().split()
                edge_count+=1
            except ValueError:
                continue
            G.add_edge(int(sid),int(tid))
            if edge_count > max_edges:
                break
    nx.draw_networkx_edges(G,pos,alpha=0.4)


# Now draw the map
m.drawcountries().set_alpha(0.5)
m.drawcoastlines(linewidth=0.5).set_alpha(0.5)
#m.bluemarble()
plt.savefig("/tmp/AS_globe.png")