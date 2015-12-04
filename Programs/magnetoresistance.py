import spinmob, numpy
import matplotlib.pyplot as plt
from matplotlib import pylab
from matplotlib import gridspec

def main(datafile, err):
    # load a *.txt data file (see spinmob wiki for formatting rules)
    d = spinmob.data.load(datafile)
    
    # create a fitter object (with a reasonable guess for the Rutherford file)
    f = spinmob.data.fitter('a*(x-x0)**2+b', 'a,x0,b')
    
    # set the data and error bar
    ys = d.c('R_=_V/I_(ohm)') # Ohms
    xs = d.c('B_(mT)') / 1000 # T
    es = d.c('error_V5') # V
    
    es = [numpy.sqrt(e**2 + (y*1e-4)**2 + (y*1e-4)**2) for y, e in zip(ys, es)]
    es = pylab.array(es) / 1.2
    
    a = -(ys[-1]-ys[0])/(xs[-1]**2-xs[0]**2)
    x0 = 0
    b = 65
    
    f.set_data(xs, ys, es)
    f.set(a=a, x0=x0, b=b)
    
    f.fit()
    res1 = f.results[0]
    fct1 = lambda x: res1[0] * (x - res1[1])**2 + res1[2]
    
    plt.clf()
    fig = pylab.figure()
    gs = gridspec.GridSpec(4, 4)
    TR = fig.add_subplot(gs[1:, :])
    TR.errorbar(xs, ys, es, fmt=',')
    Xs = pylab.linspace(min(xs), max(xs))
    TR.plot(Xs, fct1(Xs), '-', color='red')
    pylab.xlabel('Magnetic field ($\\times10^{-1}\\mathrm{T}$)')
    pylab.xticks(pylab.linspace(0, 0.5, 6),
        ['{:1.0f}'.format(i) for i in range(6)])
    pylab.xlim(min(xs), max(xs))
    pylab.ylabel('Resistance ($\\Omega$)')
    residual1 = fig.add_subplot(gs[0, :])
    rs = [(y - fct1(x))/e for x, y, e in zip(xs, ys, es)]
    residual1.errorbar(xs, rs, 1, fmt=',', color='blue')
    xs = pylab.linspace(min(xs), max(xs), 3)
    residual1.plot(xs, [0 for x in xs], '-', color='red')
    residual1.xaxis.tick_top()
    pylab.xticks([])
    pylab.xlim(min(xs), max(xs))
    pylab.yticks([])
    pylab.ylabel('Studentized\nresidual')
    plt.savefig('../Graphs/Magnetoresistance/Fit.png')
    plt.savefig('../Graphs/Magnetoresistance/Fit.pdf')
    return f
    
