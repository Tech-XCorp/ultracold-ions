import uci.Ptcls as Ptcls
import numpy as np

def test_compute_kinetic_energies():
    vx = np.array([0.1, 0.2])
    vy = np.array([10.1, 0.3])
    vz = np.array([23.4, 42.5])
    m = np.array([2.3, 3.4])
    kinetic_energies = Ptcls.compute_kinetic_energies(vx, vy, vz, m)
    for i in range(2):
        assert abs(kinetic_energies[i] -
                0.5 * m[i] * (vx[i]**2 + vy[i]**2 + vz[i]**2)) < 1.0e-7


def test_compute_temperature():
    vx = np.array([0.1, 0.2])
    vy = np.array([10.1, 0.3])
    vz = np.array([23.4, 42.5])
    m = np.array([2.3, 3.4])
    temperature = Ptcls.compute_temperature(vx, vy, vz, m)
    assert temperature > 0


def test_temperature_of_particles():
    ptcls = Ptcls.Ptcls()
    ptcls.vth = 1.0e4
    ptcls.set_nptcls(10)
    ptcls.init_ptcls()
    assert ptcls.temperature() > 0
