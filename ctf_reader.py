import numpy as np
#import matplotlib.pyplot as plt
from math import cos, sin, acos


def orientation_matrix(euler_angle):

    # Convert from degrees to radians
    phi1 = np.deg2rad(euler_angle[0])
    Phi  = np.deg2rad(euler_angle[1])
    phi2 = np.deg2rad(euler_angle[2])

    # Assemble orientation matrix
    M = np.zeros([3, 3])
    M[0,0] = cos(phi1)*cos(phi2) - sin(phi1)*sin(phi2)*cos(Phi)
    M[0,1] = sin(phi1)*cos(phi2) - cos(phi1)*sin(phi2)*cos(Phi)
    M[0,2] = sin(phi2)*sin(Phi)
    M[1,0] = -cos(phi1)*sin(phi2) - sin(phi1)*cos(phi2)*cos(Phi)
    M[1,1] = -sin(phi1)*sin(phi2) + cos(phi1)*cos(phi2)*cos(Phi)
    M[1,2] = cos(phi2)*sin(Phi)
    M[2,0] = sin(phi1)*sin(Phi)
    M[2,1] = -cos(phi1)*sin(Phi)
    M[2,2] = cos(Phi)
    return M


def compute_misorientation(euler_angle1, euler_angle2):

    # Assemble orientation matrices
    M1 = orientation_matrix(euler_angle1)
    M2 = orientation_matrix(euler_angle2)

    # Calculate misorientation
    M = M1*np.linalg.inv(M2)

    # Get angle
    cosTheta = (M[0,0]+M[1,1]+M[2,2]-1.)/2

    return np.rad2deg(acos(cosTheta))


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
            averages_r[cnt] /= np.average(dist_and_theta[cnt]['dist'])
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
    f.close()

    return averages_x, averages_r


#def plot_ratio(x, r, filename=''):
#    plt.plot(x, r)
#    plt.xlabel('x')
#    plt.ylabel('Average misorientation / average distance')
#    plt.savefig(filename+'.pdf')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help="Filename to load from (excluding .ctf extension)")
    args = parser.parse_args()

    x, r = ctf_reader(args.f)
    #plot_ratio(x, r, args.f)
