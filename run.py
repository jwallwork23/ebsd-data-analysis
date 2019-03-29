from preproc import preproc
from ctf_reader import ctf_reader
from plotting import plot_ratio

import argparse


# Read input from command prompt
parser = argparse.ArgumentParser()
parser.add_argument('-f', help="Filename to load from (excluding .ctf extension)")
parser.add_argument('-r', help="Reorder data storage X-Y precedence using preprocessor")
parser.add_argument('-p', help="Plot results")
args = parser.parse_args()
filename = args.f

# Preprocess data, if requested
if args.r is not None:
    preproc(filename)

# Compute misorientations
if args.f is None:
    raise ValueError("Enter a file to read using -f option.")
try:
    x, r = ctf_reader(args.f)
except:
    msg = "Requested file {:s} either does not exist or cannot be opened."
    raise ValueError(msg.format(args.f))
f = open(filename + '_averages.txt', 'w')
f.write('{:d}\n'.format(len(x)))
for i in range(len(x)):
    f.write('{:6.1f} {:6.3f}\n'.format(x[i], r[i]))
f.close()

# Plot, if requested
if args.p is not None:
    plot_ratio(filename, args.f)
