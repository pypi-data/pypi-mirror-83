# NQontrol Servo Controller

[![pipeline status](https://gitlab.com/las-nq/nqontrol/badges/master/pipeline.svg)](https://gitlab.com/las-nq/nqontrol/commits/master)
[![coverage report](https://gitlab.com/las-nq/nqontrol/badges/master/coverage.svg)](https://gitlab.com/las-nq/nqontrol/commits/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

<img src="doc/_static/system_overview.png" align="right">

`NQontrol` is a Python project aiming the replacement of analog PID controllers in the lab.

The project is a solution based on the ADwin real-time platform that is able to deliver in excess of 8 simultaneous locking loops running with 200 kHz sampling frequency, and offers five second-order filtering sections per channel for optimal control performance. 
It can be used up to a control bandwidth of about 12 kHz.
This Python package, together with a web-based GUI, makes the system easy to use and adapt for a wide range of control tasks in quantum-optical experiments.

The source code can be found on [GitLab](https://gitlab.com/las-nq/nqontrol).

Read the latest changes in our [changelog](CHANGELOG.md).


## Paper Version

A fixed state of this project is [version 1.1](https://gitlab.com/las-nq/nqontrol/tree/v1.1).
The publicated paper about this project is available [here](https://doi.org/10.1063/1.5135873).
The preprint version of the paper describing can be found on [arXiv](https://arxiv.org/abs/1911.08824).


## Usage Example

Here is a short example for the Python API (see the [full example](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/usage.html) in the docs):

```python
# Importing a ServoDevice is enough
from nqontrol import ServoDevice

# Create a new servo device object, connecting to ADwin with the device number 0.
# Number 0 is reserved for a virtual mock device for testing.
sd = ServoDevice(0)

# Print the timestamp
print(f'Uptime {sd.timestamp}s')

# Get a servo object to control it.
s = sd.servo(1)

# Enable in and output
s.inputSw = True
s.outputSw = True

# Run a threshold analysis for locking
s.lockAnalysis()
# Enable the autolock
s.autolock(relock=True)
```


## Graphical User Interface

`NQontrol` can also be used with a responsive graphical user interface that runs in a browser (more details in the [docs](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/gui.html)):

![NQontrol GUI](doc/_static/entry.png)


## Autolock Feature

An [autolock feature](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/features.html#autolock) makes it simple to lock all the control loops.
It scans the output until a threshold value of the `aux` signal is reached, then it activates the lock.


## Documentation

For more information please read the online documentation:

* Current documentation of the [latest release](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol)
* Current documentation of the [latest development version](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol)


## NQontrol Installation

It's as simple as
```bash
pip install nqontrol
```
But additionally you need to install the ADwin library.
For complete installation instructions please refer to the [documentation page](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/install.html).


## Contribution

If you want to make changes for yourself or contribute to the project, take a look on [this page](https://las-nq-serv.physnet.uni-hamburg.de/python/nqontrol/dev_install.html) to see how to setup the environment.
