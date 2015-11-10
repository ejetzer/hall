#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab

def simple_plot(data_file):
    databox = spinmob.data.load(data_file)
    spinmob.plot.xy.databoxes([databox], 'd[0]', 'd[1]*d[3]', 'd[2]')
    pylab.savefig(data_file.split('/')[-1] + '.png')
    pylab.savefig(data_file.split('/')[-1] + '.pdf')
    pylab.clf()

if __name__ == '__main__':
    files = sys.argv[1:]
    paths = []
    for path in files:
        paths += list(glob.glob(path))
    for path in paths:
        simple_plot(path)
