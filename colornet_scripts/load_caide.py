from __future__ import division,print_function

import colored_graph

cg = colored_graph.ColoredGraph()
cg.load_edges()
cg.load_vertex_properties()
for color in cg.all_colors:
    cg.calculate_lcbar(color)

