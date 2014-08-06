#! /usr/bin/env python
from __future__ import division
from itertools import product as iproduct
from subprocess import call
from time import time


def do_params(nC):
    global krange, N
    print[krange, nC, N]
    now = ("%.7f"%time()).replace('.','')[-10:]
    kwargs = {}
    kwargs["N"] = N
    kwargs["krange"] = krange
    kwargs["Nc"] = nC

    kwargs["output"] = "Color_scaling_N=%i_nC=%i_krange=%.4f_%s.json" % (N, nC, krange, now)
    kwarray = ["colornet"]
    for k, v in kwargs.items():
        kwarray.append("--" + k)
        kwarray.append(str(v))
    call(kwarray)
    return 0


if __name__ == '__main__':
    from sys import argv

    krange = 1
    N = 10000000
    nc_min = 3
    nc_max = 3
    repititions = 20
    nc_vals = [i for i in range(nc_min, nc_max + 1)] * repititions
    try:
        from multiprocessing import Process, Pool, cpu_count

        pool = Pool(processes=int(argv[1]))
        res = pool.map_async(do_params, nc_vals)
        print
        res.get()
    except ImportError:
        print
        "Not utilizing multiprocessing"
        map(do_params, nc_vals)
