#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy

def make_error(data_file):
    databox = spinmob.data.load(data_file)
    errs = []
    for i in range(6):
        vals = databox.c('c{:d}'.format(i))
        std = pylab.std(vals)
        errs.append(std)
    err = pylab.mean(errs)
    return err, errs

def main():
    pass

if __name__ == '__main__':
    main()
