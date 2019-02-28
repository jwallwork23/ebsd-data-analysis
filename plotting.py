import matplotlib.pyplot as plt
import numpy as np


def plot_ratio(x, r, running_average=0, filename=''):
    """
    Plot ratio between average distances and average misorientations.
    """
    N = running_average

    # Take running average over 2*N+1 pixels
    if N>0:
        r = np.convolve(r, np.ones(2*N+1)/(2*N+1), mode='valid')
        plt.plot(x[N:-N], r, 'x')

    # If N == 0, just plot unaveraged data
    else:
        plt.plot(x, r, 'x')
    plt.xlabel('x')
    plt.ylabel('Average misorientation / average distance')
    plt.savefig(filename+'.pdf')


if __name__ == "__main__":

    import argparse

    # Read input from command prompt
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help="Filename to load from (excluding .ctf extension)")
    args = parser.parse_args()
    filename = args.f

    # Read data from averages file
    f = open(filename + '_averages.txt', 'r')
    xcells = int(f.readline())
    x = np.zeros(xcells)
    r = np.zeros(xcells)
    for i in range(xcells):
        xi, ri = f.readline().split()
        x[i] = float(xi)
        r[i] = float(ri)
    f.close()

    # Plot data
    plot_ratio(x, r, filename)
