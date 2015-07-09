[![Build Status](https://travis-ci.org/Tech-XCorp/ultracold-ions.svg?branch=master)](https://travis-ci.org/Tech-XCorp/ultracold-ions)
[![Coverage Status](https://coveralls.io/repos/Tech-XCorp/ultracold-ions/badge.svg)](https://coveralls.io/r/Tech-XCorp/ultracold-ions)
[![Join the chat at https://gitter.im/Tech-XCorp/ultracold-ions](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Tech-XCorp/ultracold-ions?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


# Ultracold-ions

A framework for molecular dynamics simulations of ultracold plasmas.
The majority of ucilib is implemented in python.  Performance critical
parts are implemented in OpenCl.  The OpenCL routines can be executed
efficiently on CPUs and GPUs.


## Getting Started

To install ucilib install the [prerequisites](#prerequisites) and then
run (note that this usually requires root privileges)

    python setup.py install

For development purposes it may be advantageous to use the alternative
command

    python setup.py develop

This way any changes to the `uci` library take effect immediately (i.e.
without having to reinstall the package).


## Feedback, issues, and contributions

Please use the
[issue tracker on github](https://github.com/Tech-XCorp/ultracold-ions/issues)
for any comments, questions, and suggestions.  We are also gladly accepting
contributions and bug fixes via pull requests.  Details can be found in
the [CONTRIBUTING.md file](CONTRIBUTING.md).


## Prerequisites
<a name="prerequisites"></a>

ucilib's primary dependencies are

- Python

- numpy -- Python's defacto standard array library.

- PyOpenCL -- Python bindings for OpenCL, see 
  [PyOpenCL](http://mathema.tician.de/software/pyopencl/).

- OpenCL -- The open standard for programming heterogeneous systems, see
  [OpenCL](http://www.khronos.org/opencl/).  ucilib uses
  OpenCL 1.1 features and is forward compatible.  It should work fine
  with OpenCL 1.2 and OpenCL 2.0 platforms.  OpenCL platforms are
  available for systems with GPUs and without GPUs:

  + For NVIDIA GPUs OpenCL support is included with recent drivers.
    Code examples can be found at the [NVIDIA OpenCL page](https://developer.nvidia.com/opencl).

  + For AMD GPUs the OpenCL platform is part of the 
    [AMD APP SDK](http://developer.amd.com/tools-and-sdks/heterogeneous-computing/amd-accelerated-parallel-processing-app-sdk/).
  Additional development tools can be obtained with
  [CodeXL](http://developer.amd.com/tools-and-sdks/heterogeneous-computing/codexl/)

  For systems without GPUs high quality CPU platforms are available from
  the following sources

  + [Intel OpenCL SDK](http://software.intel.com/en-us/vcsource/tools/opencl-sdk)
  + [AMD APP SDK](http://developer.amd.com/tools-and-sdks/heterogeneous-computing/amd-accelerated-parallel-processing-app-sdk/) 

- Matplotlib (used for visualizations; not needed for running
    simulations)


### Windows


### Linux

