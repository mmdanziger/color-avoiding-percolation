from __future__ import division,print_function

import os,json
from sys import exit,argv
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np

script_path = os.path.dirname(os.path.realpath(__file__))

vertexfile = os.path.join(script_path, "../real_data/caide-latest-complete-direct-vertex-properties.txt")
iso2to3 = json.load(open(os.path.join(script_path, "../real_data/iso2to3.json")))
countrycount=defaultdict(int)
lcolorcount=defaultdict(int)
N=20
id2code=[]
with open(vertexfile) as f:
    for line in f:
        try:
            thisid, thislat, thislon, thiscid, thisccode, thislcolor, thiskcore = line.strip().split()
        except ValueError:
            continue
        if thisccode not in id2code:
            id2code.append(thisccode)
        countrycount[thisccode]+=1
        if thislcolor == "1":
            lcolorcount[thisccode]+=1

total_N = sum(countrycount.values())
total_L = sum(lcolorcount.values())
print("Overall fraction in L_color: %i / %i (%.4f)" %(total_L,total_N,total_L/total_N) )
topN_count = sorted(countrycount.items(),key=lambda x: x[1],reverse=True)[:N]
topN_lcolor_dict = dict((k,v ) for k,v in lcolorcount.items() if k in map(lambda x: x[0],topN_count))
topN_lcolor_ranked = sorted(topN_lcolor_dict.items(), key=lambda x:x[1])

X = np.loadtxt(argv[1])

top_k = len(set(X[:,0]))

A = np.zeros((top_k,top_k))

code_to_idx={}
init_color = X[0][0]
labels=[]
for idx,row in enumerate(X):
    if row[0] != init_color:
        break
    code_to_idx[row[1]] = idx
    labels.append(iso2to3[id2code[int(row[1])]])

for sid,rid,srlcol,slcol,rlcol,stotal,rtotal in X:
    A[code_to_idx[sid],code_to_idx[rid]] = slcol / stotal
    if sid != rid:
        A[code_to_idx[rid], code_to_idx[sid]] = rlcol / rtotal

plt.figure()
plt.imshow(A,interpolation="none",cmap=cm.viridis)
plt.xticks(np.arange(top_k), labels)
plt.yticks(np.arange(top_k), labels)
plt.show()