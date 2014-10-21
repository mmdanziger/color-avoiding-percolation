from __future__ import division, print_function
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from collections import defaultdict
import json


def get_data_from_file(fname):
    d = json.load(open(fname))
    d["k"] = np.array(d["k"])
    d["kc"] = d["Nc"] / (d["Nc"] - 1)
    d["S_color"] = np.array(d["S_color"]) / d["N"]
    return d


def load_glob(glob_arg):
    return [get_data_from_file(fname) for fname in glob(glob_arg)]


def scatter_plot_S_color(data, offset=None, connect_dots=False):
    if offset is None:
        offset = data["kc"]
    ls = ".-" if connect_dots else "."
    plt.loglog(data["k"] - offset, data["S_color"], ls)


def plot_average_S_color(data_list, offset=None, label_text=""):
    all_k_list = []
    all_S_list = []
    for data in data_list:
        if offset is None:
            offset = data["kc"]
        # TODO: Add binning for this function.  Needs to be log-binned so tricky.
        all_k_list.append(data["k"] - offset)
        all_S_list.append(data["S_color"])
    K = np.mean(all_k_list,axis=0)
    #assert( sum(np.diff(all_k_list)) < 1e-9)
    Savg = np.mean(all_S_list, axis=0)
    Serr = np.std(all_S_list, axis=0)
    #K, Savg, Serr = zip(*[(k_, np.mean(S_), np.std(S_)) for k, S_ in sorted(all_k_dict.items())])
    plt.loglog(K, Savg, label=label_text)
    plt.errorbar(K, Savg, yerr=Serr)
    return K, Savg, Serr


def plot_full_Scolor_curve(fname):
    d = json.load(open(fname))
    plt.plot(np.array(range(len(d['S_color']))) * d['link_res'] * 2 / d['N'], np.array(d['S_color']) / d['N'], '.-',
             label="$N_c=%i$" % d['Nc'])
    return d


def plot_all_curves(glob_arg):
    ds = list(map(plot_full_Scolor_curve,glob(glob_arg)))
    plt.xlabel(r"$<k>$")
    plt.ylabel(r"$S_color$")
    plt.legend(loc=2)
    return ds

def plot_above_kc(d):
    # this is from Sebastian's write-up:
    kc = lambda Nc: Nc / (Nc - 1)
    N_links_c = lambda N, Nc: int(2 * N * kc(Nc))
    N = d['N']
    Nc = d['Nc']
    #k = np.array(range(len(d['S_color'])))*2/d['N'] - kc(Nc)
    k = np.array(d['k']) - kc(Nc)
    S_color = np.array(d['S_color'])/d['N']
    try:
        plt.loglog(k, S_color , '.-', label="$N_c=%i$"%d['Nc'])
        plt.show()
    except ValueError:
        print("Unable to plot, max k is %.5f and max S_color is %.5f"%(max(k),max(S_color)))
    #plt.loglog(k[N_links_c(N,Nc):], S_color[N_links_c(N,Nc):] , label="$N_c=%i$"%d['Nc'])
    return k, S_color


def plot_fits(preloaded=None, glob_arg=None):
    if preloaded is None:
        ds = map(lambda fn: json.load(open(fn)), glob(glob_arg))
    else:
        ds = preloaded
    to_return = map(plot_above_kc, ds)
    return to_return

def plot_averaged_fits(curves):
    S_avg = np.mean([i[1] for i in curves],axis=0)
    S_err = np.std([i[1] for i in curves],axis=0)
    k = np.mean([i[0] for i in curves],axis=0)
    k_err = np.std([i[0] for i in curves],axis=0)
    if sum(k_err) < 1e-7:
        plt.errorbar(k,S_avg,yerr=S_err)
    else:
        plt.errorbar(k,S_avg,xerr=k_err,yerr=S_err)
    plt.plot(k,S_avg,lw=3)
    return k,S_avg,S_err