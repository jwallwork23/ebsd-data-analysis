import matplotlib.pyplot as plt


def plot_ratio(x, r, filename=''):
    """
    Plot ratio between average distances and average misorientations.
    """
    plt.plot(x, r)
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
