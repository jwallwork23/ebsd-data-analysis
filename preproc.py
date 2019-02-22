import numpy as np


def preproc(filename):
    f = open(filename+'.ctf', 'r')
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    xcells = int(f.readline().split()[1])
    ycells = int(f.readline().split()[1])
    xstep = float(f.readline().split()[1])
    ystep = float(f.readline().split()[1])
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    f.readline()
    n = xcells*ycells

    euler1 = np.zeros(n)
    euler2 = np.zeros(n)
    euler3 = np.zeros(n)

    for j in range(ycells):
        for i in range(xcells):

            line = f.readline()
            phase, X, Y, Bands, Error, Euler1, Euler2, Euler3, MAD, BC, BS = line.split()
            euler1[i*ycells+j] = float(Euler1)
            euler2[i*ycells+j] = float(Euler2)
            euler3[i*ycells+j] = float(Euler3)

    f = open(filename+'_reordered.ctf', 'w')
    f.write("XCells {:d}\n".format(xcells))
    f.write("YCells {:d}\n".format(ycells))
    f.write("X       Y       Euler1  Euler2  Euler3\n")
    msg = "{:.5f}  {:.5f}  {:.5f}  {:.5f}  {:.5f}\n"
    for i in range(xcells):
        for j in range(ycells):
            f.write(msg.format(xstep*i,ystep*j,euler1[i*ycells+j],euler2[i*ycells+j],euler3[i*ycells+j]))
    f.close()
