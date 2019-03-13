import numpy as np


def preproc(filename):
    """
    Take in a .ctf file and exchange the X-Y column ordering precedence, so as to easily compute
    misorientations in a strip in the Y-direction.
    """

    # Create file and read 'boiler plate' at top
    f = open(filename+'.ctf', 'r')
    for i in range(4):
        f.readline()
    xcells = int(f.readline().split()[1])
    ycells = int(f.readline().split()[1])
    xstep = float(f.readline().split()[1])
    ystep = float(f.readline().split()[1])
    for i in range(7):
        f.readline()
    n = xcells*ycells

    # Preallocate arrays for data storage
    euler1 = np.zeros(n)
    euler2 = np.zeros(n)
    euler3 = np.zeros(n)

    # Reorder X and Y precedence (i.e. take slices in Y rather than X)
    for j in range(ycells):
        for i in range(xcells):
            line = f.readline()
            phase, X, Y, Bands, Error, Euler1, Euler2, Euler3, MAD, BC, BS = line.split()
            euler1[i*ycells+j] = float(Euler1)
            euler2[i*ycells+j] = float(Euler2)
            euler3[i*ycells+j] = float(Euler3)

    # Print to file
    f = open(filename+'_reordered.ctf', 'w')
    f.write("XStep {:.1f}\n".format(xstep))
    f.write("XCells {:d}\n".format(xcells))
    f.write("YCells {:d}\n".format(ycells))
    f.write("X       Y       Euler1  Euler2  Euler3\n")
    msg = "{:.5f}  {:.5f}  {:.5f}  {:.5f}  {:.5f}\n"
    for i in range(xcells):
        for j in range(ycells):
            f.write(msg.format(xstep*i,ystep*j,euler1[i*ycells+j],euler2[i*ycells+j],euler3[i*ycells+j]))
    f.close()
