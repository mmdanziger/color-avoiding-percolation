from __future__ import division,print_function
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import json

def plot_full_Scolor_curve(fname):
    d = json.load(open(fname))
    plt.plot(np.array(range(len(d['S_color'])))*2/d['N'], np.array(d['S_color'])/d['N'], label="$N_c=%i$"%d['Nc'])
    return d

def plot_all_curves(glob_arg):
    ds = map(plot_full_Scolor_curve,glob(glob_arg))
    plt.xlabel(r"$<k>$")
    plt.ylabel(r"$S_color$")
    plt.legend(loc=2)

def plot_above_kc(d):
    #this is from Sebastian's write-up:
    kc = lambda Nc: Nc / (Nc - 1)
    N_links_c = lambda N,Nc: int(2*N*kc(Nc))
    N = d['N']
    Nc = d['Nc']
    k = np.array(range(len(d['S_color'])))*2/d['N'] - kc(Nc)
    S_color = np.array(d['S_color'])/d['N']
    plt.loglog(k, S_color , '.-', label="$N_c=%i$"%d['Nc'])
    plt.show()
    #plt.loglog(k[N_links_c(N,Nc):], S_color[N_links_c(N,Nc):] , label="$N_c=%i$"%d['Nc'])
    return k,S_color

def plot_fits(preloaded=None,glob_arg=None):
    if preloaded is None:
        ds = map(lambda fn: json.load(open(fn)), glob(glob_arg))
    else:
        ds = preloaded
    to_return = map(plot_above_kc,ds)
    return to_return
