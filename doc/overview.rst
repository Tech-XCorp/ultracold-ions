Overview of major concepts
==========================


Particles
---------

Particles are represented using arrays for positions, velocities,
charge, and mass.  CPU arrays are represented with numpy arrays and GPU
arrays are represented using ``pyopencl.array`` s.  In the code we use
the convention that CPU arrays are denoted by ``x``, ``y``, etc. while
GPU arrays have ``d`` appended to the variable name, e.g. ``xd``,
``yd``, etc.  It is possible to use array views in to a larger array,
however the array views have to have unit stride.  For example, one
could have a single numpy array of dimensions 8 by N where N is the
number of particles.  Slices can then be taken for the different
coordinates::

    # Create a matrix of dimension 8xN to represent the state of all
    # particles.
    ptcl_data = np.zeros(8, N)

    # Interpret the first row in the matrix as the x-coordinate.
    x = ptcl_data[0,:]

The class ``Ptcl`` provides several convenience functions for organizing
work with particle data.


Forces
------

Forces lead to changes in velocity.  In `uci`, any class that implements
the `computeAcc` method can be used as a force.  The `computeAcc` method
computes the rate of change of the velocity.  Its signature is::

    computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
               axd, ayd, azd, t, dt)

Note that the arrays are all device arrays as indicated by the ``d``
suffix.  The coordinates of the particles are not modified by the force.
The time ``t`` enables time dependent forces.  The time step size ``dt``
is needed by forces that do not lead to a linear rate of change of the
velocity.  In ``uci``, these are typically fluctuating forces such as
laser cooling forces.  Importantly, the accelerations due to the force
under consideration are `added` to the ``axd``, ``ayd``, and ``azd``
arrays.  This allows one to accumulate the action of several forces
simply by calling their ``computeAcc`` methods one after the other, for
instance::

    # Reset the acceleration arrays to zero.
    axd.fill(0)
    ayd.fill(0)
    azd.fill(0)

    # Accumulate accelerations from several forces.
    forces = [f1, f2, f3]
    for f in forces:
        f.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md, axd, ayd, azd,
                     t, dt)


Updaters
--------

Updaters orchestrate the evaluation forces (i.e. the computation of
accelerations), velocity updates, and position updates to evolve the
state of particles by a certain amount of time.  In some libraries these
classes are referred to as integrators.  The essential method of
updaters is::

    update(xd, yd, zd, vxd, vyd, vzd, qd, md, forces, t, dt, num_steps)

The entries in the ``forces`` list have to be instances of the force
concept, see above.  Updaters are typically constructed in such a way
that the number of force evaluations is minimized.

Advances
--------

