from __future__ import division
import load_colornet as lc
import logbin
from sys import argv
from glob import glob
from os import path
from matplotlib import pyplot as plt
data_dir = argv[1]
nc = argv[2]

sizes = [ "100000" , "1000000", "10000000", "100000000", "1000000000"]

def label(size):
    if size == "100000":
        return r"$N = 10^5$"
    elif size == "1000000":
        return r"$N = 10^6$"
    elif size == "10000000":
        return r"$N = 10^7$"
    elif size == "100000000":
        return r"$N = 10^8$"
    elif size == "1000000000":
        return r"$N = 10^9$"
    else:
        return "N = %.2E"%float(size)
plt.figure()
for size in sizes:
    tail_string = "Color_scaling_N=%s_nC=%s*" % (size,nc)
    glob_string = path.join(data_dir, tail_string)
    if glob(glob_string):
        data = lc.load_glob(glob_string)
        lc.plot_average_S_color(data,None,label(size),error="y")
plt.xlabel(r"$k - k_c$")
plt.ylabel(r"$S_{color}$")
plt.legend(loc=2)
plt.show()