import numpy as np


__all__ = ["preproc"]


def preproc(filename):
    """
    Read in a .ctf file, exchange the X-Y column ordering precedence and strip out data which is
    irrelevant for our purposes. This allows us to more efficiently compute misorientations in a
    strip in the Y-direction.

    :arg filename: name of datafile, with .ctf extension removed.
    """
    try:
        f = open(filename + '.ctf', 'r')
    except:
        msg = "Requested file '{:s}' either does not exist or cannot be opened."
        raise ValueError(msg.format(filename))

    # Create file and read 'boiler plate' at top
    for i in range(4):
        f.readline()
    xcells = int(f.readline().split()[1])
    ycells = int(f.readline().split()[1])
    n = xcells*ycells
    xstep = float(f.readline().split()[1])
    ystep = float(f.readline().split()[1])
    first_label = ''
    while first_label != 'Phase':
        first_label = f.readline().split()[0]  # Once we hit the headings, we are done

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

    # Print to file  TODO: could work with .npy files
    f = open(filename + '_reordered.ctf', 'w')
    f.write("XStep {:.1f}\n".format(xstep))
    f.write("XCells {:d}\n".format(xcells))
    f.write("YCells {:d}\n".format(ycells))
    f.write("X       Y       Euler1  Euler2  Euler3\n")
    msg = "{:.5f}  {:.5f}  {:.5f}  {:.5f}  {:.5f}\n"
    for i in range(xcells):
        for j in range(ycells):
            f.write(msg.format(xstep*i,
                               ystep*j,
                               euler1[i*ycells+j],
                               euler2[i*ycells+j],
                               euler3[i*ycells+j]))
    f.close()
