import numpy as np

from ebsdda.maths import compute_misorientation, symeq


__all__ = ["ctf_reader"]


def ctf_reader(filename):
    """
    Function which takes a (reformatted) .ctf file and computes misorientations, distances and
    averages for the data therein.

    :arg filename: name of datafile, with .ctf extension removed.
    """

    # Open file, get number of x and y values
    try:
        f = open(filename + '_reordered.ctf', 'r')
    except:
        msg = "File {:s} either does not exist or needs to be reformatted using -r option."
        IOError(msg.format(filename))
    xstep = float(f.readline().split()[1])  # Get step in x-direction
    xcells = int(f.readline().split()[1])   # Get extent in x-direction
    ycells = int(f.readline().split()[1])   # Get extent in y-direction
    n = xcells*ycells                       # Total extent
    f.readline()                            # Skip headings row

    cnt = -1                  # Counter for current x-level (becomes 0 at start of first loop)
    symlist = symeq('cubic')  # Working numpy array, initialised for efficiency

    # Dictionary for data storage
    dat = {}
    dat['x'] = [xstep*i for i in range(xcells)]
    dat['dist'] = []
    dat['theta'] = []

    # Open file for output and write header
    g = open(filename + '_misorientations.ctf', 'w')
    g.write("{:6s} {:6s} {:6s} {:8s} {:8s}\n".format('X','Y1','Y2','distance','misorientation'))

    # Read each line of the file in order
    for i in range(n):
        line = f.readline()

        # Convert header titles to floating point format
        X, Y, Euler1, Euler2, Euler3 = line.split()
        X = float(X)
        Y = float(Y)
        Euler = [float(Euler1), float(Euler2), float(Euler3)]

        # If we are at the start of a slice, reset / increment variables
        if i % ycells == 0:
            cnt += 1                                 # Current x-position index
            started = False                          # Indicates misorientation calculation underway
            Euler_ = None                            # Euler angle from previous step
            dat['x'][cnt] = X        # Current x-position
            dat['dist'].append([])   # NOTE: We do not know the length of these
            dat['theta'].append([])  #       arrays a priori => dynamic allocation
            print("Y-slice {:d}/{:d} ({:.2f}% complete)".format(cnt+1,
                                                                xcells,
                                                                float(i)/float(n)*100))

        # Compute misorientation between two consecutive Euler angles using quaternions
        if Euler_ is not None:
            misorientation = compute_misorientation(Euler_, Euler, symlist=symlist)

            # If misorientation is between 1 and 10 degrees, do stuff...
            if (1. < misorientation < 10.) and not started:
                started = True
                Y_ = Y
                continue
            if (1. < misorientation < 10.) and started:
                distance = Y-Y_
                Y_ = Y
                msg = "{:6.1f} {:6.1f} {:6.1f} {:8.1f} {:8.3f}\n"
                g.write(msg.format(X, Y_, Y, distance, misorientation))
                dat['dist'][cnt].append(distance)
                dat['theta'][cnt].append(misorientation)

        # Save Euler angles from previous step
        Euler_ = Euler
    print("Done!")
    f.close()
    g.close()

    # Take averages of the misorientations and associated distances and take ratios thereof
    f = open(filename + '_averages.txt', 'w')
    f.write('XCells: {:d}\n'.format(xcells))  # TODO: Move into first loop
    for i in range(xcells):
        r = np.average(dat['theta'][i]) / np.average(dat['dist'][i])
        f.write('{:6.1f} {:6.3f}\n'.format(dat['x'][i], r))
    f.close()
