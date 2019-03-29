import numpy as np

from ebsdda.maths import compute_misorientation


__all__ = ["ctf_reader"]


def ctf_reader(filename):
    """
    Function which takes a (reformatted) .ctf file and computes misorientations, distances and
    averages for the data therein.
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

    cnt = -1  # Counter for current x-level (becomes 0 at start of first loop)

    # Dictionary for data storage
    dat = {}
    dat['x'] = [xstep*i for i in range(xcells)]
    dat['dist'] = []
    dat['theta'] = []

    # Open file for output and write header
    g = open(filename + '_misorientations.txt', 'w')
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

        # Compute misorientation between two consecutive Euler angles
        if Euler_ is not None:
            misorientation = compute_misorientation_quat(Euler_, Euler)

            # If misorientation is greater than 5 degrees, do stuff...
            if (1. < misorientation < 10.) and not started:
                started = True
                Y_ = Y
                continue
            if (1. < misorientation < 10.) and started:
                distance = Y-Y_
                Y_ = Y
                msg = "{:6.1f} {:6.1f} {:6.1f} {:8.1f} {:8.3f}\n"
                g.write(msg.format(X,Y_,Y,distance,misorientation))
                dat['dist'][cnt].append(distance)
                dat['theta'][cnt].append(misorientation)

        # Save Euler angles from previous step
        Euler_ = Euler

        # Print progress to screen every 100 steps
        if i % 100 == 0:
            print("{:.2f}% complete".format(float(i)/float(n)*100))
    print("Done!")

    # Take averages of the misorientations and associated distances and return ratios thereof
    averages = np.zeros(xcells)
    for i in range(xcells):
        averages[i] = np.average(dat['theta'][i])
        averages[i] /= np.average(dat['dist'][i])
    f.close()
    g.close()

    return dat['x'], averages
