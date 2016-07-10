from __future__ import division,print_function

import os,json
from sys import exit,argv
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from os.path import basename
from matplotlib.colors import LogNorm
from matplotlib.ticker import FuncFormatter

script_path = os.path.dirname(os.path.realpath(__file__))

vertexfile = os.path.join(script_path, "../real_data/caide-latest-complete-direct-vertex-properties.txt")
iso2to3 = json.load(open(os.path.join(script_path, "../real_data/iso2to3.json")))
countrycount=defaultdict(int)
lcolorcount=defaultdict(int)
N=20
newid2oldid=[]
newid2oldcode=[]
with open(vertexfile) as f:
    for line in f:
        try:
            thisid, thislat, thislon, thiscid, thisccode, thislcolor, thiskcore = line.strip().split()
        except ValueError:
            continue
        if thisccode not in newid2oldcode:
            newid2oldid.append(thiscid)
            newid2oldcode.append(thisccode)
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
B = np.zeros((top_k,top_k))

code_to_idx={}
init_color = X[0][0]
labels=[]
for idx,row in enumerate(X):
    if row[0] != init_color:
        break
    code_to_idx[row[1]] = idx
    labels.append(iso2to3[newid2oldcode[int(row[1])]])



for sid,rid,srlcol,slcol,rlcol,stotal,rtotal in X:
    A[code_to_idx[sid],code_to_idx[rid]] = slcol / stotal
    if sid != rid:
        A[code_to_idx[rid], code_to_idx[sid]] = rlcol / rtotal

for sid,rid,srlcol,slcol,rlcol,stotal,rtotal in X:
    B[code_to_idx[sid],code_to_idx[rid]] = slcol / lcolorcount[newid2oldcode[int(sid)]]
    if sid != rid:
        B[code_to_idx[rid], code_to_idx[sid]] = rlcol / lcolorcount[newid2oldcode[int(rid)]]

fmt = lambda x,pos: "%.2f"%10**x

plt.figure(figsize=(8,7))
plt.imshow(A,interpolation="none",cmap=cm.viridis)
plt.colorbar()
plt.xticks(np.arange(top_k), labels, rotation=90)
plt.yticks(np.arange(top_k), labels)
plt.tight_layout()
plt.savefig("/tmp/" +basename(argv[1]).rstrip(".txt")+".pdf")

plt.figure(figsize=(8,7))
im = plt.imshow(np.log10(B),interpolation="none",cmap=cm.viridis)
ticks = np.linspace(B.min(),B.max(),10)
plt.colorbar(im,ticks=np.log10(ticks),format=FuncFormatter(fmt))
plt.xticks(np.arange(top_k), labels, rotation=90)
plt.yticks(np.arange(top_k), labels)
plt.tight_layout()
plt.savefig("/tmp/" +basename(argv[1]).rstrip(".txt")+"_improvement.pdf")

