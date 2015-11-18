#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy

def fit_exp(Ts, Rs, Rerr, eguess):
    'Fit an exponential function to the data'
    model, ps = 'a * exp(b * x)', 'a,b'
    # Make intelligent guesses for the parameters
    a, b = eguess
    b = pylab.log(Rs[-1]/Rs[0]) / ( Ts[-1] - Ts[0] )
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, b=b) # Set guesses
    fitter.set(xlabel='Temperature',
               ylabel='Resistance')
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_exp.png')
    pylab.savefig('../Graphs/RvsT/fit_exp.pdf')
    return fitter

def fit_power(Ts, Rs, Rerr, pguess):
    'Fit a power function to the data'
    model, ps = 'a * (x-x0)**(3/2)', 'a,x0'
    # Make intelligent guesses for the parameters
    a, x0 = pguess
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, x0=x0) # Set guesses
    fitter.set(xlabel='Temperature',
               ylabel='Resistance')
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_power.png')
    pylab.savefig('../Graphs/RvsT/fit_power.pdf')
    return fitter

def splitfit(Ts, Rs, es, a, b, c, d, pguess, eguess):
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
    fit1 = fit_power(x1, y1, e1, pguess)
    ## Fit one part with the polynomial
    fit2 = fit_exp(x2, y2, e2, eguess)
    return fit1, fit2

def main(data_file, a, b, c, d, pguess, eguess):
    databox = spinmob.data.load(data_file)
    xs, ys, es = databox[0], databox[1], databox[2]
    if 'current' in databox.hkeys:
        current = databox.h('current')
    else:
        current = 1 # mA
        databox.h(current=current)
    Rs = ys / current
    Rerrs = es / current
    fits = splitfit(xs, Rs, Rerrs, a, b, c, d, pguess, eguess)
    return fits

if __name__ == '__main__':
    data_file = sys.argv[1]
    a, b, c, d = sorted([float(i) for i in sys.argv[2:6]])
    fits = main(data_file, a, b, c, d)
    for fit in fits:
        print fit
        print
