import ucilib.Sim as Sim
import ucilib.BorisUpdater as BorisUpdater
import numpy as np


# Some helpful constants.
fund_charge = 1.602176565e-19


# Mass of Be^+ ions.
ion_mass = 8.9465 * 1.673e-27


# Create a simulation with n particles.
n = 10000
s = Sim.Sim()
s.ptcls.set_nptcls(n)


# 1/e radius of cloud.
s.ptcls.sigma = 2.0e-4
s.ptcls.init_ptcls(charge = fund_charge, mass = ion_mass)


# Turn the first n/2 particles into electrons by setting their mass and
# charge.
s.ptcls.q()[:(n/2)] = -fund_charge * np.ones(n/2)
s.ptcls.m()[:(n/2)] = 9.1e-31 * np.ones(n/2)


# Finally we set the updater.
s.updater = BorisUpdater.BorisUpdater(s.ctx, s.queue)


