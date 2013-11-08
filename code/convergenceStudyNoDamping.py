import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np

def createSimulation(initialStateFile, t0):
    t = TrapConfig.TrapConfiguration()
    t.Bz = 4.5
    #V0 in V/m^2
    t.kz = 2.0 * 1.167e6
    delta = 0.010
    t.kx = -(0.5 + delta) * t.kz
    t.ky = -(0.5 - delta) * t.kz
    t.theta = 0
    t.omega = 2.0 * np.pi * 43.0e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(400)
    s.ptcls.rmax = 2.0e-4
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = 0.0
    angularFrictionCoeff = 0.0
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
    s.ptcls.ptclList = np.loadtxt(initialStateFile, dtype=np.float32)
    s.t = t0
    return s

def advanceSimulation(s, dt, Tmax):
    advancedSim = s.copy()
    numsteps = int(Tmax / dt)
    advancedSim.take_steps(dt, numsteps)
    return advancedSim

def computeError(initialState, referenceSimulation, dt, Tmax):
    advancedSim = advanceSimulation(initialState, dt, Tmax)
    return np.linalg.norm(advancedSim.ptcls.ptclList[0:2]-
        referenceSimulation.ptcls.ptclList[0:2]) / np.sqrt(advancedSim.ptcls.ptclList.shape[1])

s=createSimulation('convergenceStudy/initialState_1_1ms_400ptcls.txt', 0.0011)

tmax = 1.0e-4
referenceDT = 1.0e-10
ref = advanceSimulation(s, referenceDT, tmax)
exponents = np.arange(1, 8)
dts = referenceDT*(2**exponents)
errors = [computeError(s, ref, dt, tmax) for dt in dts]

