# ebsd-data-analysis

Python package for analysing misorientation distribution.

## Usage
* In a terminal, navigate to the directory where you would like the code to reside.
* Either type `export PYTHONPATH=$(pwd)` or add this location to your `.bashrc` file.
* Clone this repo as something with no hyphens, e.g. `ebsdda`.
* Given a data file `data.ctf`, you should now be able to run the following commands:
```
from ebsdda import *

f = 'data'
preproc(f)
ctf_reader(f)
plot_ratio(f)
```

### TODO: Link for dataset
