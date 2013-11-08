import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np
import matplotlib.pyplot as plt

def createSimulation(initialStateFile, t0):
    t = TrapConfig.TrapConfiguration()
    t.Bz = 4.5
    #V0 in V/m^2
    t.kz = 2.0 * 1.167e6
    delta = 0.010
    t.kx = -(0.5 + delta) * t.kz
    t.ky = -(0.5 - delta) * t.kz
    t.theta = -0.5
    t.omega = 2.0 * np.pi * 42.5e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(400)
    s.ptcls.rmax = 2.0e-4
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = 1.0
    angularFrictionCoeff = 1.0
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
    s.ptcls.ptclList = np.loadtxt(initialStateFile, dtype=np.float32)
    s.t = t0
    s.spin_up()
    return s

def advanceSimulation(s, dt, Tmax):
    advancedSim = s.copy()
    numsteps = int(Tmax / dt)
    advancedSim.take_steps(dt, numsteps)
    return advancedSim

s=createSimulation('convergenceStudy/initialState_1_1ms_400ptcls.txt', 0.0)
simulations = []
numSteps = 10000
for t in range(numSteps):
     s.take_steps(1.0e-8, 1)
     simulations.append(s.copy())

radialFrequencies = [
    simulations[t].angular_velocities()/simulations[t].radii()
    for t in range(0, numSteps)]
means=[np.mean(radialFrequencies[t]) for t in range(numSteps)]
stddevs=[np.sqrt(np.linalg.norm(radialFrequencies[t])**2 / s.ptcls.numPtcls
    - means[t]**2) for t in range(0, numSteps)]

plt.plot(np.array(means) + 0.0 * np.array(stddevs),'b')
plt.plot(np.array(means) - 0.5 * np.array(stddevs),'r')
plt.plot(np.array(means) + 0.5 * np.array(stddevs),'r')
plt.xlabel('t/10^-8 s')
plt.ylabel('nu/Hz')
plt.savefig('rockingModeWithVarianceDOmega.pdf')

plt.clf()
plt.plot(np.array(means))
plt.xlabel('t/10^-8 s')
plt.ylabel('nu/Hz')
plt.savefig('rockingModeDOmega.pdf')

