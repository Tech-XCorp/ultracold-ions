import uci.BorisUpdater as BorisUpdater
import uci.CoulombAccScaled as CoulombAccScaled
import uci.Ptcls as Ptcls
import numpy as np
import pyopencl as cl
import pyopencl.array as cl_array
import argparse
import sys

parser = argparse.ArgumentParser(
        description=
        """Simulate evolution of a plasma starting from a random
        configuration""")
parser.add_argument('-t', '--tmax',
        nargs=1,
        help='Duration of simulation in plasma periods',
        type=float,
        default=1.0)
parser.add_argument('-d', '--dt',
        nargs=1,
        help='Integrator time step size',
        type=float,
        default=0.01)
parser.add_argument('-n', '--n_ions',
        nargs=1,
        help='Number of ions/electrons',
        type=int,
        default=250)
parser.add_argument('-o', '--num_dump',
        nargs=1,
        help='Number of time steps between dumps of plasma state',
        type=int,
        default=10)

class UsageError(Exception):
    def __init__(self, msg):
        self.msg = msg

Epsilon = 8.854187817620e-12
fund_charge_SI = 1.602176565e-19
fund_charge = 1.0
atomic_unit = 1.836152675241972e+03
ion_mass = 29.783981668036578 * atomic_unit
electron_mass_SI = 9.10938291e-31
electron_mass = 1.0
kB = 1.3806e-23

def run_simulation(n_ions, dt, tmax, num_dump = 1):
    # initialize particles
    ptcls = Ptcls.Ptcls()
    ptcls.set_nptcls(2 * n_ions)
    density = 1.0e+18
    volume = n_ions / density
    l = (3 * volume / 4 / np.pi)**(1./3.)
    a_ws = (3 /( 4 * np.pi * density))**(1./3.)
    l = l / a_ws
    # electron plasma frequency is used to scale time t -> t * w_e
    w_e = np.sqrt(density * fund_charge_SI**2 / (electron_mass_SI * Epsilon))

    # ions
    i = 0
    while i < n_ions:
        xt = (np.random.random()-0.5)*l*2
        yt = (np.random.random()-0.5)*l*2
        zt = (np.random.random()-0.5)*l*2
        rt = np.sqrt(xt**2+yt**2+zt**2)
        if rt <= l:
            ptcls.x()[i] = xt
            ptcls.y()[i] = yt
            ptcls.z()[i] = zt
            i += 1
    ptcls.ptclList[3:6,:n_ions] = 0
    ptcls.ptclList[6,:n_ions] = fund_charge
    ptcls.ptclList[7,:n_ions] = ion_mass

    #electrons
    i = 0
    while i < n_ions:
        xt = (np.random.random()-0.5)*l*2
        yt = (np.random.random()-0.5)*l*2
        zt = (np.random.random()-0.5)*l*2
        rt = np.sqrt(xt**2+yt**2+zt**2)
        if rt <= l:
            ptcls.x()[n_ions+i] = xt
            ptcls.y()[n_ions+i] = yt
            ptcls.z()[n_ions+i] = zt
            i += 1
  
    electron_temperature = 3.0
    vThermal = np.sqrt(kB * electron_temperature / electron_mass_SI)
    vThermal = vThermal / (a_ws * w_e)
    ptcls.ptclList[3:6,n_ions:] = np.random.normal(
            0.0, vThermal, ptcls.ptclList[3:6,n_ions:].shape)
    ptcls.ptclList[6,n_ions:] = -fund_charge
    ptcls.ptclList[7,n_ions:] = electron_mass


    ctx = cl.create_some_context(interactive = True)
    queue = cl.CommandQueue(ctx)
    coulomb_acc = CoulombAccScaled.CoulombAccScaled(ctx, queue)
    accelerations = [coulomb_acc]
    updater = BorisUpdater.BorisUpdater(ctx, queue)

    xd = cl_array.to_device(queue, ptcls.x())
    yd = cl_array.to_device(queue, ptcls.y())
    zd = cl_array.to_device(queue, ptcls.z())
    vxd = cl_array.to_device(queue, ptcls.vx())
    vyd = cl_array.to_device(queue, ptcls.vy())
    vzd = cl_array.to_device(queue, ptcls.vz())
    qd = cl_array.to_device(queue, ptcls.q())
    md = cl_array.to_device(queue, ptcls.m())
    
    t = 0.0
    while t < tmax:
        #np.save('data\ptcls' + str(t) + '.npy',ptcls.ptclList[0:6,:])
        np.savetxt('data\ptcls' + str(t) + '.txt',ptcls.ptclList[0:6,:])
        t = updater.update(
                xd, yd, zd, vxd, vyd, vzd, qd, md, accelerations, t, dt,
                num_dump)
        xd.get(queue, ptcls.x())
        yd.get(queue, ptcls.y())
        zd.get(queue, ptcls.z())
        vxd.get(queue, ptcls.vx())
        vyd.get(queue, ptcls.vy())
        vzd.get(queue, ptcls.vz())

    np.savetxt('data\ptcls' + str(t) + '.txt',ptcls.ptclList[0:6,:])

def main(argv=None):
    try:
        try:
            args = parser.parse_args(argv)
        except Exception as msg:
            raise UsageError(msg)

        run_simulation(args.n_ions, args.dt, args.tmax, args.num_dump)

    except UsageError as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, 'For help use --help'
        return 2

if __name__ == '__main__':
    sys.exit(main())