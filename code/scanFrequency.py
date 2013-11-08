# the purpose of this simulation is to study the 1-2 plane transition

import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np
#import matplotlib.pyplot as plt

scanNumber = 5

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
    axialFrictionCoeff = 2.0e5
    angularFrictionCoeff = 1.0e6
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff,
        recoilVelocity = 0.01, scatterRate = 1.0e6)
    s.ptcls.ptclList = np.loadtxt(filename, dtype=np.float32)
    s.t=0.0
    return s

def savePtcls(sim, filename):
    np.savetxt(filename, sim.ptcls.ptclList)

def buildFileName(path, basename, omega, suffix):
    return path + basename + str(omega / 2 / np.pi) + suffix

s = loadCrystal('runs/run10_999.dat')

def rotate(xy, phase):
    return np.array([
            xy[0] * np.cos(phase) - xy[1] * np.sin(phase),
            xy[0] * np.sin(phase) + xy[1] * np.cos(phase)
            ])

def scrambleZCoords(sim):
    nPtcls = sim.ptcls.ptclList[0].size
    sim.ptcls.ptclList[2] = np.random.standard_normal(nPtcls) * 1.0e-6

phaseInitial = 0.880 * np.pi
s.ptcls.ptclList[:2] = rotate(s.ptcls.ptclList[:2], phaseInitial)
s.ptcls.ptclList[3:5] = rotate(s.ptcls.ptclList[3:5], phaseInitial)

# dump initial state
savePtcls(s,
    buildFileName(
        'frequencyScan/nptcls400/',
        'scan'+str(scanNumber)+'_', s.trapConfiguration.omega, '.dat'))

# Description of the frequency range
dt = 1.0e-8
dOmega = 0.1e3 * 2 * np.pi
omegaMax = 55.0e3 * 2 * np.pi
omegaMin = 41.0e3 * 2 * np.pi

s.trapConfiguration.omega = omegaMax
scrambleZCoords(s)

numStepsEquilibrate = 20000

print "Start equilibration ..."
for j in range(10):
    print "j=", j
    scrambleZCoords(s)
    for i in range(j*10, (j+1)*10):
        s.spin_up()
        s.take_steps(dt, numStepsEquilibrate/4)
        savePtcls(s,
            buildFileName(
                'frequencyScan/nptcls127/',
                'scan'+str(scanNumber)+'_equ_'+str(i)+'_', s.trapConfiguration.omega, '.dat'))
s.take_steps(dt, 20 * numStepsEquilibrate)
print "... Equilibration finished."

print "Starting frequency sweep ..."
for omega in np.arange(omegaMax, omegaMin, -dOmega):
    print "omega/2pi=", omega / 2.0 / np.pi
    s.trapConfiguration.omega = omega
    s.take_steps(dt, numStepsEquilibrate)
    savePtcls(s,
        buildFileName(
            'frequencyScan/nptcls127/',
            'scan'+str(scanNumber)+'_', s.trapConfiguration.omega, '.dat'))



