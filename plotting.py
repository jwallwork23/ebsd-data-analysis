import matplotlib.pyplot as plt
import numpy as np


__all__ = ["plot_ratio"]


def plot_ratio(filename, running_average=0):
    """
    Plot ratio between average distances and average misorientations.

    :arg filename: name of datafile, with .ctf extension removed.
    :kwarg running_average: optionally take a running average of the data, over each sequence of 
                            2*N+1 consecutive pixel, where N = `running_average`. If N == 0 then
                            the data is plotted without the computation of a running average.
    """

    # Read from file  TODO: .npy file would make this easier
    try:
        f = open(filename + '_averages.txt', 'r')
    except:
        msg = "Requested file '{:s}' has not yet been averaged. Please run `ctf_reader`."
        raise ValueError(msg.format(filename))
    xcells = int(f.readline().split()[1])
    x = np.zeros(xcells)
    r = np.zeros(xcells)
    for i in range(xcells):
        xi, ri = f.readline().split()
        x[i] = float(xi)
        r[i] = float(ri)
    f.close()

    # Take running average over 2*N+1 pixels
    N = running_average
    if N>0:
        r = np.convolve(r, np.ones(2*N+1)/(2*N+1), mode='valid')
        plt.plot(x[N:-N], r, 'x')

    # If N == 0, just plot unaveraged data
    else:
        plt.plot(x, r, 'x')
    plt.xlabel('x')
    plt.ylabel('Average misorientation / average distance')
    plt.savefig(filename+'.pdf')
