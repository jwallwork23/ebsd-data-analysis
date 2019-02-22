import matplotlib.pyplot as plt


def plot_ratio(x, r, filename=''):
    plt.plot(x, r)
    plt.xlabel('x')
    plt.ylabel('Average misorientation / average distance')
    plt.savefig(filename+'.pdf')

