#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy
from matplotlib import gridspec

def fit_exp(Ts, Rs, Rerr, eguess):
    'Fit an exponential function to the data'
    Rs, Rerr = pylab.array(Rs), pylab.array(Rerr)
    model, ps = 'a * exp(b * x)', 'a,b'
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
    model, ps = 'a * (x-x0)', 'a,x0'
    # Make intelligent guesses for the parameters
    a, x0 = pguess
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, x0=x0) # Set guesses
    fitter.set(xlabel='Temperature (K)',
               ylabel='Resistance ($\Omega$)')
    # Fit.
    fitter.fit()
    #pylab.savefig('../Graphs/RvsT/fit_power.png')
    #pylab.savefig('../Graphs/RvsT/fit_power.pdf')
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
    res1 = fit1.results[0]
    res2 = fit2.results[0]
    fct1 = lambda x: res1[0] * (x - res1[1])
    fct2 = lambda x: res2[0] * pylab.exp(res2[1]*x)
    pylab.clf()
    fig = pylab.figure()
    gs = gridspec.GridSpec(4, 4)
    TR = fig.add_subplot(gs[1:, :])
    TR.errorbar(Ts, Rs, es[0], fmt=',')
    xs = pylab.linspace(a, b, 100)
    TR.plot(xs, fct1(xs), '-', color='red')
    xs = pylab.linspace(c, d, 100)
    TR.plot(xs, fct2(xs), '-', color='red')
    pylab.xlim(200, 390)
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Resistance ($\\Omega$)')
    # Plot the other run
    sw6 = spinmob.data.load('../Data/Resistance against temperature/Nov12/slow_warming.6')
    TR.plot(sw6[0], -sw6[1]/0.001, ',', color='grey')
    residual1 = fig.add_subplot(gs[0, :2])
    xs = [x for x in Ts if a <= x <= b]
    ys = [(y - fct1(x))/e for x, y, e in zip(Ts, Rs, es[0]) if a <= x <= b]
    residual1.errorbar(xs, ys, 1, fmt=',', color='blue')
    xs = pylab.linspace(a, b, 100)
    residual1.plot(xs, [0 for x in xs], '-', color='red')
    residual1.xaxis.tick_top()
    pylab.xlim(a, b)
    pylab.xticks([a+1, b-1])
    #pylab.ylim(-1, 1)
    pylab.ylabel('Residual')
    residual2 = fig.add_subplot(gs[0, 2:])
    xs = [x for x in Ts if c <= x <= d]
    ys = [(y - fct2(x))/e for x, y, e in zip(Ts, Rs, es[1]) if c <= x <= d]
    residual2.errorbar(xs, ys, 1, fmt=',', color='blue')
    xs = pylab.linspace(c, d, 100)
    residual2.plot(xs, [0 for x in xs], '-', color='red')
    residual2.xaxis.tick_top()
    pylab.xticks([c+1, d-1])
    #pylab.ylim(-1, 1)
    residual2.yaxis.tick_right()
    pylab.xlim(c, d)
    fig.savefig('../Graphs/Fits.png')
    fig.savefig('../Graphs/Fits.pdf')
    # Zoom in
    pylab.clf()
    pylab.xlim(a, b)
    pylab.errorbar(Ts, Rs, es[0], fmt=',')
    xs = pylab.linspace(a, b, 100)
    pylab.plot(xs, fct1(xs), '-')
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Resistance ($\\Omega$)')
    pylab.savefig('../Graphs/Fits_power.png')
    pylab.savefig('../Graphs/Fits_power.pdf')
    # Zoom in on exp
    pylab.clf()
    pylab.xlim(c, d)
    pylab.errorbar(Ts, Rs, es[0], fmt=',')
    xs = pylab.linspace(c, d, 100)
    pylab.plot(xs, fct2(xs), '-')
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Resistance ($\\Omega$)')
    pylab.savefig('../Graphs/Fits_exp.png')
    pylab.savefig('../Graphs/Fits_exp.pdf')
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
