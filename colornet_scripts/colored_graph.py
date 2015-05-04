from __future__ import print_function,division
import networkx as nx
import os,json
from sys import exit
from collections import Counter,defaultdict

script_path = os.path.dirname(os.path.realpath(__file__))
from sys import argv
get_item = lambda ind : lambda x: x[ind]

class ColoredGraph(object):

    def __init__(self):
        self.G = nx.Graph()
        self.color={}
        self.all_colors=set()
        self.lc_components={}
        self.lcolor=set()

    def load_edges(self,fname=None):
        fname =  os.path.join(script_path, "../real_data/caide-latest-complete-direct-edge-list.txt") if fname is None else fname
        with open(fname) as f:
            f.readline()
            for row in f:
                try:
                    i,j = row.strip().split()
                    self.G.add_edge(int(i),int(j))
                except ValueError:
                    pass

    def load_vertex_properties(self, fname=None):
        fname =  os.path.join(script_path, "../real_data/caide-latest-complete-direct-vertex-properties.txt") if fname is None else fname
        with open(fname) as f:
            f.readline();f.readline();f.readline();
            for row in f:
                thisid, thislat, thislon, thiscid, thisccode, thislcolor, thiskcore \
                        = row.strip().split()
                self.color[int(thisid)] = int(thiscid)
                self.all_colors.add(int(thiscid))
    def calculate_lcbar(self,to_avoid):
        all_seen=defaultdict(lambda : -1) #not visited nodes evaluate to -1
        double_counted=defaultdict(list)
        for source in self.G.nodes_iter(): #find all components from all sources
            #if self.color[source] == to_avoid or source in all_seen:
            #don't start a search on a bad node
            #    continue
            seen={}                  # level (number of hops) when seen in BFS
            level=0                  # the current level
            nextlevel={source:1}  # dict of nodes to check at next level
            while nextlevel:
                thislevel=nextlevel  # advance to next level
                nextlevel={}         # and start a new list (fringe)
                for v in thislevel:
                    if v not in seen:
                        seen[v]=level
                        if all_seen[v] != -1: #this should only occur for a to_avoid node that
                            double_counted[all_seen[v]].append(v) # set the level of vertex v
                        all_seen[v] = source
                        if self.color[v] != to_avoid:
                            nextlevel.update(self.G[v]) # add neighbors of v
                level=level+1
        comp_counter = Counter(all_seen.values())
        for key,doubles in double_counted.items():
            comp_counter[key]+=len(doubles)
        max_key,count = list(sorted(comp_counter.items(),key=get_item(1),reverse=True))[0]
        self.lc_components[to_avoid] = [node for node in self.G.nodes_iter() if all_seen[node] == max_key] + double_counted[source]
        self.lcolor = set(self.lc_components[to_avoid]) if len(self.lcolor) ==0 else self.lcolor.intersection(self.lc_components[to_avoid])
    def calculate_lcolor(self):
        for color in self.all_colors:
            self.calculate_lcbar(color)

