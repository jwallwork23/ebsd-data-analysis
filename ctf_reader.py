import numpy as np
import os

from maths import orientation_matrix, compute_misorientation


def ctf_reader(filename):
    """
    Function which takes a (reformatted) .ctf file and computes misorientations, distances and
    averages for the data therein.
    """

    # Open file, get number of x and y values
    try:
        f = open(os.path.join(filename, '_reordered.ctf'), 'r')
    except:
        msg = "File {:s} either does not exist or needs to be reformatted using -r option."
        IOError(msg.format(filename))
    xstep = float(f.readline().split()[1])  # Get step in x-direction
    xcells = int(f.readline().split()[1])   # Get extent in x-direction
    ycells = int(f.readline().split()[1])   # Get extent in y-direction
    n = xcells*ycells                       # Total extent
    f.readline()                            # Skip headings row

    # Counters, etc.
    cnt = 0
    started = False  # Boolean variable to indicate misorientation calculation
    Euler_ = None    # Previous Euler angle
    X_ = 0.          # Previous X value (Set to initial X value)
    out = "X {x:6.1f} Y1 {y1:6.1f} Y2 {y2:6.1f} dist. {d:6.1f} mis. {m:6.3f}"  # For outputting

    # Dictionaries for data storage  TODO: These could probably just be lists of dicts
    dist_and_theta = {}
    dist_and_theta[0] = {}
    dist_and_theta[0]['x'] = 0.
    dist_and_theta[0]['dist'] = []
    dist_and_theta[0]['theta'] = []

    # Open file for output
    g = open(os.path.join('_misorientations.txt'), 'w')
    g.write('{:6s} {:6s} {:6s} {:8s} {:8s}\n'.format('X','Y1','Y2','distance','misorientation'))
    
    # Read each line of the file in order
    for i in range(n):
        line = f.readline()

        # Read line from file and convert to floating point
        X, Y, Euler1, Euler2, Euler3 = line.split()
        X = float(X)
        Y = float(Y)
        Euler = [float(Euler1), float(Euler2), float(Euler3)]

        # If we move onto a new slice, compute averages of data accumulated
        if X != X_:
            started = False
            cnt += 1
            dist_and_theta[cnt] = {}
            dist_and_theta[cnt]['x'] = X
            dist_and_theta[cnt]['dist'] = []
            dist_and_theta[cnt]['theta'] = []
            Euler_ = None

        # Compute misorientation between two consecutive Euler angles
        if Euler_ is not None:
            misorientation = compute_misorientation(Euler_, Euler)

            # If misorientation is greater than 5 degrees, do stuff...
            if (misorientation > 5.) and not started:
                started = True
                X_ = X
                Y_ = Y
                continue
            if (misorientation > 5.) and started:
                started = False
                distance = Y-Y_
                if i % 10 == 0:
                    print('{:.2f}% complete'.format(float(i)/float(n)*100))
                g.write('{:6.1f} {:6.1f} {:6.1f} {:8.1f} {:8.3f}\n'.format(X,Y_,Y,distance,misorientation))
                dist_and_theta[cnt]['dist'].append(distance)
                dist_and_theta[cnt]['theta'].append(misorientation)

        # Save values from previous step
        X_ = X
        Y_ = Y
        Euler_ = Euler
    print('Done!')
    averages = np.zeros(xcells)
    x_values = np.zeros(xcells)
    for i in range(xcells):
        averages[i] = np.average(dist_and_theta[i]['theta']) / np.average(dist_and_theta[i]['dist'])
        x_values[i] = (i+1)*xstep
    f.close()
    g.close()

    return x_values, averages


if __name__ == "__main__":

    import argparse

    # Read input from command prompt
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help="Filename to load from (excluding .ctf extension)")
    parser.add_argument('-r', help="Reorder data storage X-Y precedence using preprocessor")
    parser.add_argument('-p', help="Plot results")
    args = parser.parse_args()
    filename = args.f

    # Preprocess data, if requested
    if args.r:
        import preproc
        preproc.preproc(filename)

    # Compute misorientations
    if args.f is None:
        raise ValueError("Enter a file to read using -f option.")
    try:
        x, r = ctf_reader(args.f)
    except:
        msg = "Requested file {:s} either does not exist or cannot be opened."
        raise ValueError(msg.format(args.f))
    f = open(os.path.join(filename, '_averages.txt'), 'w')
    f.write('{:d}\n'.format(len(x)))
    for i in range(len(x)):
        f.write('{:6.1f} {:6.3f}\n'.format(x[i], r[i]))
    f.close()

    # Plot, if requested
    if args.p:
        import plotting
        plotting.plot_ratio(x, r, args.f)
