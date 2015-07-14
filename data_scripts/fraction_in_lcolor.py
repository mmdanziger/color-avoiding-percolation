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

total_N = sum(countrycount.values())
total_L = sum(lcolorcount.values())
print("Overall fraction in L_color: %i / %i (%.4f)" %(total_L,total_N,total_L/total_N) )
topN_count = sorted(countrycount.items(),key=lambda x: x[1],reverse=True)[:N]
topN_lcolor_dict = dict((k,v ) for k,v in lcolorcount.items() if k in map(lambda x: x[0],topN_count))
topN_lcolor_ranked = sorted(topN_lcolor_dict.items(), key=lambda x:x[1])
print("By country:")
for cid,num in reversed(topN_lcolor_ranked):
    print("%s\t%i / %i\t%.6f" % (iso2to3[cid],num,countrycount[cid], num/countrycount[cid]))


plt.figure(figsize=(5,7.5))
plt.barh(list(range(N)), [countrycount[i[0]] for i in topN_lcolor_ranked],color="red",alpha=0.6)
plt.barh(list(range(N)), [lcolorcount[i[0]] for i in topN_lcolor_ranked],alpha=0.8)
plt.yticks([i+0.5 for i in range(N)],[iso2to3[i[0]] for i in topN_lcolor_ranked])
plt.xticks([0,500,1000,1500,2000,2500,3000,3500,4000],[0,'',1000,'',2000,'',3000,'',4000])
plt.xlim(xmax=4500)
plt.xlabel("Connectable/Total Nodes")
plt.tight_layout()
plt.show()
plt.savefig("/tmp/AS_top%i.pdf"%N)
