#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab

def simple_plot(data_file):
    data = spinmob.data.load(data_file)
    spinmob.plot.xy.data(data[0], data[1])
    pylab.savefig(data_file.split('/')[-1] + '.png')
    pylab.clf()

if __name__ == '__main__':
    files = sys.argv[1:]
    paths = []
    for path in files:
        paths += list(glob.glob(path))
    for path in paths:
        simple_plot(path)
