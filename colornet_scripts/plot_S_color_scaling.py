from __future__ import division
import load_colornet as lc
import logbin
from sys import argv
from glob import glob
from os import path
from matplotlib import pyplot as plt
import theoretical_curves as tc
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

if __name__ == "__main__":
    plt.figure()
    k,S_color = tc.get_theory(int(nc))
    plt.loglog(k,S_color,lw=3,label="theory")
    for size in sizes:
        tail_string = "Color_scaling_N=%s_nC=%s*" % (size,nc)
        glob_string = path.join(data_dir, tail_string)
        if glob(glob_string):
            data = lc.load_glob(glob_string)
            lc.plot_average_S_color(data,None,label(size),error=None)
    plt.xlabel(r"$k - k_c$")
    plt.ylabel(r"$S_{color}$")
    plt.legend(loc=4)
    plt.axis([1e-4,1e-1,1e-11,1e-2])
    plt.show()