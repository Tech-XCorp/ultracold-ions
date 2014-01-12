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
    t.theta = 0.0
    t.omega = 2.0 * np.pi * 43.0e3
    fundcharge = 1.602176565e-19
    ionMass = 8.9465 * 1.673e-27
    s = Sim.Sim()
    s.ptcls.set_nptcls(400)
    s.ptcls.rmax = 2.0e-4
    s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
    axialFrictionCoeff = 1.0e4
    angularFrictionCoeff = 1.0e7
    s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
    s.ptcls.ptclList = np.loadtxt(initialStateFile, dtype=np.float32)
    s.ptcls.ptclList[7] = ionMass * np.ones(s.ptcls.ptclList[7].shape)
    s.t = t0
    s.spin_up()
    return s

s = createSimulation('convergenceStudy/initialState_1_1ms_400ptcls.txt',
    0.0)
s.init_sim(s.trapConfiguration, s.updater.axialDampingCoefficient, s.updater.angularDampingCoefficient, scatterRate = 1.0e8)
s.take_steps(1.0e-8, 100000)
s.updater.axialDampingCoefficient = 0.0
s.updater.angularDampingCoefficient = 0.0
s.accList[2].diffusionConstant=0.0

def dumpSim(s, path):
    filename = path + str(s.t) + '.txt'
    np.savetxt(filename, s.ptcls.ptclList)

for i in range(0, 20000):
    s.take_steps(1.0e-8, 40)
    dumpSim(s, 'timeSeries/timeSeries4_')

