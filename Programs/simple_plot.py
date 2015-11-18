#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab

def simple_plot(data_file, title=None):
    databox = spinmob.data.load(data_file)
    xs, ys, es = databox[0], databox[1], databox[2]
    databox[1] = abs(ys)
    spinmob.plot.xy.data(xs, abs(ys), es, marker='+')
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Potential (V)')
    spinmob.plot.tweaks.ubertidy(keep_axis_labels=True)
    if title: pylab.title(title)
    pylab.savefig('../Graphs/Simple plots/' + data_file.split('/')[-1] + '.png')
    pylab.savefig('../Graphs/Simple plots/' + data_file.split('/')[-1] + '.pdf')
    pylab.clf()

if __name__ == '__main__':
    files = sys.argv[1:]
    paths = []
    for path in files:
        paths += list(glob.glob(path))
    for path in paths:
        simple_plot(path)
