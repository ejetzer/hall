#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab

def simple_plot(data_file, title=None, fct=lambda x: x,
                ylabel='Potential (V)',
                xlabel='Temperature (K)',
                xmin=None, xmax=None,
                outfile=None):
    if not isinstance(data_file, list): data_file = [data_file]
    for df in data_file:
        databox = spinmob.data.load(df)
        xs, ys = databox[0], databox[1]
        if not xmin: xmin = min(xs)
        if not xmax: xmax = max(xs)
        ys = [fct(abs(y)) for x, y in zip(xs, ys) if xmin <= x <= xmax]
        xs = [x for x in xs if xmin <= x <= xmax]
        pylab.plot(xs, ys, '.')
    if title: pylab.title(title)
    pylab.xlabel(xlabel)
    pylab.ylabel(ylabel)
    if not outfile: outfile = data_file[0].split('/')[-1]
    pylab.savefig('../Graphs/Simple plots/' + outfile + '.png')
    pylab.savefig('../Graphs/Simple plots/' + outfile + '.pdf')
    pylab.clf()

if __name__ == '__main__':
    files = sys.argv[1:]
    paths = []
    for path in files:
        paths += list(glob.glob(path))
    for path in paths:
        simple_plot(path)
