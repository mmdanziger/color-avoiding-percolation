from __future__ import division,print_function
import colored_graph
from collections import defaultdict,Counter
import matplotlib.pyplot as plt
import numpy as np
import os,json
from sys import argv


nosweden = True if len(argv) > 1 else False



script_path = os.path.dirname(os.path.realpath(__file__))


iso2to3 = json.load(open(os.path.join(script_path, "../real_data/iso2to3.json")))

cg = colored_graph.ColoredGraph(lonlatids=False)
lcol = defaultdict(int)
for i in cg.seb_lcolor:
    lcol[i]=1
country_degree = defaultdict(list)
country_lcol = defaultdict(int) #only keep track of lcol, total is len of other dict

for i in cg.G.nodes_iter():
    country_degree[cg.color[i]].append(cg.G.degree(i))
    country_lcol[cg.color[i]]+=lcol[i]

for country in country_lcol:
    country_lcol[country] /= len(country_degree[country])

country_avg_degree = dict( (k,np.mean(v)) for k,v in country_degree.items())

threshold_country_size = 20
minx,maxx,miny,maxy=[1e6,0,1e6,0]
plt.figure(figsize=(7,10))
for country in country_avg_degree:
    if len(country_degree[country]) > threshold_country_size:
        x = country_avg_degree[country]
        y = country_lcol[country]
        minx,maxx,miny,maxy = [min(minx,x),max(maxx,x),min(miny,y),max(maxy,y)]
        plt.text(x,y,country,
            fontsize=10,horizontalalignment='center',verticalalignment='center' )

plt.axis([minx*0.75,maxx*1.25,0,1])
if nosweden:
    plt.axis([minx*0.75,28,0,1])
plt.grid()
plt.xlabel(r"$\langle k_C \rangle$")
plt.ylabel(r"$P(\mathcal{L}_{\rm color})$")
plt.savefig("/tmp/L_color_by_country_by_degree.pdf") if not nosweden else plt.savefig("/tmp/L_color_by_country_by_degree_no_sweden.pdf")
