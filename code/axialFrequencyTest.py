import ucilib.Sim as Sim
import ucilib.TrapConfiguration as TrapConfig
import numpy as np
import matplotlib.pyplot as plt


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
s.ptcls.set_nptcls(1)
s.ptcls.rmax = 2.0e-4
s.ptcls.init_ptcls(charge = fundcharge, mass = ionMass)
axialFrictionCoeff = 0.0e0
angularFrictionCoeff = 0.0e0
s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
s.spin_up()

timeSeries=[]
for i in range(0,1000):
    timeSeries.append(s.ptcls.ptclList.copy())
    s.take_steps(1.0e-9, 100)

zs = np.array(timeSeries)[:,2]
spectrum = abs(np.fft.fft(zs[:,0]))**2
psd=spectrum[0:499]+spectrum[1000:500:-1]
plt.clf()
plt.semilogy(np.arange(0, np.pi/0.1-np.pi/0.1/500, np.pi/0.1/500), psd)
plt.savefig('axialSpectrum.pdf')

