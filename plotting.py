import matplotlib.pyplot as plt


def plot_ratio(x, r, filename=''):
    """
    Plot ratio between average distances and average misorientations.
    """
    plt.plot(x, r)
    plt.xlabel('x')
    plt.ylabel('Average misorientation / average distance')
    plt.savefig(filename+'.pdf')

