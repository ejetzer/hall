#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy

def fit_exp(Ts, Rs, Rerr, eguess):
    'Fit an exponential function to the data'
    Rs, Rerr = pylab.array(Rs), pylab.array(Rerr)
    model, ps = '1/a * exp(b * x)', 'a,b'
    # Make intelligent guesses for the parameters
    a, b = eguess
    b = pylab.log(Rs[0]/Rs[1]) / ( Rs[-1] - Rs[0] )
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, b=b) # Set guesses
    fitter.set(xlabel='Temperature (K)',
               ylabel='Resistance ($\Omega$)')
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_exp.png')
    pylab.savefig('../Graphs/RvsT/fit_exp.pdf')
    return fitter

def fit_power(Ts, Rs, Rerr, pguess):
    'Fit a power function to the data'
    Rs, Rerr = pylab.array(Rs), pylab.array(Rerr)
    model, ps = 'a * (x-x0) + b', 'a,x0,b'
    # Make intelligent guesses for the parameters
    a, x0, b = pguess
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, x0=x0, b=b) # Set guesses
    fitter.set(xlabel='Temperature (K)',
               ylabel='Resistance ($\Omega$)')
    # Fit.
    fitter.fit()
    pylab.savefig('../Graphs/RvsT/fit_power.png')
    pylab.savefig('../Graphs/RvsT/fit_power.pdf')
    return fitter

def splitfit(Ts, Rs, es, a, b, c, d, pguess, eguess):
    ## Split the data in two parts
    x1, x2, y1, y2, e1, e2 = [], [], [], [], [], []
    for T, R, pe, ee in zip(Ts, Rs, es[0], es[1]):
        if a < T < b:
            x1.append(T)
            y1.append(abs(R))
            e1.append(pe)
        elif c < T < d:
            x2.append(T)
            y2.append(abs(R))
            e2.append(ee)
    ## Fit one part with the exponential
    fit1 = fit_power(x1, y1, e1, pguess)
    ## Fit one part with the polynomial
    fit2 = fit_exp(x2, y2, e2, eguess)
    return fit1, fit2

def main(data_file, a, b, c, d, pguess, eguess, perr=1, eerr=1):
    databox = spinmob.data.load(data_file)
    xs, ys, es, Ns = databox[:4]
    pes, ees = perr / pylab.sqrt(Ns), eerr / pylab.sqrt(Ns)
    if 'current' in databox.hkeys:
        current = databox.h('current')
    else:
        current = 0.001 # A
        databox.h(current=current)
    Rs = ys / current
    Rerrs = pes / current, ees / current
    fits = splitfit(xs, Rs, Rerrs, a, b, c, d, pguess, eguess)
    return fits

def print_results(fits):
    models = ('# Power fit', '# Exponential fit')
    for model, fit in zip(models, fits):
        print model
        print
        text = str(fit)
        lines = text.split('\n')
        limit = -1
        # Only print the results
        for index, line in enumerate(lines):
            if 'FIT RESULTS' in line: limit = index
            if 0 < limit <= index: print line
        print

if __name__ == '__main__':
    data_file = sys.argv[1]
    a, b, c, d = sorted([float(i) for i in sys.argv[2:6]])
    fits = main(data_file, a, b, c, d)
    for fit in fits:
        print fit
        print
