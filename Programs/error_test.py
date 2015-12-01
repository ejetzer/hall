#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy

def make_error(data_file, xin=None):
    databox = spinmob.data.load(data_file)
    errs = []
    xs = databox.c('c8')
    xs -= xs[0]
    for i in range(6):
        vals = databox.c('c{:d}'.format(i))
        if xin:
            vals = pylab.array([v for x, v in zip(xs, vals) if xin[0] <= x <= xin[1]])
        std = pylab.std(vals)
        errs.append(std)
    err = pylab.mean(errs)
    return err, errs

def main():
    pass

if __name__ == '__main__':
    main()
