import numpy as np
import matplotlib.pyplot as plt

def effectivePotential(e, V0, Bz, m, Omega):
  return (e * Bz * Omega - m * Omega * Omega - e * V0)

omegas = np.arange(0,1.0e5,1.0e3)*2 * np.pi
plt.plot(omegas/2/np.pi,effectivePotential(1.6e-19, 1.167e6, 4.5, 13*1932*9.1e-31, omegas)/1.6e-19)

plt.savefig("effectiveRadialPotential.pdf")

