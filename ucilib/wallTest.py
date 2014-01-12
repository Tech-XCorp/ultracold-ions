import Sim
import TrapConfiguration
import numpy as np
import matplotlib.pyplot as plt


t = TrapConfiguration.TrapConfiguration()
t.Bz = 0.0001
#V0 in V/m^2
t.kz = 1.0e6
t.kx = 1.0e6
t.ky = 1.0e6
t.theta = 0
t.omega = 1.0

fundcharge = 1.602176565e-19
fundmass = 9.10938215e-31
s = Sim.Sim()
s.ptcls.set_nptcls(1)
s.ptcls.rmax = 2.0e-4
s.ptcls.init_ptcls(charge = fundcharge, mass = 1932.0 * fundmass * 13.0)
axialFrictionCoeff = 1.0
angularFrictionCoeff = 1.0
s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
s.spin_up()

for i in range(100):
    s.take_steps(1.0e-8, 10)
    plt.plot(s.ptcls.x(), s.ptcls.y(),'.b')
    plt.plot(s.ptcls.x(), s.ptcls.z(),'.r')

plt.savefig('isotropic.pdf')

plt.figure()
t = TrapConfiguration.TrapConfiguration()
t.Bz = 0.0001
#V0 in V/m^2
t.kz = 16.0e6
t.kx = 1.0e6
t.ky = 4.0e6
t.theta = 0
t.omega = 1.0

fundcharge = 1.602176565e-19
fundmass = 9.10938215e-31
s = Sim.Sim()
s.ptcls.set_nptcls(1)
s.ptcls.rmax = 2.0e-4
s.ptcls.init_ptcls(charge = fundcharge, mass = 1932.0 * fundmass * 13.0)
axialFrictionCoeff = 1.0
angularFrictionCoeff = 1.0
s.init_sim(t, axialFrictionCoeff, angularFrictionCoeff)
s.spin_up()

for i in range(100):
    s.take_steps(1.0e-8, 10)
    plt.plot(s.ptcls.x(), s.ptcls.y(),'.b')
    plt.plot(s.ptcls.x(), s.ptcls.z(),'.r')

plt.savefig('anisotropic.pdf')
plt.clf()

t=0
dt=1.0e-8
data=[]
for i in range(100):
    s.take_steps(dt, 10)
    t+=dt
    data.append(np.array([t, s.ptcls.x(), s.ptcls.y(), s.ptcls.z()]))
data=np.array(data)
print data
plt.plot(data[:,0],data[:,1])
plt.plot(data[:,0],data[:,2])
plt.plot(data[:,0],data[:,3])
plt.savefig('timeseries.pdf')

