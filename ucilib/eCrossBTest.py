import CyclAdvance
import BendKickUpdater
import TrapConfiguration
import ConstantEAcc
import Ptcls
import pyopencl as cl
import pyopencl.array as cl_array

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig_width_pt = 8.0*72/2.54  # Get this from LaTeX using \showthe\columnwidth
inches_per_pt = 1.0/72.27               # Convert pt to inch
golden_mean = (np.sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height = fig_width*golden_mean      # height in inches
fig_size =  [fig_width,fig_height]

params = {'backend': 'ps',
    'axes.labelsize': 10,
    'text.fontsize': 10,
    'legend.fontsize': 10,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'text.usetex': True,
    'figure.figsize': fig_size}

plt.rcParams.update(params)


class Sim():

    accList = []
    ptcls = Ptcls.Ptcls()
    t = 0

    def __init__(self, ctx = None, queue = None):
        self.ctx = ctx
        self.queue = queue
        if self.ctx == None:
            self.ctx = cl.create_some_context()
        if self.queue == None:
            self.queue = cl.CommandQueue(self.ctx,
                properties=cl.command_queue_properties.PROFILING_ENABLE)

        self.updater = BendKickUpdater.BendKickUpdater(self.ctx, self.queue)

    def init_sim(self, Bz, Ex, Ey):
        self.updater.trapConfiguration.Bz = Bz

        self.accList = []

        fieldKick = ConstantEAcc.ConstantEAcc(self.updater.ctx, self.updater.queue)
        fieldKick.eField = np.array([Ex, Ey, 0], dtype = np.float32)
        self.accList.append(fieldKick)

        self.t = 0

    def take_steps(self, dt, numSteps = 1):
        xd = cl_array.to_device(self.queue, self.ptcls.x(), async = True)
        yd = cl_array.to_device(self.queue, self.ptcls.y(), async = True)
        zd = cl_array.to_device(self.queue, self.ptcls.z(), async = True)
        vxd = cl_array.to_device(self.queue, self.ptcls.vx(), async = True)
        vyd = cl_array.to_device(self.queue, self.ptcls.vy(), async = True)
        vzd = cl_array.to_device(self.queue, self.ptcls.vz(), async = True)
        qd = cl_array.to_device(self.queue, self.ptcls.q(), async = True)
        md = cl_array.to_device(self.queue, self.ptcls.m())

        for n in range(numSteps):
            self.updater.update(xd, yd, zd, vxd, vyd, vzd, qd, md,
                    self.accList, self.t, dt)
        self.t += numSteps * dt

        xd.get(self.queue, self.ptcls.x(), async = True)
        yd.get(self.queue, self.ptcls.y(), async = True)
        zd.get(self.queue, self.ptcls.z(), async = True)
        vxd.get(self.queue, self.ptcls.vx(), async = True)
        vyd.get(self.queue, self.ptcls.vy(), async = True)
        vzd.get(self.queue, self.ptcls.vz())

mySim = Sim()

Bz = 4.5
E = 1.0e-2
vInitial = 1.0e0
numsteps = 1000
dt = 1.0e-3
mass = 9 * 1934 * mySim.ptcls.fundmass 

omegaB = mySim.ptcls.fundcharge * Bz / mass 
print "omegaB = ", omegaB
print "nuB = ", omegaB / 2.0 / np.pi / 1.0e6, "MHz"
print "a = ", vInitial / omegaB * 1.0e6, "mu m"
print "kick dv = ", dt * E * mySim.ptcls.fundcharge / mass
print "vdrift = ", E / Bz
print "ldrift = ", dt * numsteps * E / Bz

mySim.ptcls.set_nptcls(1)
mySim.ptcls.init_ptcls(mass = mass) 
mySim.ptcls.ptclList[0][0] = 0.0
mySim.ptcls.ptclList[1][0] = 0.0
mySim.ptcls.ptclList[2][0] = 0.0
mySim.ptcls.ptclList[3][0] = vInitial
mySim.ptcls.ptclList[4][0] = 0.0
mySim.ptcls.ptclList[5][0] = 0.0
mySim.init_sim(Bz, E, 0)

traj = []
for i in range(0, numsteps):
    traj.append(np.copy(mySim.ptcls.ptclList[0:6, 0]))
    mySim.take_steps(dt, 1)
traj = np.array(traj)

plt.clf()
plt.plot(1000.0 * traj[:,0], 1000.0 * traj[:,1],'.')
plt.xlabel(r'$x/\rm{mm}$')
plt.ylabel(r'$y/\rm{mm}$')
plt.gcf().subplots_adjust(left = 0.15, bottom = 0.19, top=0.95,
  right=0.95)
plt.savefig('eCrossBTestXY.pdf')
plt.clf()
plt.plot(traj[:,3], traj[:,4],'o')
plt.savefig('eCrossBTestVXVY.pdf')
plt.clf()
plt.plot(np.linspace(0, numsteps * dt, traj.shape[0]), 1000.0 * traj[:,1])
plt.xlabel(r'$t/\rm{s}$')
plt.ylabel(r'$y/\rm{mm}$')
plt.gcf().subplots_adjust(left = 0.15, bottom = 0.19, top=0.95,
  right=0.95)
plt.savefig('eCrossBTestY.pdf')


# vi: ts=4 sw=4

