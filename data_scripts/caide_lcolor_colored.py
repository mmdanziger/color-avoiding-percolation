#!/usr/bin/python3
from __future__ import division,print_function
import matplotlib

matplotlib.use("pdf")
from mpl_toolkits.basemap import Basemap
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors
from numpy.random import shuffle
from collections import OrderedDict, defaultdict
import os

script_path = os.path.dirname(os.path.realpath(__file__))
from sys import argv

if len(argv) > 4:
    ll_lat = float(argv[1])
    ll_lon = float(argv[2])
    ur_lat = float(argv[3])
    ur_lon = float(argv[4])
else:
    print("Please enter lower left (lat,lon) and upper right (lat,lon) args to create the figure.")
    exit()
# vertex_info
vertexfile = os.path.join(script_path, "../real_data/caide-latest-complete-direct-vertex-properties.txt")
edgefile = os.path.join(script_path, "../real_data/caide-latest-complete-direct-edge-list.txt")
draw_edges = False
# position in decimal lat/lon
country = {}
countrylat = defaultdict(float)
countrylon = defaultdict(float)
countrycount = defaultdict(int)
kcore = {}
lcolor = []
id2code = {}
lat = OrderedDict()
lon = OrderedDict()
G = nx.Graph()
plot_all = False
# m2 = Basemap(width=40e6,height=40e6,projection='aea',
#                resolution=None,lat_0=(ll_lat+ur_lat)/2, lon_0=(ll_lon + ur_lon)/2,suppress_ticks=True)
pos = {}
m = Basemap(llcrnrlat=ll_lat, llcrnrlon=ll_lon, urcrnrlat=ur_lat, urcrnrlon=ur_lon, projection='aea',
            area_thresh=500, resolution='f', lat_0=(ll_lat + ur_lat) / 2, lon_0=(ll_lon + ur_lon) / 2,
            suppress_ticks=True)

with open(vertexfile) as f:
    for line in f:
        try:
            thisid, thislat, thislon, thiscid, thisccode, thislcolor, thiskcore = line.strip().split()
        except ValueError:
            continue
        thisid = int(thisid)
        thislat = float(thislat)
        thislon = float(thislon)
        pos[thisid] = m(thislon, thislat)
        countrylat[thiscid] += thislat
        countrylon[thiscid] += thislon
        country[thisid] = thiscid
        id2code[thiscid] = thisccode
        if thislat != 0 and thislon != 0:
            countrycount[thiscid] += 1
        if not plot_all:
            if not (ll_lat <= thislat <= ur_lat and ll_lon <= thislon <= ur_lon):
                continue
        if thislcolor == "1":
            lcolor.append(thisid)
        kcore[thisid] = int(thiskcore)
        lat[thisid] = thislat
        lon[thisid] = thislon
for cid in countrylat:
    try:
        countrylat[cid] /= countrycount[cid]
        countrylon[cid] /= countrycount[cid]
    except ZeroDivisionError:
        print("No nonzero for cid %s" % cid)

#ll_lat,ll_lon,ur_lat,ur_lon=[36.5, -89.5, 48.8, -66.5]
#ll_lat,ll_lon,ur_lat,ur_lon=[40.66, -74.18, 41.17, -73.16]
# put map projection coordinates in pos dictionary


for idx in pos:
    if pos[idx] == m(0, 0):
        pos[idx] = m(countrylon[country[idx]], countrylat[country[idx]])

countries = list(set([country[idx] for idx in lon]))
country_colors = list(colors.cnames.keys())
shuffle(country_colors)


# draw
plt.figure(figsize=(6, 6), dpi=400)


not_lcolor = [i for i in lon if i not in lcolor]
nx.draw_networkx_nodes(G, pos, nodelist=lcolor, node_size=80, node_color="green", alpha=0.7)
nx.draw_networkx_nodes(G, pos, nodelist=not_lcolor, node_shape="^", node_color="red", node_size=80, alpha=0.4)


#\(G,pos,node_size=200,node_color='blue')
if draw_edges:
    max_edges = 25000
    with open(edgefile) as f:
        edge_count = 0
        for line in f:
            try:
                sid, tid = map(int, line.strip().split())
            except ValueError:
                continue
            if sid in lat or tid in lat:
                G.add_edge(sid, tid)
                edge_count += 1
            if edge_count > max_edges:
                break
    nx.draw_networkx_edges(G, pos, alpha=0.2, width=0.5)


# Now draw the map
m.drawcountries(linewidth=1.5, zorder=-5).set_alpha(0.9)
m.drawcoastlines(linewidth=1.5, zorder=-5).set_alpha(0.9)
m.shadedrelief(alpha=0.7, zorder=-5)
plt.savefig("/tmp/AS_Lcolor_Spain.pdf")