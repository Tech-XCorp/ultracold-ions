import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np
import ucilib.CoolingLaserAdvance as coolingLsr

from time import time


def loadCrystal(filename):
    t = TrapConfig.TrapConfiguration()
    t.Bz = 4.4584
    #V0 in V/m^2
    t.kz = 2.0 * 1.167e6
    delta = 0.0036
    t.kx = -(0.5 + delta) * t.kz
    t.ky = -(0.5 - delta) * t.kz
    t.theta = 0
    t.omega = 2.0 * np.pi * 44.0e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(127)
    s.ptcls.rmax = 1.0e-4
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = None
    angularFrictionCoeff = None
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff,
        recoilVelocity = 0.01, scatterRate = 1.0e6)
    s.ptcls.ptclList = np.loadtxt(filename, dtype=np.float32)
    s.t=0.0
    return s


def buildFileName(path, basename, suffix):
    return path + basename + suffix

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

def scrambleZCoords(sim):
    nPtcls = sim.ptcls.ptclList[0].size
    sim.ptcls.ptclList[2] = np.random.standard_normal(nPtcls) * 1.0e-6


def savePtcls(sim, filename):
    np.savetxt(filename, sim.ptcls.ptclList)

#s = createCrystal()
#np.savetxt("crystal127.dat", s.ptcls.ptclList)

s = loadCrystal('runs/run10_999.dat')

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])
phaseInitial = 0.880 * np.pi
s.ptcls.ptclList[:2] = rotate(s.ptcls.ptclList[:2], phaseInitial)
s.ptcls.ptclList[3:5] = rotate(s.ptcls.ptclList[3:5], phaseInitial)

#runNumber = 3
#
#s.accList = s.accList[0:2]
#s.updater.axialFrictionCoeff=None
#s.updater.angularFrictionCoeff=None
#
#claAlongZ = coolingLsr.CoolingLaserAdvance(s.ctx, s.queue)
#claAlongZ.sigma = None
#claAlongZ.k0 = np.array([0, 0, -2.0 * np.pi / 313.0e-9], dtype = np.float32)
#s.accList.append(claAlongZ)
#perpCooling = coolingLsr.CoolingLaserAdvance(s.ctx, s.queue)
#perpCooling.sigma = 30.0e-6
#perpCooling.k0 = np.array([2.0 * np.pi / 313.0e-9, 0, 0], dtype = np.float32)
#perpCooling.S = 0.5
#s.accList.append(perpCooling)
#
#print "theta=", s.trapConfiguration.theta
#
#nSteps = 2000
#dt = 5.0e-9
#t0 = time()
#for i in range(nSteps):
#    ti = time()
#    print "i: ", i, "wall time: ", ti - t0, "sim. time: ", s.t
#    savePtcls(s,
#        buildFileName(
#            'axialPhononRuns/',
#            'run'+str(runNumber)+'_'+str(i), '.dat'))
#    s.take_steps(dt, 100)
#

runNumber = 4

s.accList = s.accList[0:2]
s.updater.axialFrictionCoeff=None
s.updater.angularFrictionCoeff=None

claAlongZ = coolingLsr.CoolingLaserAdvance(s.ctx, s.queue)
claAlongZ.sigma = None
claAlongZ.k0 = np.array([0, 0, -2.0 * np.pi / 313.0e-9], dtype = np.float32)
s.accList.append(claAlongZ)
perpCooling = coolingLsr.CoolingLaserAdvance(s.ctx, s.queue)
perpCooling.sigma = 30.0e-6
perpCooling.k0 = np.array([2.0 * np.pi / 313.0e-9, 0, 0], dtype = np.float32)
perpCooling.S = 0.5
s.accList.append(perpCooling)

#equilibrate    
dt = 1.0e-8
s.take_steps(dt, 10000)

#now turn off the cooling
s.accList = s.accList[0:2]

print "theta=", s.trapConfiguration.theta

nSteps = 2000
dt = 5.0e-9
t0 = time()
for i in range(nSteps):
    ti = time()
    print "i: ", i, "wall time: ", ti - t0, "sim. time: ", s.t
    savePtcls(s,
        buildFileName(
            'axialPhononRuns/',
            'run'+str(runNumber)+'_'+str(i), '.dat'))
    s.take_steps(dt, 100)



#runNumber = 5
#
#s.accList = s.accList[1:2]
#s.updater.axialFrictionCoeff=None
#s.updater.angularFrictionCoeff=None
#
## Displace entire crystal along the z axis to measure the com mode
## frequency
#s.ptcls.ptclList[2] += 1.0e-6
#print s.accList
#
#nSteps = 200
#dt = 1.0e-8
#t0 = time()
#for i in range(nSteps):
#    ti = time()
#    print "i: ", i, "wall time: ", ti - t0, "sim. time: ", s.t
#    savePtcls(s,
#        buildFileName(
#            'axialPhononRuns/',
#            'run'+str(runNumber)+'_'+str(i), '.dat'))
#    s.take_steps(dt, 50)

#
# vi: sw=4 ts=4
