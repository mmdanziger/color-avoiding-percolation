from __future__ import division
ipy = False
try:
    ipy = __IPYTHON__
except NameError:
    pass

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
import numpy as np
import theoretical_curves as tc
import load_colornet as lc
from glob import glob
from os import path
from matplotlib import pyplot as plt
from sys import argv

data_dir = argv[1]
size=str(int(10**6))
if __name__ == "__main__":

    plt.figure()
    plt.ion()

    """
    Code for S
    """
    k = np.linspace(0,10,1000)
    Sfunc = tc.S_ER()
    S = list(map(Sfunc,k))
    plt.plot(k,S,color='black',label="$S$")
    """
    Code for S_inf
    """
    k = np.linspace(0,10,1000)
    Sfunc = tc.S_infER() 
    S = list(map(Sfunc,k))
    plt.plot(k,S,'-.k',label=r"$S_{{\rm color},\infty}$")

    """
    Code for C=10
    """
    data_count={}
    tail_string = "Color_scaling_N=%s_nC=%i*" % (size,10)
    glob_string = path.join(data_dir, tail_string)
    if glob(glob_string):
        data = lc.load_glob(glob_string)
        data_count[size] = len(data)
        label,color = [r"$S_{{\rm color},10}$",'green']
        lc.plot_average_S_color(data,0,label,color,error=None,type="lin")
    k,S_color = tc.get_theory(10,"lin")
    plt.loglog(k,S_color,lw=1,color="blue")
    """
    Code for C=2
    """
    data_count={}
    tail_string = "Color_scaling_N=%s_nC=%i*" % (size,2)
    glob_string = path.join(data_dir, tail_string)
    if glob(glob_string):
        data = lc.load_glob(glob_string)
        data_count[size] = len(data)
        label,color = [r'$S_{{\rm color},2}$','red']
        lc.plot_average_S_color(data,0,label,color,error=None,type="lin")
    k,S_color = tc.get_theory(2,"lin")
    plt.loglog(k,S_color,lw=1,color="blue")
    """
    Code for general plot properties
    """
    plt.xlabel(r"$\bar{k}$")
    plt.ylabel(r"fraction of nodes")
    plt.legend(loc=4)
    plt.yscale('linear', nonposy='clip')
    plt.xscale('linear', nonposy='clip')
    plt.axis([0.5,5,0,1])
    plt.show() if ipy else plt.savefig("/tmp/S_color.pdf")
    if not ipy:
        plt.close()


