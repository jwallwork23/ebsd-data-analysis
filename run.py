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
if filename is None:
    raise ValueError("Enter a file to read using -f option.")

# Preprocess data
if args.r is not None:
    preproc(filename)

# Compute misorientations
ctf_reader(filename)

# Plot
if args.p is not None:
    plot_ratio(filename)
