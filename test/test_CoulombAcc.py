import uci.CoulombAcc as uci
import numpy as np
import pyopencl as cl
import pyopencl.array as cl_array

testCtx = cl.create_some_context(interactive = True)
testQueue = cl.CommandQueue(testCtx)

def test_Constructor():
    coulomb_acc = uci.CoulombAcc()

def test_ForceOnSingleParticleIsZero():
    coulomb_acc = uci.CoulombAcc(testCtx, testQueue)
    one = np.ones(1)
    ax = np.zeros(1)
    ay = np.zeros(1)
    az = np.zeros(1)

    xd = cl_array.to_device(testQueue, one)
    yd = cl_array.to_device(testQueue, one)
    zd = cl_array.to_device(testQueue, one)
    vxd = cl_array.to_device(testQueue, one)
    vyd = cl_array.to_device(testQueue, one)
    vzd = cl_array.to_device(testQueue, one)
    qd = cl_array.to_device(testQueue, one)
    md = cl_array.to_device(testQueue, one)
    axd = cl_array.to_device(testQueue, ax)
    ayd = cl_array.to_device(testQueue, ay)
    azd = cl_array.to_device(testQueue, az)

    coulomb_acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
            axd, ayd, azd, 0)

    axd.get(testQueue, ax)
    ayd.get(testQueue, ay)
    azd.get(testQueue, az)
    assert ax[0] == 0
    assert ay[0] == 0
    assert az[0] == 0
    

def test_TwoParticlesWithEqualChargeRepelEachOther():
    coulomb_acc = uci.CoulombAcc(testCtx, testQueue)
    one = np.ones(2)
    ax = np.zeros(2)
    ay = np.zeros(2)
    az = np.zeros(2)

    x = np.array([0.1, 1])
    y = np.array([0.2, 2.3])
    z = np.array([0.3, 2.7])
    xd = cl_array.to_device(testQueue, x)
    yd = cl_array.to_device(testQueue, y)
    zd = cl_array.to_device(testQueue, z)
    vxd = cl_array.to_device(testQueue, one)
    vyd = cl_array.to_device(testQueue, one)
    vzd = cl_array.to_device(testQueue, one)
    qd = cl_array.to_device(testQueue, one)
    md = cl_array.to_device(testQueue, one)
    axd = cl_array.to_device(testQueue, ax)
    ayd = cl_array.to_device(testQueue, ay)
    azd = cl_array.to_device(testQueue, az)

    coulomb_acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
            axd, ayd, azd, 0)

    axd.get(testQueue, ax)
    ayd.get(testQueue, ay)
    azd.get(testQueue, az)
    assert ax[0] != 0
    assert np.abs(ax[0] + ax[1]) < 1.0e-6
    assert np.abs(ay[0] + ay[1]) < 1.0e-6
    assert np.abs(az[0] + az[1]) < 1.0e-6


def reference_solution(x, y, z, vx, vy, vz, q, m, ax, ay, az):
    epsilon0 = 8.854187817e-12
    for i in range(x.size):
        for j in range(x.size):
            prefactor = 1.0 / (4.0 * np.pi * epsilon0) * q[i] * q[j]
            r = np.sqrt(
                    (x[i] - x[j]) * (x[i] - x[j]) +
                    (y[i] - y[j]) * (y[i] - y[j]) +
                    (z[i] - z[j]) * (z[i] - z[j]) +
                    1.0e-20
                    )
            rCubed = np.power(r, 3.0)
            ax[i] += prefactor * (x[i] - x[j]) / rCubed / m[i]
            ay[i] += prefactor * (y[i] - y[j]) / rCubed / m[i]
            az[i] += prefactor * (z[i] - z[j]) / rCubed / m[i]


def compareWithReferenceSol(n):
    coulomb_acc = uci.CoulombAcc(testCtx, testQueue)
    x = np.random.random_sample(n) - 0.5
    y = np.random.random_sample(n) - 0.5
    z = np.random.random_sample(n) - 0.5
    vx = np.random.random_sample(n) - 0.5
    vy = np.random.random_sample(n) - 0.5
    vz = np.random.random_sample(n) - 0.5
    q = np.random.random_sample(n) - 0.5
    m = np.random.random_sample(n) - 0.5
    ax = np.zeros(n)
    ay = np.zeros(n)
    az = np.zeros(n)

    xd = cl_array.to_device(testQueue, x)
    yd = cl_array.to_device(testQueue, y)
    zd = cl_array.to_device(testQueue, z)
    vxd = cl_array.to_device(testQueue, vx)
    vyd = cl_array.to_device(testQueue, vy)
    vzd = cl_array.to_device(testQueue, vz)
    qd = cl_array.to_device(testQueue, q)
    md = cl_array.to_device(testQueue, m)
    axd = cl_array.to_device(testQueue, ax)
    ayd = cl_array.to_device(testQueue, ay)
    azd = cl_array.to_device(testQueue, az)

    coulomb_acc.computeAcc(xd, yd, zd, vxd, vyd, vzd, qd, md,
            axd, ayd, azd, 0)

    axd.get(testQueue, ax)
    ayd.get(testQueue, ay)
    azd.get(testQueue, az)

    ax_ref = np.zeros(n)
    ay_ref = np.zeros(n)
    az_ref = np.zeros(n)
    reference_solution(x, y, z, vx, vy, vz, q, m, ax_ref, ay_ref, az_ref)
    for i in range(n):
        assert np.abs(ax[i] - ax_ref[i]) / (
                np.abs(ax[i]) + np.abs(ax_ref[i])) < 1.0e-6


def test_SmallSystem():
    compareWithReferenceSol(10)


def test_PowerOfTwo():
    compareWithReferenceSol(128)


