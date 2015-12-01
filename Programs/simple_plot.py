#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab

def simple_plot(data_file, title=None, fct=lambda x: x,
                ylabel='Potential (V)',
                xlabel='Temperature (K)',
                xmin=None, xmax=None):
    databox = spinmob.data.load(data_file)
    xs, ys = databox[0], databox[1]
    if xmin: pylab.xmin(xmin)
    if xmax: pylab.xmax(xmax)
    if title: pylab.title(title)
    pylab.plot(xs, fct(abs(ys)), '.')
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
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
