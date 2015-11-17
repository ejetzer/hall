#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy

def fit_exp(Ts, Rs, Rerr, a=1, b=1, x0=0):
    'Fit an exponential function to the data'
    model, ps = 'a * exp(b * (x-x0))', 'a,b,x0'
    # Make intelligent guesses for the parameters
    #a, b, x0 = 1, 1, 0
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, b=b, x0=x0) # Set guesses
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_exp.png')
    pylab.savefig('../Graphs/RvsT/fit_exp.pdf')
    return fitter

def fit_power(Ts, Rs, Rerr, a=1, x0=0):
    'Fit a power function to the data'
    model, ps = 'a * (x-x0)**(3/2)', 'a,x0'
    # Make intelligent guesses for the parameters
    #a, x0 = 1, 1
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, x0=x0) # Set guesses
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_power.png')
    pylab.savefig('../Graphs/RvsT/fit_power.pdf')
    return fitter

def splitfit(Ts, Rs, es, a, b, c, d, a1=1, a2=1, b2=1, x01=0, x02=0):
    ## Split the data in two parts
    x1, x2, y1, y2, e1, e2 = [], [], [], [], [], []
    for T, R, e in zip(Ts, Rs, es):
        if a < T < b:
            x1.append(T)
            y1.append(abs(R))
            e1.append(e)
        elif c < T < d:
            x2.append(T)
            y2.append(abs(R))
            e2.append(e)
    ## Fit one part with the exponential
    fit1 = fit_power(x1, y1, e1, a1, x01)
    ## Fit one part with the polynomial
    fit2 = fit_exp(x2, y2, e2, a2, b2, x02)
    return fit1, fit2

def main(data_file, a, b, c, d, a1=1, a2=1, b2=1, x01=0, x02=0):
    databox = spinmob.data.load(data_file)
    xs, ys, es = databox[0], databox[1], databox[2]
    if 'current' in databox.hkeys:
        current = databox.h('current')
    else:
        current = 1 # mA
        databox.h(current=current)
    Rs = ys / current
    Rerrs = es / current
    fits = splitfit(xs, Rs, Rerrs, a, b, c, d, a1, a2, b2, x01, x02)
    return fits

if __name__ == '__main__':
    data_file = sys.argv[1]
    a, b, c, d = sorted([float(i) for i in sys.argv[2:6]])
    fits = main(data_file, a, b, c, d)
    for fit in fits:
        print fit
        print
