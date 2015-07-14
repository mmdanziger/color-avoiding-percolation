from __future__ import division,print_function
import colored_graph
from collections import defaultdict,Counter
import matplotlib.pyplot as plt
import numpy as np


cg = colored_graph.ColoredGraph(lonlatids=False)
lcol = defaultdict(int)
for i in cg.seb_lcolor:
    lcol[i]=1

c_in_lcolor= Counter([k for idx,k in cg.G.degree().items() if lcol[idx]==1])
c_not_in_lcolor= Counter([k for idx,k in cg.G.degree().items() if lcol[idx]==0])

plt.figure()
k1,Pk1 = zip(*sorted(c_in_lcolor.items()))
k0,Pk0 = zip(*sorted(c_not_in_lcolor.items()))
Pk1 = np.array(Pk1)/sum(Pk1)
Pk0 = np.array(Pk0)/sum(Pk0)
plt.loglog(k1,Pk1,'.-',label=r"$\mathcal{L}_{\rm col}$")
plt.loglog(k0,Pk0,'.-',label=r"$\bar{\mathcal{L}}_{\rm col}$")
plt.axis("tight")
plt.grid()
plt.xlabel(r"$k$")
plt.ylabel(r"$P(k)$")
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("/tmp/L_color_by_degree.pdf")