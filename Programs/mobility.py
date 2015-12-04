#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy
from matplotlib import gridspec
import scipy, scipy.interpolate

def fit_exp(Ts, Rs, Rerr, eguess):
    'Fit an exponential function to the data'
    Rs, Rerr = pylab.array(Rs), pylab.array(Rerr)
    model, ps = 'a * exp(b / x)', 'a,b'
    # Make intelligent guesses for the parameters
    a, b = eguess
    b = pylab.log(Rs[0]/Rs[1]) / ( Rs[-1] - Rs[0] )
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, b=b) # Set guesses
    # Fit.
    fitter.fit()
    return fitter

def fit_power(Ts, Rs, Rerr, pguess):
    'Fit a power function to the data'
    Rs, Rerr = pylab.array(Rs), pylab.array(Rerr)
    model, ps = 'a * (x-x0)**(3/2)', 'a,x0'
    # Make intelligent guesses for the parameters
    a, x0 = pguess
    # Create a spinmob fitter
    fitter = spinmob.data.fitter(model, ps)
    fitter.set_data(Ts, Rs, Rerr)
    fitter.set(a=a, x0=x0) # Set guesses
    # Fit.
    fitter.fit()
    return fitter

def splitfit(Ts, Rs, es, a, b, c, d, pguess, eguess, outfile=None):
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
    fct2 = lambda x: res2[0] * pylab.exp(res2[1]/x)
    pylab.clf()
    make_fig(Ts, Rs, es, a, b, c, d, fct1, fct2, outfile)
    return '', ''

def make_fig(Ts, Rs, es, outfile):
    fig = pylab.figure()
    gs = gridspec.GridSpec(4, 4)
    TR = fig.add_subplot(gs[:, :])
    TR.errorbar(Ts, Rs, es, fmt=',', color='blue')
    #TR.plot(Ts, Rs, '.', color='blue')
    pylab.xlim(200, 400)
    #pylab.yticks(list(pylab.linspace(0, 25e-2, 6)),
    #    ['{:.0f}'.format(i) for i in pylab.linspace(0, 25, 6)])
    #pylab.ylim(0, 2e-1)
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Mobility ($\\mathrm{T}^{-1}$)')
    if not outfile: outfile = 'Fits'
    fig.savefig('../Graphs/Mobility/'+outfile+'.png')
    fig.savefig('../Graphs/Mobility/'+outfile+'.pdf')

def interpolate(databox):
    x, V, e, N = databox[:4]
    V = [y for j, y in zip(x, V) if 200 <= j <= 400]
    N = [y for j, y in zip(x, N) if 200 <= j <= 400]
    x = [j for j in x if 200 <= j <= 400]
    f1 = scipy.interpolate.interp1d(x, V, kind='cubic')
    f2 = scipy.interpolate.interp1d(x, N, kind='cubic')
    mini, maxi = int(min(x))+1, int(max(x))-1
    V = [f1(i) for i in range(mini, maxi)]
    N = [f2(i)/4 for i in range(mini, maxi)]
    x = [i for i in range(mini, maxi)]
    return x, V, N

def main(data_files1, data_files2,
         err, B=0.5003991, l=2e-2, w=1e-2,
         outfile=None):
    mu_H = lambda V_5, V_1: V_5 * l / ( V_1 * B * w)
    mu_He = lambda V_5, V_1, V_5e, V_1e: pylab.sqrt(\
                ( (l / ( V_1 * B * w)) * V_5e )**2 +\
                ( (V_5 / ( V_1 * B * w)) * 1e-4 )**2 +\
                ( (V_5 * l / ( V_1 * B * w)) * 1e-4 )**2 +\
                ( (V_5 * l / ( V_1**2 * B * w)) * V_1e )**2 +\
                ( (V_5 * l / ( V_1 * B**2 * w)) * 2e-8 )**2 +\
                ( (V_5 * l / ( V_1 * B * w**2)) * 1e-4 )**2)
    x5, x1, V5, V1, N5, N1 = [], [], [], [], [], []
    for df in data_files1:
        databox = spinmob.data.load(df)
        x, V, N = interpolate(databox)
        x5 += x
        V5 += V
        N5 += N
    for df in data_files2:
        databox = spinmob.data.load(df)
        x, V, N = interpolate(databox)
        x1 += x
        V1 += V
        N1 += N
    min_len = min([len(x5), len(x1)])
    xs = pylab.array(x5[:min_len])
    V5, V1 = pylab.array(V5[:min_len]), pylab.array(V1[:min_len])
    N5, N1 = pylab.array(N5[:min_len]), pylab.array(N1[:min_len])
    e5, e1 = err / pylab.sqrt(N5), err / pylab.sqrt(N1)
    ys, es = mu_H(V5, V1), mu_He(V5, V1, e5, e1)
    make_fig(xs, ys, es, outfile)
