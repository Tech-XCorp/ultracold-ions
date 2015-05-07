import uci.BorisUpdater as BorisUpdater
import uci.Ptcls as Ptcls
import numpy as np


# Some helpful constants.
fund_charge = 1.602176565e-19


# Mass of Sr88 ions.
atomic_unit = 1.66053892e-27
ion_mass = 87.9056 * atomic_unit


# initialize particles
n_wells = 100
n_ions = n_wells**3
ptcls = Ptcls.Ptcls()
ptcls.set_nptcls(2 * n_ions)

# ions
lattice_spacing = 1.0e-6
xmin = -0.5 * (n_wells - 1) * lattice_spacing
for i in range(n_ions):
    ptcls.x()[i] = xmin + lattice_spacing * ((i / (n_wells**0)) % n_wells)
    ptcls.y()[i] = xmin + lattice_spacing * ((i / (n_wells**1)) % n_wells)
    ptcls.z()[i] = xmin + lattice_spacing * ((i / (n_wells**2)) % n_wells)
ptcls.ptclList[3:6,:n_ions] = 0
ptcls.ptclList[6,:n_ions] = fund_charge
ptcls.ptclList[7,:n_ions] = ion_mass

#electrons
ptcls.ptclList[0:3,n_ions:] = np.random.normal(0.0, 0.5 * abs(xmin),
                                               ptcls.ptclList[0:3,n_ions:].shape)
electron_temperature = 300.0
electron_mass = 9.10938291e-31
kB = 1.3806e-23
vThermal = np.sqrt(kB * electron_temperature / electron_mass)
ptcls.ptclList[3:6,n_ions:] = np.random.normal(0.0, vThermal,
                                               ptcls.ptclList[3:6,n_ions:].shape)
ptcls.ptclList[6,n_ions:] = -fund_charge
ptcls.ptclList[7,n_ions:] = electron_mass
