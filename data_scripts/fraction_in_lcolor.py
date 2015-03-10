from __future__ import division,print_function

import os,json
from sys import exit
from collections import defaultdict
from matplotlib import pyplot as plt

script_path = os.path.dirname(os.path.realpath(__file__))

vertexfile = os.path.join(script_path, "../real_data/caide-latest-complete-direct-vertex-properties.txt")
iso2to3 = json.load(open(os.path.join(script_path, "../real_data/iso2to3.json")))
countrycount=defaultdict(int)
lcolorcount=defaultdict(int)
N=20
id2code={}
with open(vertexfile) as f:
    for line in f:
        try:
            thisid, thislat, thislon, thiscid, thisccode, thislcolor, thiskcore = line.strip().split()
        except ValueError:
            continue
        id2code[thiscid] = thisccode
        countrycount[thisccode]+=1
        if thislcolor == "1":
            lcolorcount[thisccode]+=1

topN_count = sorted(countrycount.items(),key=lambda x: x[1],reverse=True)[:N]
topN_lcolor_dict = dict((k,v ) for k,v in lcolorcount.items() if k in map(lambda x: x[0],topN_count))
topN_lcolor_ranked = sorted(topN_lcolor_dict.items(), key=lambda x:x[1],reverse=True)


plt.bar(list(range(N)), [countrycount[i[0]] for i in topN_lcolor_ranked],color="red",alpha=0.6)
plt.bar(list(range(N)), [lcolorcount[i[0]] for i in topN_lcolor_ranked],alpha=0.8)
plt.xticks([i+0.5 for i in range(N)],[iso2to3[i[0]] for i in topN_lcolor_ranked],rotation="vertical")
plt.ylim(ymax=4500)
plt.tight_layout()
plt.show()