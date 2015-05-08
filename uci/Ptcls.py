# vi: ts=4 sw=4

import random
import numpy
import math


def compute_kinetic_energies(vx, vy, vz, m):
    """Compute the kinetic energies of a set of particles."""
    return 0.5 * m * (vx**2 + vy**2 + vz**2)


def compute_temperature(vx, vy, vz, m):
    """Compute temperature of neutral particles in free space.
        
        This function assumes that all motion of the particles is
        thermal,  i.e. there is no center of mass momentum or angular
        momentum.
        """
    kB = 1.3806e-23
    return (2.0 / 3.0) * numpy.mean(compute_kinetic_energies(vx, vy, vz, m)) / kB
    

class Ptcls():
    """An ensemble of particles."""
    
    def __init__(self, n = 1):
        self.numPtcls = 1
        self.sigma = 1.0e-4
        self.vbar = 0
        self.vth = 0

        self.ptclList = 0.0 * numpy.ndarray([8, self.numPtcls],dtype=numpy.float32)

        self.prec = numpy.float32
        self.numPtcls = n

    def init_ptcls(self, pstart = 0, pend = 0, charge = 1.602176565e-19,
            mass = 8.9465 * 1.673e-27, source = 'gaussian'):

        self.ptclList = 0. * numpy.ndarray([8, self.numPtcls], dtype = self.prec)
        if pend == 0:
            pend = self.numPtcls

        if source=='gaussian':
            for j in range(pstart, pend):
                r = abs(random.gauss(0.,self.sigma))
                theta = numpy.arccos(2.*random.random()-1)
                phi = 2.*numpy.pi*random.random()
                self.ptclList[0][j]=r*numpy.sin(theta)*numpy.cos(phi)
                self.ptclList[1][j]=r*numpy.sin(theta)*numpy.sin(phi)
                self.ptclList[2][j]=r*numpy.cos(theta)
                vr = random.gauss(self.vbar,self.vth)
                theta = numpy.arccos(2.*random.random()-1)
                phi = 2.*numpy.pi*random.random()
                self.ptclList[3][j]=vr*numpy.sin(theta)*numpy.cos(phi)
                self.ptclList[4][j]=vr*numpy.sin(theta)*numpy.sin(phi)
                self.ptclList[5][j]=vr*numpy.cos(theta)
                self.ptclList[6][j]=charge
                self.ptclList[7][j]=mass
        elif source:
            self.ptclList = numpy.loadtxt(source)
            self.numPtcls = myarr.shape[1]

    def temperature(self):
        """Compute temperature of the ensemble of particles.
            
            This function assumes that all motion of the particles is
            thermal,  i.e. there is no center of mass momentum or angular
            momentum.
        """
        return compute_temperature(self.ptclList[3], self.ptclList[4],
                self.ptclList[5], self.ptclList[7])

    def set_nptcls(self, np):
        self.numPtcls = np
        self.ptclList = numpy.resize(self.ptclList, [8, self.numPtcls])

    def x(self):
        return self.ptclList[0]

    def y(self):
        return self.ptclList[1]

    def z(self):
        return self.ptclList[2]

    def vx(self):
        return self.ptclList[3]

    def vy(self):
        return self.ptclList[4]

    def vz(self):
        return self.ptclList[5]

    def q(self):
        return self.ptclList[6]

    def m(self):
        return self.ptclList[7]


