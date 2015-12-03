#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spinmob, glob, sys, matplotlib.pylab as pylab, scipy
from matplotlib import gridspec

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

def make_fig(Ts, Rs, es, a, b, c, d, fct1, fct2, outfile):
    fig = pylab.figure()
    gs = gridspec.GridSpec(4, 4)
    TR = fig.add_subplot(gs[:, :])
    TR.errorbar(Ts, Rs, 2e-8, fmt=',')
    xs = pylab.linspace(a, b, 100)
    #TR.plot(xs, fct1(xs), '-', color='red')
    xs = pylab.linspace(c, d, 100)
    #TR.plot(xs, fct2(xs), '-', color='red')
    pylab.xlim(160, 400)
    pylab.yticks(list(pylab.linspace(-5e-4, 3.5e-4, 8)),
        ['{:1.1f}'.format(i) for i in pylab.linspace(-5, 3.5, 8)])
    pylab.ylim(-1e-4, 3.5e-4)
    pylab.xlabel('Temperature (K)')
    pylab.ylabel('Hall coefficient ($10^{-4}\\,\\mathrm{m}^3/\\mathrm{C}$)')
    room_T, nominal_R_H, nRHe = 293, 1.47e-4, 0.01e-4
    TR.errorbar([room_T], [nominal_R_H], nRHe, fmt='.', color='green')
    if not outfile: outfile = 'Fits'
    fig.savefig('../Graphs/Hall/'+outfile+'.png')
    fig.savefig('../Graphs/Hall/'+outfile+'.pdf')

def main(data_files, a, b, c, d, pguess, eguess, perr=1, eerr=1,
         I=0.001, B=0.5003991, sample_thickness=1e-3,
         outfile=None):
    R_H = lambda V_H: V_H*sample_thickness / (I*B) # Vm/AT
    R_He = lambda V_H, V_He: pylab.sqrt( ( sample_thickness/(I*B) * V_He )**2 + \
                ( V_H / (I*B) * 1e-4 )**2 + \
                ( V_H * sample_thickness / (B**2 * I) * 2e-8 )**2 )
    xs, ys, es, Ns = [], [], [], []
    for df in data_files:
        databox = spinmob.data.load(df)
        x, y, e, N = databox[:4]
        xs += list(x)
        ys += [R_H(abs(i)) for i in y]
        es += [R_He(abs(i), j) for i, j in zip(y, e)]
        Ns += list(N)
    xs, ys, es, Ns = pylab.array(xs), pylab.array(ys), pylab.array(es), pylab.array(Ns)
    pes, ees = perr / pylab.sqrt(Ns), eerr / pylab.sqrt(Ns)
    fits = splitfit(xs, ys, (pes, ees), a, b, c, d, pguess, eguess, outfile)
    return fits

if __name__ == '__main__':
    data_file = sys.argv[1]
    a, b, c, d = sorted([float(i) for i in sys.argv[2:6]])
    fits = main(data_file, a, b, c, d)
    for fit in fits:
        print fit
        print
