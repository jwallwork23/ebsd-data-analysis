import numpy as np

from maths import orientation_matrix, compute_misorientation


def ctf_reader(filename):

    # Open file, get number of x and y values
    f = open(filename + '_reordered.ctf', 'r')
    xcells = int(f.readline().split()[1])
    ycells = int(f.readline().split()[1])
    f.readline()  # Skip headings row

    # Counters, etc.
    cnt = 0
    started = False
    Euler_ = None
    X_ = 0.  # Set to initial X value
    out = "X {x:6.1f} Y1 {y1:6.1f} Y2 {y2:6.1f} dist. {d:6.1f} mis. {m:6.3f}"  # For outputting

    # Dictionaries for data storage  TODO: These could probably just be lists of dicts
    dist_and_theta = {}
    averages_x = []
    averages_r = []
    dist_and_theta = {}
    averages = {}
    dist_and_theta[0] = {}
    dist_and_theta[0]['x'] = 0.
    dist_and_theta[0]['dist'] = []
    dist_and_theta[0]['theta'] = []
    averages[0] = {}
    
    # Read each line of the file in order
    for i in range(xcells*ycells):
        line = f.readline()

        # Read line from file
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
            averages[cnt] = {}
            averages_x.append(X)
            averages_r.append(np.average(dist_and_theta[cnt]['theta']))
            averages_r[cnt-1] /= np.average(dist_and_theta[cnt]['dist'])
            Euler_ = None

        # Compute misorientation between two consecutive Euler angles
        if Euler_ is not None:
            misorientation = compute_misorientation(Euler_, Euler)

            # If misorientation is greater than 5 degrees, do stuff
            if (misorientation > 5.) and not started:
                started = True
                X_ = X
                Y_ = Y
                continue
            if (misorientation > 5.) and started:
                started = False
                distance = Y-Y_
                print(out.format(x=X,y1=Y_,y2=Y,d=distance,m=misorientation))
                # TODO: Print to file
                dist_and_theta[cnt]['dist'].append(distance)
                dist_and_theta[cnt]['theta'].append(misorientation)

        # Save values from previous step
        X_ = X
        Y_ = Y
        Euler_ = Euler
    print('Done!')
    f.close()
    g.close()

    return averages_x, averages_r


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help="Filename to load from (excluding .ctf extension)")
    parser.add_argument('-r', help="Reorder data storage X-Y precedence using preprocessor")
    parser.add_argument('-p', help="Plot results")
    args = parser.parse_args()

    # Preprocess data, if requested
    if args.r:
        import preproc
        preproc.preproc(filename)

    # Compute misorientations
    x, r = ctf_reader(args.f)
    f = open('averages.txt', 'w')
    for i in range(len(x)):
        f.write('{:6.3f} {:6.3f}\n'.format(x[i], r[i]))
    f.close()

    # Plot, if requested
    if args.p:
        import plotting
        plotting.plot_ratio(x, r, args.f)
