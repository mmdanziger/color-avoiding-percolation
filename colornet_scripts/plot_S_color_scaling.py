from __future__ import division
ipy = False
try:
    ipy = __IPYTHON__
except NameError:
    pass
import numpy as np
import matplotlib

if not ipy:
    matplotlib.use('Qt4Agg')
    matplotlib.rcParams.update({"figure.autolayout": "true"})
    try:
        matplotlib.rcParams.update({"usetex": "true"})
    except KeyError:
        matplotlib.rcParams.update({"text.usetex": "true"})
    from matplotlib import font_manager
    font_manager.USE_FONTCONFIG = True

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

def label_color(size):
    if size == "100000":
        return r"$N = 10^5$","cyan"
    elif size == "1000000":
        return r"$N = 10^6$","red"
    elif size == "10000000":
        return r"$N = 10^7$","magenta"
    elif size == "100000000":
        return r"$N = 10^8$","green"
    elif size == "1000000000":
        return r"$N = 10^9$","gray"
    else:
        return "N = %.2E"%float(size),"yellow"

if __name__ == "__main__":
    k,S_color = tc.get_theory(int(nc))
    plt.figure()
    plt.ion()
    plt.loglog(k,S_color,lw=3,label="theory")
    data_count={}
    for size in sizes:
        tail_string = "Color_scaling_N=%s_nC=%s*" % (size,nc)
        glob_string = path.join(data_dir, tail_string)
        if glob(glob_string):
            data = lc.load_glob(glob_string)
            data_count[size] = len(data)
            label,color = label_color(size)
            lc.plot_average_S_color(data,None,label,color,error=None)
            for dset in data:
                lc.scatter_plot_S_color(dset,color=color)
    plt.xlabel(r"$k - k_c$")
    plt.ylabel(r"$S_{color}$")
    plt.legend(loc=4)
    plt.axis([1e-4,1e-1,1e-11,1e-2])
    plt.show() if ipy else plt.savefig("/tmp/S_scaling_%s.pdf"%nc)
    if not ipy:
        plt.close()