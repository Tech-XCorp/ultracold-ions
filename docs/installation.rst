Installation
============


To install ucilib install the :ref:`prerequisites <prerequisites>`)
and then run (note that this usually requires root privileges)::

    python setup.py install

For development purposes it may be advantageous to use the alternative
command::

    python setup.py develop

This way any changes to the `uci` library take effect immediately (i.e.
without having to reinstall the package).


.. _prerequisites:

Prerequisites
-------------

uci's primary dependencies are

- Python

- numpy -- Python's defacto standard array library.

- PyOpenCL -- Python bindings for OpenCL, see 
  http://mathema.tician.de/software/pyopencl/.

- OpenCL -- The open standard for programming heterogeneous systems, see
  http://www.khronos.org/opencl/.  uci uses
  OpenCL 1.1 features and is forward compatible.  It should work fine
  with OpenCL 1.2 and OpenCL 2.0 platforms.  OpenCL platforms are
  available for systems with GPUs and without GPUs:

  + For NVIDIA GPUs OpenCL support is included with recent drivers.
    Code examples can be found at https://developer.nvidia.com/opencl.

  + For AMD GPUs the OpenCL platform is part of the 
    http://developer.amd.com/tools-and-sdks/heterogeneous-computing/amd-accelerated-parallel-processing-app-sdk/.  Additional development tools can be obtained with http://developer.amd.com/tools-and-sdks/heterogeneous-computing/codexl/

For systems without GPUs high quality CPU platforms are available from
the following sources

  + http://software.intel.com/en-us/vcsource/tools/opencl-sdk
  + http://developer.amd.com/tools-and-sdks/heterogeneous-computing/amd-accelerated-parallel-processing-app-sdk/ 

- Matplotlib (used for visualizations; not needed for running simulations)


Windows
-------


Linux
-----

