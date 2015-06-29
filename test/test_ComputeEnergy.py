from uci.ComputePotentialEnergy import ComputePotentialEnergy
import numpy
import pyopencl as cl

k = 1./(4.*numpy.pi*8.854187817620389e-12)
electron_charge = 1.602176565e-19

impactFact = 1.0e-9**2 

f32 = numpy.float32
f64 = numpy.float64

testCtx = cl.create_some_context(interactive = True)
testQueue = cl.CommandQueue(testCtx)

def test_constructor():
    computeEnergy = ComputePotentialEnergy(testCtx, testQueue)
    
def test_compare_device_host_64():   
    N = 100;
    x = numpy.random.random(N)
    y = numpy.random.random(N)
    z = numpy.random.random(N)
    q = numpy.concatenate((numpy.ones(N/2),-numpy.ones(N/2)))*electron_charge
    computeEnergy = ComputePotentialEnergy(testCtx, testQueue)
    energyd = computeEnergy.computeEnergy(x,y,z,q)
    energyh = 0.0
    for i in range(x.size):
        for j in range(x.size):
            if i!=j:
                r = numpy.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2+(z[i]-z[j])**2+impactFact)
                energyh += k * q[i]*q[j]/r/2.0;
    assert numpy.fabs(energyh - energyd)/numpy.fabs(energyh)< 1.0e-10
    
def test_compare_device_host_32():   
    N = 100;
    x = numpy.random.random(N).astype(f32)
    y = numpy.random.random(N).astype(f32)
    z = numpy.random.random(N).astype(f32)
    q_ion = numpy.ones(N/2,dtype = f32)*electron_charge
    q_electron = - q_ion
    q = numpy.concatenate((q_ion,q_electron))
    computeEnergy = ComputePotentialEnergy(testCtx, testQueue)
    energyd = computeEnergy.computeEnergy(x,y,z,q)
    energyh = 0.0
    for i in range(x.size):
        for j in range(x.size):
            if i!=j:
                r = numpy.sqrt((x[i]-x[j])**2+(y[i]-y[j])**2+(z[i]-z[j])**2+impactFact)
                energyh += k * q[i]*q[j]/r/2.0;
    assert numpy.fabs(energyh - energyd)/numpy.fabs(energyh)< 1.0e-5
