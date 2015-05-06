import uci.Sim as Sim
import uci.TrapConfiguration as TrapConfig
import numpy as np


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
s.ptcls.set_nptcls(300)
s.ptcls.sigma = 2.0e-4
s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
axialFrictionCoeff = 1.0e7
angularFrictionCoeff = 1.0e7
s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff,
    recoilVelocity = 0.01, scatterRate = 1.0e6)
s.updater.peakCoolingRate = 1.0e4
s.updater.peakDiffusionConstant = 0.1 * np.sqrt(1.0e4)
s.updater.width = 30.0e-6
s.updater.offset = 0.0
s.spin_up()


